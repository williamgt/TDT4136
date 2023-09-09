import sys


def astar(map, start, goal, h):
    """
    Based implementation on this https://en.wikipedia.org/wiki/A*_search_algorithm
    """
    discovered = set() #Discovered nodes, should be a pq
    discovered.add(tuple(start))
    cameFrom = dict() #A dictionary of the nodes that preceeded the nth node

    gScore = inf_dict(map.int_map.shape) #Cost of cheapest path from start to n
    gScore[tuple(start)] = 0 #Does not cost anything from start to start
    
    fScore = inf_dict(map.int_map.shape) #Sum of g and f, used when deciding path
    fScore[tuple(start)] = h(start, goal)

    while len(discovered):
        current = lowest_f_score(discovered, fScore)
        #print(current)
        if current == tuple(goal):
            return path(cameFrom, current)
        
        discovered.remove(current)

        neighborsToCurrent = get_neighbors(map.int_map, current[0], current[1], include_diagonals=False)
        #print(neighborsToCurrent)

        for n in neighborsToCurrent:
            tentative_gScore = gScore[current] + map.int_map[n]
            #print(tentative_gScore)
            if tentative_gScore < gScore[n]:
                cameFrom[n] = current
                gScore[n] = tentative_gScore
                fScore[n] = tentative_gScore + h(n, goal)
                if n not in discovered:
                    discovered.add(n)

    return -1

def path(came_from, current):
    totalPath = [current]
    while current in came_from.keys():
        current = came_from[current]
        totalPath = [current] + totalPath
    return totalPath

def inf_dict(shape):
    """Creates a dictionary with given shape containing only large values"""
    dictionary = dict()
    for i in range(shape[0]):
        for j in range(shape[1]):
            dictionary[tuple([i, j])] = sys.maxsize
    return dictionary

def lowest_f_score(discovered, fScore):
    """
    Should return the tuple in discovered which has the lowest fScore.
    Something wrong happened if returning (-1,-1). 
    NB! Could rather create a pq than using this function on the 'discovered' set.
    """
    min = sys.maxsize
    returnVal = (-1,-1)
    for val in discovered:
        if fScore[val] < min:
            min = fScore[val]
            returnVal = val
    return returnVal

def neighbors(map, row_number, column_number, radius=1):
     """From https://stackoverflow.com/questions/22550302/find-neighbors-in-a-matrix"""
     return [[map[i][j] if  i >= 0 and i < len(map) and j >= 0 and j < len(map[0]) else 0
                for j in range(column_number-1-radius, column_number+radius)]
                    for i in range(row_number-1-radius, row_number+radius)]

def get_neighbors(matrix, row, col, include_diagonals=False):
    """
    Gets all the neighboring coordinates for a given coordinate in a matrix 
    excluding where the value is -1 (assumed to be a wall)
    """
    neighbors = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    if include_diagonals:
        directions.extend([(1, 1), (-1, -1), (1, -1), (-1, 1)])

    rows, cols = len(matrix), len(matrix[0])

    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < rows and 0 <= c < cols and matrix[r][c] != -1:
            neighbors.append((r, c))

    return neighbors