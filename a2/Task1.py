import AStar
import Map

#Task 1
print('Results from task 1')
map1 = Map.Map_Obj(1)

print('start1:')
print(map1.start_pos)
print('goal1:')
print(map1.goal_pos)

#Show map before shortest path
map1.show_map()

path = AStar.astar(map1, map1.start_pos, map1.goal_pos, AStar.heuristic_bad)
print('Length of path')
print(len(path))

#Add path to map and show it
for pos in path:
    map1.replace_map_values(pos, 2, map1.goal_pos)

map1.show_map()
