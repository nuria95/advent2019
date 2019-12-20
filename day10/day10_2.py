#Note: For representing lines we express asteroid as points in a 2d plane, as [x,y]. x-axis positive to the right, y-axis positive down.
import numpy as np
import pandas as pd
from itertools import combinations
from collections import namedtuple
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

asteroid_pos = list(np.where(data == 1)) # [y,x]
list_asteroids_pos = []
for p1 in zip(asteroid_pos[0],asteroid_pos[1]):
    list_asteroids_pos.append(list(reversed(p1))) # [x,y]!


Asteroid_Data = namedtuple('Asteroid', 'pos m quadrant')
asteroids_data = []
station_position = [25,31] # [x,y] from prev exercise. Viewing 329 asteroids.
p1 = station_position
asteroids_to_remove = []
for p2 in list_asteroids_pos:
    if p2 == station_position:
        continue
    m, xint, yint= compute_line(p1,p2)
    dist = compute_dist(p1,p2)
    quadrant = compute_quadrant(p1,p2)
    obstacle = others_in_line(m,xint,yint, p1, p2, dist, quadrant)
    if not obstacle:
        asteroid = Asteroid_Data(pos=p2,
                                    m=m,
                                    quadrant=quadrant)
        asteroids_data.append(asteroid)

quad1_4 = [a for a in asteroids_data if a.quadrant == 1 or a.quadrant == 4] #select asteroids in quadrant 1 and 4
quad1_4_sorted = sorted(quad1_4, key=lambda x: x.m) # start at slope -inf till slope + inf

quad3_2 = [a for a in asteroids_data if a.quadrant == 3 or a.quadrant == 2] #select asteroids in quadrant 3 and 2
quad3_2_sorted = sorted(quad3_2, key=lambda x: x.m) # start at slope -inf till slope + inf
ordered_asteroids_clockwise = quad1_4_sorted + quad3_2_sorted

print('200th asteroid to be vaporized is',ordered_asteroids_clockwise[200-1]) # position is already [x,y] :)