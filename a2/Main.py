import AStar
import Map

map1 = Map.Map_Obj(1)

#map.print_map(map.str_map)
#map.print_map(map.int_map)

#print(map1.int_map.shape)
print('start1:')
print(map1.start_pos)
print('goal1:')
print(map1.goal_pos)

#Very unfinished heuristic function
def heuristic_1(current, goal):
    return 0

#Show map before shortest path
map1.show_map()

path = AStar.astar(map1, map1.start_pos, map1.goal_pos, heuristic_1)
#print(path)
#print(len(path))

#Add path to map and show it
for pos in path:
    map1.replace_map_values(pos, 2, map1.goal_pos)

map1.show_map()

