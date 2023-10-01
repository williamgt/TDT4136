import AStar
import Map

#Task 2
print('Results from task 2')
map2 = Map.Map_Obj(2)

print('start2:')
print(map2.start_pos)
print('goal2:')
print(map2.goal_pos)

#Show map before shortest path
map2.show_map()

path = AStar.astar(map2, map2.start_pos, map2.goal_pos, AStar.manhatten)
print('Length of path')
print(len(path))

#Add path to map and show it
for pos in path:
    map2.replace_map_values(pos, 2, map2.goal_pos)

map2.show_map()
