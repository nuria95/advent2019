import numpy as np
import time
data = np.loadtxt('input.txt',delimiter=',').astype(int)

def to_string(array_to_transform): #[1240] --> ['1','2','4','0']
    return [i for i in str(array_to_transform)]

def get_data(data,pointer):
    string=to_string(data[pointer])
    if int(string[-1])==4 or int(string[-1])==3: #check if last element of instruction opcode is a 3 or 4 
        length_instr = 2
    else:
        length_instr = 4  
    return data[pointer:pointer+length_instr]

def prepare_instruction(instruction):
    instruction_opcode_str=to_string(instruction[0])
    m3, m2,m1,temp1,temp2 = ['0']*(5-len(instruction_opcode_str)) + instruction_opcode_str #in case some parameter modes missing fill with 0s
    opcode=''.join([temp1,temp2])

    return int(opcode),int(m1),int(m2),int(m3)


def add_function(m1,m2, instruction,pointer):
    value1 = data[instruction[1]] if m1==0 else instruction[1]
    value2 = data[instruction[2]] if m2 ==0 else instruction[2]
    number = value1 + value2
    data[instruction[3]]=number
    pointer=pointer+4
    return pointer


def multiply_function(m1,m2,instruction,pointer):
    value1 = data[instruction[1]] if m1==0 else instruction[1]
    value2 = data[instruction[2]] if m2 ==0 else instruction[2]
    number = value1 * value2
    data[instruction[3]]=number
    pointer=pointer+4
    return pointer

def input_function(instruction,pointer):
    the_input=input('Provide me an input (give a 5): ')
    data[instruction[1]]=int(the_input)
    pointer=pointer+2
    return pointer

def output_function(m1,instruction,pointer):
    pointer=pointer+2
    return data[instruction[1]] if m1==0 else data[1], pointer

def jump_if_true(m1,m2,instruction,pointer):
    parameter1 = data[instruction[1]] if m1==0 else instruction[1]
    parameter2 = data[instruction[2]] if m2==0 else instruction[2]
    if parameter1!=0:
        pointer = parameter2
    else:
        pointer = pointer + 3
    return pointer

def jump_if_false(m1,m2,instruction,pointer):
    parameter1 = data[instruction[1]] if m1==0 else instruction[1]
    parameter2 = data[instruction[2]] if m2==0 else instruction[2]
    if parameter1==0:
        pointer = parameter2
    else:
        pointer = pointer + 3
    return pointer

def less_than(m1,m2,instruction,pointer):
    parameter1 = data[instruction[1]] if m1==0 else instruction[1]
    parameter2 = data[instruction[2]] if m2==0 else instruction[2]
    if parameter1<parameter2:
        data[instruction[3]]=1
    else:
        data[instruction[3]]=0
    pointer = pointer + 4
    return pointer

def equals_than(m1,m2,instruction,pointer):
    parameter1 = data[instruction[1]] if m1==0 else instruction[1]
    parameter2 = data[instruction[2]] if m2==0 else instruction[2]
    if parameter1==parameter2:
        data[instruction[3]]=1
    else:
        data[instruction[3]]=0
    pointer = pointer + 4
    return pointer


pointer = 0
# data=[103,3,1105,-1,9,1101,0,0,12,4,12,99,1]
while True:
    
    instruction = get_data(data,pointer)
    # print('Instruction',instruction)
    opcode, m1, m2, m3 = prepare_instruction(instruction)
    # print(opcode, m1, m2, m3)
    if opcode==99:
        print('End!')
        break
    elif opcode==1:
        pointer = add_function(m1, m2, instruction, pointer)
    elif opcode==2:
        pointer = multiply_function(m1, m2, instruction, pointer)
    elif opcode==3:
        pointer = input_function(instruction, pointer)
    elif opcode==4:
        output, pointer = output_function(m1, instruction, pointer)
        print('output:',output) 
       
    elif opcode==5:
        pointer = jump_if_true(m1,m2,instruction, pointer)
    elif opcode==6:
        pointer = jump_if_false(m1,m2,instruction, pointer)
    elif opcode==7:
        pointer = less_than(m1,m2,instruction, pointer)
    elif opcode==8:
        pointer = equals_than(m1,m2,instruction, pointer)
    

    else:
        print('No valid opcode')
        raise ValueError



