import AStar
import Map

#Task 3
print('Results from task 3')
map3 = Map.Map_Obj(3)

print('start3:')
print(map3.start_pos)
print('goal3:')
print(map3.goal_pos)


#Show map before shortest path
map3.show_map()

path = AStar.astar(map3, map3.start_pos, map3.goal_pos, AStar.euclidean)
print('Length of path')
print(len(path))
print('Cost of path:')
print(AStar.path_cost(map3, path))

#Add path to map and show it
for pos in path:
    map3.replace_map_values(pos, 2, map3.goal_pos)

map3.show_map()
