import numpy as np
import time
data = np.loadtxt('input.txt',delimiter=',').astype(int)

def to_string(array_to_transform): #[1240] --> ['1','2','4','0']
    return [i for i in str(array_to_transform)]

def divide_chunks(original_data,n):
    i=0
    while i < len(original_data):
        string=to_string(original_data[i])
        if int(string[-1])==4 or int(string[-1])==3: #check if last element of instruction opcode is a 3 or 4 
            yield original_data[i : i+2]
            i=i+2
        else:
            yield original_data[i : i+n]
            i=i+n

def prepare_instruction(instruction):
    instruction_opcode_str=to_string(instruction[0])
    m3, m2,m1,temp1,temp2 = ['0']*(5-len(instruction_opcode_str)) + instruction_opcode_str #in case some parameter modes missing fill with 0s
    opcode=''.join([temp1,temp2])

    return int(opcode),int(m1),int(m2),int(m3)


def add_function(m1,m2, instruction):
    value1 = data[instruction[1]] if m1==0 else instruction[1]
    value2 = data[instruction[2]] if m2 ==0 else instruction[2]
    number = value1 + value2
    data[instruction[3]]=number


def multiply_function(m1,m2,instruction):
    value1 = data[instruction[1]] if m1==0 else instruction[1]
    value2 = data[instruction[2]] if m2 ==0 else instruction[2]
    number = value1 * value2
    data[instruction[3]]=number

def input_function(instruction):
    the_input=input('Provide me an input (give a 1): ')
    data[instruction[1]]=int(the_input)

def output_function(m1,instruction):

    return data[instruction[1]] if m1==0 else data[1] 

#Replace values of data:
n = 4
chunked_data = divide_chunks(data,n) #chunked data is a generator. We can only iterate over it once ! If want to remove this constraint, get it into a list first (list(chunked_data))
for instruction in chunked_data:
    opcode, m1, m2, m3 = prepare_instruction(instruction)
    if opcode==99:
        break
    elif opcode==1:
        add_function(m1, m2, instruction)
    elif opcode==2:
        multiply_function(m1, m2, instruction)
    elif opcode==3:
        input_function(instruction)
    elif opcode==4:
        output = output_function(m1, instruction)
        print('output:',output)

    else:
        print('No valid opcode')
        raise ValueError
    



