import numpy as np
import time
import copy
from itertools import product
data_original = np.loadtxt('input.txt',delimiter=',').astype(int)

def divide_chunks(original_data,n):
    for i in range(0,len(original_data),n):
        yield original_data[i : i+n]

def add_function(instruction):
    number = data[instruction[1]]+data[instruction[2]]
    data[instruction[3]]=number

def multiply_function(instruction):
    number = data[instruction[1]]*data[instruction[2]]
    data[instruction[3]]=number


n = 4
output = 0
goal = 19690720

perm = list(product(np.arange(0,100), repeat=2))

output=0
i=0
while output != goal:
    data= data_original.copy() 
    data[1]=perm[i][0]
    data[2]=perm[i][1]
    chunked_data = list(divide_chunks(data,n))

    for instruction in chunked_data:
        if instruction[0]==99:
            break
        elif instruction[0]==1:
            add_function(instruction)

        elif instruction[0]==2:
            multiply_function(instruction)

    output = data[0]
    i = i+1

print('output:',data[0], 'noun:',data[1],'verb:',data[2])

