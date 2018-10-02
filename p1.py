from p1_support import load_level, show_level, save_level_costs
from math import inf, sqrt
from heapq import heappop, heappush


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
    queue = [initial_position]
    while queue:
        current_node = queue[0]
        if current_node == destination:
            return path_to(destination, graph)
        else:
            for new in adj(current_node, graph):
                if new.prev == None:
                    new.prev = current_node
                    queue.insert(0, new)
    return(-1)

def path_to(destination, graph):
    path = []
    current_node = destination
    while current_node.prev:
        path.insert(0, current_node.prev)
        current_node = current_node.prev
    return path


def dijkstras_shortest_path_to_all(initial_position, graph, adj):
    """ Calculates the minimum cost to every reachable cell in a graph from the initial_position.

    Args:
        initial_position: The initial cell from which the path extends.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        A dictionary, mapping destination cells to the cost of a path from the initial_position.
    """

    return {}


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

    #each navigable cell in a level is stored in a dictionary within the level object called spaces.
    #the dictionary uses a tuple representing cartesian coordinates (x, y) as the key, and
    #the weight of the edge as the value.

    #Look up the cell in level['spaces'] 
    #use some math to get the cells above, below, right, and left of the current cell, 
    #and all the diagonals
    #return a list of tuples of the form ((x, y), weight)

    #get the dimensions of the level
    dimX = 0
    dimY = 0

    for wall in level['walls']:
        if(dimX < wall[0]):
            dimX = wall[0]
        if(dimY < wall[1]):
            dimY = wall[1]

    adjList = ()
    #top-left
    if cell[0] > 1 and cell[1] > 1:
        adjCell = level['spaces'][(cell[0] - 1, cell[1] - 1)]
        adjList += ((adjCell[0][0], adjCell[0][1]), adjCell[1])
    #above
    if cell[1] > 1:
        adjCell = level['spaces'][(cell[0],cell[1] - 1)]
        adjList += ((adjCell[0][0], adjCell[0][1]), adjCell[1])
    #top-right
    if cell[0] < dimX and cell[1] > 1:
        adjCell = level['spaces'][(cell[0] + 1, cell[1] - 1)]
        adjList += ((adjCell[0][0], adjCell[0][1]), adjCell[1])
    #right
    if cell[0] < dimX:
        adjCell = level['spaces'][(cell[0] + 1, cell[1])]
        print(adjCell)
        adjList += ((adjCell[0][0], adjCell[0][1]), adjCell[1])
    #bottom-right
    if cell[1] < dimY and cell[0] < dimX:
        adjCell = level['spaces'][(cell[0] + 1, cell[1] + 1)]
        adjList += ((adjCell[0][0], adjCell[0][1]), adjCell[1])
    #below
    if cell[1] < dimY:
        adjCell = level['spaces'][(cell[0],cell[1] + 1)]
        adjList += ((adjCell[0][0], adjCell[0][1]), adjCell[1])
    #bottom-left
    if cell[1] < dimY and cell[0] > 1 :
        adjCell = level['spaces'][(cell[0] - 1, cell[1] + 1)]
        adjList += ((adjCell[0][0], adjCell[0][1]), adjCell[1])
    #left
    if cell[0] > 1:
        adjCell =level['spaces'][(cell[0] - 1, cell[1])]
        adjList += ((adjCell[0][0], adjCell[0][1]), adjCell[1])
   
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
    print(level)
    destination = level['waypoints']['b']

    print(dijkstras_shortest_path(src, destination, level, navigation_edges))
    #filename, src_waypoint, dst_waypoint = 'example.txt', 'a','e'

    # Use this function call to find the route between two waypoints.
    #test_route(filename, src_waypoint, dst_waypoint)

    # Use this function to calculate the cost to all reachable cells from an origin point.
    #cost_to_all_cells(filename, src_waypoint, 'my_costs.csv')
