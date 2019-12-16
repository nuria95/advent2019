import numpy as np
import time
data = np.loadtxt('input.txt',delimiter=',').astype(int)
data = np.append(data,np.zeros((100000,1),dtype=int))
def to_string(array_to_transform): #[1240] --> ['1','2','4','0']
    return [i for i in str(array_to_transform)]

def get_data(data,pointer):
    string=to_string(data[pointer])
    if int(string[-1])==4 or int(string[-1])==3 or int(string[-1])==9: #check if last element of instruction opcode is a 3 or 4 or 9
        length_instr = 2
    else:
        length_instr = 4  
    return data[pointer:pointer+length_instr]

def prepare_instruction(instruction):
    instruction_opcode_str=to_string(instruction[0])
    m3, m2,m1,temp1,temp2 = ['0']*(5-len(instruction_opcode_str)) + instruction_opcode_str #in case some parameter modes missing fill with 0s
    opcode=''.join([temp1,temp2])

    return int(opcode),int(m1),int(m2),int(m3)


def add_function(m1,m2,m3, instruction,pointer,offset):
    value1 = data[instruction[1]] if m1==0 else instruction[1] if m1==1 else data[instruction[1]+offset]
    value2 = data[instruction[2]] if m2 ==0 else instruction[2] if m2==1 else data[instruction[2]+offset]
    position = instruction[3] if m3==0 else (instruction[3]+offset)
    number = value1 + value2
    data[position]=number
    pointer=pointer+4
    return pointer


def multiply_function(m1,m2,m3,instruction,pointer,offset):
    value1 = data[instruction[1]] if m1==0 else instruction[1] if m1==1 else data[instruction[1]+offset]
    value2 = data[instruction[2]] if m2 ==0 else instruction[2] if m2==1 else data[instruction[2]+offset]
    number = value1 * value2
    position = instruction[3] if m3==0 else (instruction[3]+offset)
    data[position]=number
    pointer=pointer+4
    return pointer

def input_function(m1, instruction,pointer,offset):
    the_input=input('Provide me an input (give a 2): ')
    position = instruction[1] if m1==0 else (instruction[1]+offset)
    data[position]=int(the_input)
    pointer=pointer+2
    return pointer

def output_function(m1,instruction,pointer,offset):
    pointer=pointer+2
    output = data[instruction[1]] if m1==0 else data[1] if m1==1 else data[instruction[1]+offset]
    return output, pointer

def jump_if_true(m1,m2,instruction,pointer,offset):
    parameter1 = data[instruction[1]] if m1==0 else instruction[1] if m1==1 else data[instruction[1]+offset]
    parameter2 = data[instruction[2]] if m2==0 else instruction[2] if m2==1 else data[instruction[2]+offset]
    if parameter1!=0:
        pointer = parameter2
    else:
        pointer = pointer + 3
    return pointer

def jump_if_false(m1,m2,instruction,pointer,offset):
    parameter1 = data[instruction[1]] if m1==0 else instruction[1] if m1==1 else data[instruction[1]+offset]
    parameter2 = data[instruction[2]] if m2==0 else instruction[2] if m2==1 else data[instruction[2]+offset]
    if parameter1==0:
        pointer = parameter2
    else:
        pointer = pointer + 3
    return pointer

def less_than(m1,m2,m3,instruction,pointer,offset):
    parameter1 = data[instruction[1]] if m1==0 else instruction[1] if m1==1 else data[instruction[1]+offset]
    parameter2 = data[instruction[2]] if m2==0 else instruction[2] if m2==1 else data[instruction[2]+offset]
    position = instruction[3] if m3==0 else (instruction[3]+offset)
    if parameter1<parameter2:
        data[position]=1
    else:
        data[position]=0
    pointer = pointer + 4
    return pointer

def equals_than(m1,m2,m3,instruction,pointer,offset):
    parameter1 = data[instruction[1]] if m1==0 else instruction[1] if m1==1 else data[instruction[1]+offset]
    parameter2 = data[instruction[2]] if m2==0 else instruction[2] if m2==1 else data[instruction[2]+offset]
    position = instruction[3] if m3==0 else (instruction[3]+offset)
    if parameter1==parameter2:
        data[position]=1
    else:
        data[position]=0
    pointer = pointer + 4
    return pointer

def change_offset(m1, instruction, pointer,offset):
    parameter1 = data[instruction[1]] if m1==0 else instruction[1] if m1==1 else data[instruction[1]+offset]
    offset = offset + parameter1
    pointer=pointer+2

    return pointer, offset

pointer = 0
offset = 0
while True:
    
    instruction = get_data(data,pointer)
    #print('Instruction',instruction)
    opcode, m1, m2, m3 = prepare_instruction(instruction)
    #print(opcode, m1, m2, m3)
    if opcode==99:
        print('End!')
        break
    elif opcode==1:
        pointer = add_function(m1, m2, m3, instruction, pointer,offset)
    elif opcode==2:
        pointer = multiply_function(m1, m2, m3, instruction, pointer,offset)
    elif opcode==3:
        pointer = input_function(m1,instruction, pointer,offset)
    elif opcode==4:
        output, pointer = output_function(m1, instruction, pointer,offset)    
        print('output',output)
    elif opcode==5:
        pointer = jump_if_true(m1,m2,instruction, pointer,offset)
    elif opcode==6:
        pointer = jump_if_false(m1,m2,instruction, pointer,offset)
    elif opcode==7:
        pointer = less_than(m1,m2,m3,instruction, pointer,offset)
    elif opcode==8:
        pointer = equals_than(m1,m2,m3,instruction, pointer,offset)
    elif opcode==9:
        pointer, offset = change_offset(m1,instruction, pointer,offset)
    else:
        print('No valid opcode')
        raise ValueError
