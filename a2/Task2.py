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
    return 1
