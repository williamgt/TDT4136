import math
import AStar
import Map

#Task 2
print('Results from task 2')
map2 = Map.Map_Obj(2)

print('start2:')
print(map2.start_pos)
print('goal2:')
print(map2.goal_pos)

def heuristic_2(current, goal):
    return 0

def manhatten(current, goal):
    """Returns the manhatten distance between given coordinate and goal"""
    return abs(current[0]-goal[0]) + abs(current[1]-goal[1])

def euclidean(current, goal):
    """Returns the euclidean distance between given coordinate and goal"""
    return math.sqrt((goal[0]-current[0])**2 + (goal[1]-current[1])**2)

#Show map before shortest path
map2.show_map()

path = AStar.astar(map2, map2.start_pos, map2.goal_pos, euclidean)
print('Length of path')
print(len(path))

#Add path to map and show it
for pos in path:
    map2.replace_map_values(pos, 2, map2.goal_pos)

map2.show_map()
