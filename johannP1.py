from p1_support import load_level, show_level, save_level_costs
from math import inf, sqrt
from heapq import heappop, heappush

def dijkstras_shortest_path(source, destination, level, adj):
    """ Searches for a minimal cost path through a level using Dijkstra's algorithm.

    Args:
        source: The initial cell from which the path extends.
        destination: The end location for the path.
        level: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        If a path exits, return a list containing all cells from source to destination.
        Otherwise, return None.

    """

    source = (source, 0)
    queue = [(source[1], source[0])]
    dist = {source[0] : 0}
    prev = {}

    while queue:
        current_node = heappop(queue)
        if current_node[1] == destination:
            path = []
            n = destination
            while n in prev:
                path.insert(0, prev[n])
                n =  prev[n]
            path.append(destination)
            return path
        else:
            for adj_node in adj(level, current_node[1]):
                adj_node = (adj_node[1], adj_node[0])
                new_cost = dist[current_node[1]] + adj_node[0]
                if adj_node[1] not in dist or new_cost < dist[adj_node[1]]:
                #if adj_node[1] not in dist or alt < dist[current_node[1]]:
                    prev[adj_node[1]] = current_node[1]
                    dist[adj_node[1]] = new_cost
                    heappush(queue, adj_node)
                    
    return None   

def dijkstras_shortest_path_to_all(source, level, adj):
    """ Calculates the minimum cost to every reachable cell in a level from the source.

    Args:
        source: The initial cell from which the path extends.
        level: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        A dictionary, mapping destination cells to the cost of a path from the source.
    """
    def calculate_cost(path, level):
        lastNode = path[0]
        total_cost = 0
        #print(level)
        for node in path[1:]:
            cost = level['spaces'][lastNode] + level['spaces'][node]
            if(lastNode[0] != node[0] and lastNode[1] != node[1]):         
                cost *= 0.5 * sqrt(2)
            else:
                cost *= 0.5
            total_cost += cost
            lastNode = node
        return total_cost

    costs = {}

    for cell in level['spaces']:
        path = dijkstras_shortest_path(source, cell, level, adj)
        if path is not None:
            costs[cell] = calculate_cost(path, level)

    return costs



def navigation_edges(level, cell):
    """ Provides a list of adjacent cells and their respective costs from the given cell.

    Args:
        level: A loaded level, containing walls, spaces, and waypoints.
        cell: A target location.

    Returns:
        A list of tuples containing an adjacent cell's coordinates and the cost of the edge joining it and the
        originating cell.

        E.g. from (0,0):
            [((0,1), 1),
             ((1,0), 1),
             ((1,1), 1.4142135623730951),
             ... ]
    """
    if 'dimX' not in level or 'dimY' not in level:  
        xs, ys = zip(*(list(level['spaces'].keys()) + list(level['walls'])))
        dimX = max(xs)
        dimY = max(ys)
        level['dimX'] = dimX
        level['dimY'] = dimY
    else:
        dimX = level['dimX']
        dimY = level['dimY']

    adjList = []
    x = cell[0]
    y = cell[1]

    def checkAdjacent(coords, level, diagonal=False):
        startCell = (cell, level['spaces'][cell])
        if coords in level['spaces'] and not diagonal:
            return (coords, (level['spaces'][coords] + startCell[1]) * 0.5)
        elif coords in level['spaces'] and diagonal:
            adj =  (coords, level['spaces'][coords])
            if adj != None:
                return (adj[0], (adj[1] + startCell[1]) * sqrt(2) * 0.5)
        return None

    #top-left
    if x > 0 and y > 0:
        adjList.append(checkAdjacent((x - 1, y - 1), level, True))
    #above
    if y > 0:
        adjList.append(checkAdjacent((x, y - 1), level))
    #top-right
    if x < dimX and y > 0:
        adjList.append(checkAdjacent((x + 1, y - 1), level, True))
    #right
    if x < dimX:
        adjList.append(checkAdjacent((x + 1, y), level))
    #bottom-right
    if y < dimY and x < dimX:
        adjList.append(checkAdjacent((x + 1, y + 1), level, True))
    #below
    if y < dimY:
        adjList.append(checkAdjacent((x, y + 1), level))
    #bottom-left
    if y < dimY and x > 0:
        adjList.append(checkAdjacent((x - 1, y + 1), level, True))
    #left
    if x > 0:
        adjList.append(checkAdjacent((x - 1, y), level))
   
    while None in adjList:
        adjList.remove(None)

    #print('adjList: ', adjList)

    return adjList
    

def test_route(filename, src_waypoint, dst_waypoint):
    """ Loads a level, searches for a path between the given waypoints, and displays the result.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        dst_waypoint: The character associated with the destination waypoint.

    """

    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source and destination coordinates from the level.
    src = level['waypoints'][src_waypoint]
    dst = level['waypoints'][dst_waypoint]

    # Search for and display the path from src to dst.
    path = dijkstras_shortest_path(src, dst, level, navigation_edges)
    if path:
        show_level(level, path)
    else:
        print("No path possible!")


def cost_to_all_cells(filename, src_waypoint, output_filename):
    """ Loads a level, calculates the cost to all reachable cells from 
    src_waypoint, then saves the result in a csv file with name output_filename.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        output_filename: The filename for the output csv file.

    """
    
    # Load and display the level.
    level = load_level(filename)
    show_level(level)


    # Retrieve the source coordinates from the level.
    src = level['waypoints'][src_waypoint]
    
    # Calculate the cost to all reachable cells from src and save to a csv file.
    costs_to_all_cells = dijkstras_shortest_path_to_all(src, level, navigation_edges)
    save_level_costs(level, costs_to_all_cells, output_filename)


if __name__ == '__main__':

    filename, src_waypoint, dst_waypoint = 'example.txt', 'a','d'

    level = load_level(filename)
    src = level['waypoints'][src_waypoint]
    dst = level['waypoints'][dst_waypoint]

    #path = dijkstras_shortest_path(src, dst, level, navigation_edges)

    # Use this function call to find the route between two waypoints.
    #test_route(filename, src_waypoint, dst_waypoint)



    # Use this function to calculate the cost to all reachable cells from an origin point.
    cost_to_all_cells(filename, src_waypoint, 'my_costs.csv')
