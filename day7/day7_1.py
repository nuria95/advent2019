import numpy as np
import time
from itertools import permutations

data_original = np.loadtxt('input.txt',delimiter=',').astype(int)
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

def input_function(instruction,pointer, the_input):
    #the_input=input('Provide me an input: ')
    data[instruction[1]]=the_input
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


output_amplifier = 0 # first_input to amplifier A
possible_combinations = list(permutations([0,1,2,3,4]))
final_thruster = 0 # to keep updating with maximum value
for setting_list in possible_combinations:
    
    for setting_amplifier in setting_list:
        data=data_original.copy() #Reset data
        mode='setting_mode'

        pointer = 0
        while True:
            instruction = get_data(data,pointer)
            opcode, m1, m2, m3 = prepare_instruction(instruction)
            if opcode==99:
                print('break')
                break
            elif opcode==1:
                pointer = add_function(m1, m2, instruction, pointer)
            elif opcode==2:
                pointer = multiply_function(m1, m2, instruction, pointer)
            elif opcode==3:
                print(mode)
                if mode =='setting_mode':
                    pointer = input_function(instruction, pointer, int(setting_amplifier))
                    mode = 'input_mode'
                else:
                    pointer = input_function(instruction, pointer, output_amplifier)
            elif opcode==4:
                output_amplifier, pointer = output_function(m1, instruction, pointer)
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

    if output_amplifier > final_thruster:
        final_thruster = output_amplifier.copy()
        final_settings = list(setting_list).copy()
    output_amplifier = 0 # Reset for input to amplifier A

print('Max final_thruster', final_thruster)
print('Settings to achieve this thruster', final_settings)
