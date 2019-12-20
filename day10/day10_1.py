#Note: For representing lines we express asteroid as points in a 2d plane, as [x,y]. x-axis positive to the right, y-axis positive down.
import numpy as np
import pandas as pd
from itertools import combinations
import time
t=time.time()
df = pd.read_csv('input.txt',sep='\t', header = None)
m=[]
for row in range(df.shape[0]):
    d = [1 if i=='#' else 0 for i in df[0][row]]
    m.append(d)
data = np.array(m)

def compute_dist(p1,p2):
    # Compute euclidean dist between two points
    dist = np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
    return dist

def compute_line(p1,p2): 
    # Compute slope and intercepts.
    if p2[0]-p1[0] !=0: # if not vertical line
        m = (p2[1]-p1[1])/(p2[0]-p1[0]) # slope of line
    else:
        if p2[1]-p1[1] > 0:
            m = np.inf
        else:
            m = -np.inf

    xint = p1[0] # offset
    yint = p1[1] # offset
    return m, xint, yint

def compute_quadrant(p1,p2):
    if p2[0]-p1[0]>=0: # x2 >= x1
        if p2[1] - p1[1] <= 0: # y2 <= y1
            quadrant = 1
        else:
            quadrant = 4
    else:
        if p2[1] - p1[1] <= 0: # y2 <= y1
            quadrant = 2
        else:
            quadrant = 3
    return quadrant


def others_in_line(m,xint,yint, p1, p2, dist, quadrant):
    for col,row in zip(asteroid_pos[1],asteroid_pos[0]): # col = x, row = y
        if [col,row] != p1 and [col,row] != p2:
            p3 = [col,row]
        else:
            continue
        p3_in_line = p3[1] == m*(p3[0] - xint) + yint if np.abs(m) != np.inf else xint == p3[0]
        if p3_in_line:
            if compute_quadrant(p1,p3) == quadrant:
                if compute_dist(p1,p3) < dist:
                    return True
    return False

final_matrix = np.zeros_like(data)
asteroid_pos = list(np.where(data == 1)) # [y,x] !
list_asteroids_pos = []
for p1 in zip(asteroid_pos[0],asteroid_pos[1]):
    list_asteroids_pos.append(list(p1))
possible_combs = list(combinations(list_asteroids_pos,2)) #list of (asteroid1,asteroid2), (asteroid1,asteroid3) ... (asteroid3,asteroid4)
print('Number of combinations',len(possible_combs))

num_pairs = 0
for pair in possible_combs:
    # print(num_pairs)
    p1=list(reversed(pair[0])) # read revrese way --> p1= [x, y]
    p2=list(reversed(pair[1])) # read revrese way --> p2= [x, y]
    m, xint, yint= compute_line(p1,p2)
    dist = compute_dist(p1,p2)
    quadrant = compute_quadrant(p1,p2)
    obstacle = others_in_line(m,xint,yint, p1, p2, dist, quadrant)
    if not obstacle:
        final_matrix[p1[1],p1[0]] += 1 
        final_matrix[p2[1],p2[0]] += 1 
    num_pairs +=1

#Transpose for notation:
print('Best view', np.where(final_matrix == np.max(final_matrix))[1], np.where(final_matrix == np.max(final_matrix))[0], 'viewing ',np.max(final_matrix), 'asteroids' )
print('Elapsed time', time.time()-t)