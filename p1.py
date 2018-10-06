from p1_support import load_level, show_level, save_level_costs, save_level
from math import inf, sqrt
from heapq import heappop, heappush, heapify


def dijkstras_shortest_path(initial_position, destination, graph, adj):
    """ Searches for a minimal cost path through a graph using Dijkstra's algorithm.
    Args:
        initial_position: The initial cell from which the path extends.
        destination: The end location for the path.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.
    Returns:
        If a path exits, return a list containing all cells from initial_position to destination.
        Otherwise, return None.
    """
    #initial_position = (initial_position, 0)
    queue = [(0, initial_position)]
    dist = {initial_position : 0}
    prev = {}

    while queue:
        current_cost, current_cell = heappop(queue)

        if current_cell == destination:
            path = []
            n = destination
            while n in prev:
                path.insert(0, prev[n])
                n =  prev[n]
            path.append(destination)
            return path
        else:
            for adj_cell, adj_cost in adj(graph, current_cell):
                alt = dist[current_cell] + adj_cost
                if adj_cell not in dist or alt < dist[adj_cell]:
                    prev[adj_cell] = current_cell
                    dist[adj_cell] = alt
                    heappush(queue, (alt, adj_cell))
    return(-1) 


def dijkstras_shortest_path_to_all(initial_position, level, adj):
    """ Calculates the minimum cost to every reachable cell in a graph from the initial_position.
		Args:
        initial_position: The initial cell from which the path extends.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.
		Returns:
        A dictionary, mapping destination cells to the cost of a path from the initial_position.
		"""
    
    #to_return is a dictionary of costs
    to_return = {initial_position: 0}
    
    #populate the set of all possible (non-wall) destinations in a list called unvisited
    unvisited = list(level['spaces'])

    while unvisited:
        #get next cell and the path to it
        next_cell = unvisited.pop()
        path = dijkstras_shortest_path(initial_position, next_cell, level, adj)

        #get the accumulated cost of each node in the path
        total_cost = 0
        prev = initial_position
        for node in path:
            if node in level['walls']:
                total_cost = inf
                break
            elif node != initial_position:
                total_cost += do_math(level, prev, node)
            prev = node

        #put it in the dictionary
        to_return[next_cell] = total_cost

    return to_return

def do_math(level, from_cell, to_cell):
    xf, yf = from_cell
    xt, yt = to_cell

    from_cost = level['spaces'][from_cell]
    to_cost = level['spaces'][to_cell]

    if xf==xt or yf==yt:
        cost = (from_cost+to_cost) * 0.5
    else:
        cost = (from_cost+to_cost) * (0.5 * sqrt(2))

    return cost


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
        if cell in level['spaces']:
            startCell = (cell, level['spaces'][cell])
        if cell in level['walls']:
            startCell = (cell, inf)

        if coords in level['spaces'] and not diagonal:
            return (coords, level['spaces'][coords] * 0.5 + startCell[1] * 0.5)
        elif coords in level['spaces'] and diagonal:
            adj =  (coords, level['spaces'][coords])
            if adj != None:
                return (adj[0], adj[1] * sqrt(2) * 0.5 + startCell[1] * sqrt(2) * 0.5)
        elif coords in level['walls']:
            return (coords, inf)
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
    # Load and display the level.
    level = load_level('example.txt')
    show_level(level)
    
    # Retrieve the source coordinates from the level.
    src = level['waypoints']['a']
    print(src)
    print(level)
    destination = level['waypoints']['e']

    path = dijkstras_shortest_path(src, destination, level, navigation_edges)
    show_level(level, path)
    
    #save_level('path_file.txt', level, path)
    
    #filename, src_waypoint, dst_waypoint = 'my_maze.txt', 'a','e'

    # Use this function call to find the route between two waypoints.
    #test_route(filename, src_waypoint, dst_waypoint)

    # Use this function to calculate the cost to all reachable cells from an origin point.
    cost_to_all_cells(filename, src_waypoint, 'my_costs.csv')
