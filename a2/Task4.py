import AStar
import Map

#Task 4
print('Results from task 4')
map4 = Map.Map_Obj(4)

print('start4:')
print(map4.start_pos)
print('goal4:')
print(map4.goal_pos)


#Show map before shortest path
map4.show_map()

path = AStar.astar(map4, map4.start_pos, map4.goal_pos, AStar.manhatten)
print('Length of path')
print(len(path))
print('Cost of path:')
print(AStar.path_cost(map4, path))

#Add path to map and show it
for pos in path:
    map4.replace_map_values(pos, 2, map4.goal_pos)

map4.show_map()
