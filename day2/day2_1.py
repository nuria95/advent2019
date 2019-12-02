import numpy as np
import time
data = np.loadtxt('input.txt',delimiter=',').astype(int)

def divide_chunks(original_data,n):
    for i in range(0,len(original_data),n):
        yield original_data[i : i+n]

def add_function(instruction):
    number = data[instruction[1]]+data[instruction[2]]
    data[instruction[3]]=number


def multiply_function(instruction):
    number = data[instruction[1]]*data[instruction[2]]
    data[instruction[3]]=number

#Replace values of data:
data[1]=12
data[2]=2
# data = np.array([1,1,1,4,99,5,6,0,99])
n = 4
chunked_data = list(divide_chunks(data,n))
for instruction in chunked_data:
    if instruction[0]==99:
        break
    elif instruction[0]==1:
        
        add_function(instruction)
    elif instruction[0]==2:
       
        multiply_function(instruction)

print(data)

#Solution:4138687