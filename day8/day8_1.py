import numpy as np
import time
from itertools import permutations

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

num_layers = Total_matrix.shape[0]
min_num_zeros = tall*width # max num zeros possible
for layer in range(num_layers):
    zeros_in_layer = np.sum(Total_matrix[layer, : ,:]==0)
    if zeros_in_layer<min_num_zeros:
        min_num_zeros = zeros_in_layer
        layer_min_zeros = layer
matrix = Total_matrix[layer_min_zeros, : ,:]
print('Result',np.sum(matrix==1) * np.sum(matrix ==2))
