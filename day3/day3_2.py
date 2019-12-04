import numpy as np
data = np.loadtxt('input.txt', delimiter=',', dtype=np.str)
class Movement(object):
    def __init__(self):
        self.position = [0, 0]
        self.final_trajectory = [[0,0]]

    def __call__(self, code):
        method_name = code[0]  # first element of string
        method = getattr(self, method_name, lambda: 'Invalid')
        return method(code[1::])
    
    def fill_trajectory(self,last_pos,next_pos, move_type):
        if move_type == 'U' or move_type == 'D':
            # change in x (consdering (position = [x,y]))
            order = 1 if move_type=='D' else -1 # to increase or decrease range()
            for x in range(last_pos[0] + order,next_pos[0],order):
                to_add = [x, next_pos[1]]
                self.final_trajectory.append(to_add[:])

        else: # if move_type == 'L' or 'R'
            # change in y (consdering (position = [x,y]))
            order = 1 if move_type=='R'  else -1 # to increase or decrease range()  
            for y in range(last_pos[1]+order,next_pos[1],order):
                to_add = [next_pos[0], y]
                self.final_trajectory.append(to_add[:])

    def R(self, steps):
        last_position = self.position[:]
        self.position[1] = self.position[1] + int(steps)
        self.fill_trajectory(last_position,self.position, move_type = 'R')
        self.final_trajectory.append(self.position[:]) # add next pos since it is not included in range
    def L(self, steps):
        last_position = self.position[:]
        self.position[1] = self.position[1] - int(steps)
        self.fill_trajectory(last_position,self.position, move_type = 'L')
        self.final_trajectory.append(self.position[:])# add next pos since it is not included in range
    def U(self, steps):
        last_position = self.position[:]
        self.position[0] = self.position[0] - int(steps)
        self.fill_trajectory(last_position,self.position, move_type = 'U')
        self.final_trajectory.append(self.position[:]) # add next pos since it is not included in range
    def D(self, steps):
        last_position = self.position[:]
        self.position[0] = self.position[0] + int(steps)
        self.fill_trajectory(last_position,self.position,move_type = 'D')
        self.final_trajectory.append(self.position[:]) # add next pos since it is not included in range

line1 = Movement()
line2 = Movement()
for action1,action2 in zip(data[0,:],data[1,:]):
    #Move line 1
    line1(action1)
    line2(action2)
    
trajectory1 = line1.final_trajectory
trajectory2 = line2.final_trajectory


#Shitty way of getting tuples to compute intersection
new_traj1 = []
new_traj2 = []
for i in trajectory1:
    new_traj1.append(tuple(i))
for i in trajectory2:
    new_traj2.append(tuple(i))

traj1=tuple(new_traj1)
traj2 = tuple(new_traj2)
intersections = list(set(traj1).intersection(traj2))
total_steps1=[]
total_steps2 =[]
for i in intersections[1:]: # do not account for initial intersect
    steps1 = traj1.index(i)
    
    if len([steps1])>1:
        steps1=steps1[0]
    
    total_steps1.append(steps1)

    steps2 = traj2.index(i)
    if len([steps2])>1:
        steps2=steps2[0]
    total_steps2.append(steps2)


sum_steps = np.array(total_steps1) + np.array(total_steps2)
min_sum_steps = min(val for val in sum_steps if val >0)

print('Minimum combined steps is',min_sum_steps)