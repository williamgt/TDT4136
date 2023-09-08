import AStar
import Map

map = Map.Map_Obj(1)

#map.print_map(map.str_map)
#map.print_map(map.int_map)

print(map.int_map.shape)
print(map.start_pos)
print(map.goal_pos)
print(map.get_cell_value(map.start_pos))

#Very unfinished heuristic function
def heuristic(tuple):
    return 0

map.show_map()

path = AStar.astar(map, map.start_pos, map.goal_pos, heuristic)
print(path)
print(len(path))

for pos in path:
    map.replace_map_values(pos, 2, map.goal_pos)

map.show_map()

