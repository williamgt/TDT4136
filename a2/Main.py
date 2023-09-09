import AStar
import Map

map = Map.Map_Obj(1)

#map.print_map(map.str_map)
#map.print_map(map.int_map)

print(map.int_map.shape)
print('start ' + map.start_pos)
print('goal ' + map.goal_pos)

#Very unfinished heuristic function
def heuristic_1(current, goal):
    return 0

#Show map before shortest path
map.show_map()

path = AStar.astar(map, map.start_pos, map.goal_pos, heuristic_1)
#print(path)
#print(len(path))

#Add path to map and show it
for pos in path:
    map.replace_map_values(pos, 2, map.goal_pos)

map.show_map()

