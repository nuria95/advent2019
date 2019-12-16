import numpy as np
import time
from itertools import permutations
import matplotlib.pyplot as plt

data = open("input.txt").read()
width = 25
tall = 6
matrix = np.zeros((tall,width))
Total_matrix = None
row = 0
for y in range(0,len(data)+1,width):
    if y+width > len(data):
        break
    matrix[row,:] = list(map(int, data[y:y+width])) #convert to ints
    row = row + 1
    if row > tall-1:
        if Total_matrix is None:
            Total_matrix = matrix
        else:   
            Total_matrix = np.dstack((Total_matrix,matrix))
        row = 0  
        matrix = np.zeros((tall,width)) 

Total_matrix = np.transpose(Total_matrix, (2, 0, 1)) # tranpose to [num_layers, tall, width]

Final_image = np.zeros((tall,width))
for x in range(tall):
    for y in range(width):
        color = 2
        z=-1
        while color ==2:
            z = z+1
            color = Total_matrix[z,x,y]
            
        Final_image[x,y]=Total_matrix[z,x,y]


plt.imshow(Final_image)
plt.show()
