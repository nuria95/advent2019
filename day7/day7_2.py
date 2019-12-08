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

def advance_system(num_amplifier, input_amplifiers):
    if num_amplifier < 4:
        num_amplifier = num_amplifier+1
        input_amplifiers[num_amplifier] = output_amplifier
        return num_amplifier, input_amplifiers
        
    else:
        num_amplifier = 0
        input_amplifiers[num_amplifier] = output_amplifier
        return num_amplifier, input_amplifiers
        
  
data_list_original = []
for i in range(5):
    data_list_original.append(data_original.copy()) #Keeps status of every amplifier

possible_combinations = list(permutations([5,6,7,8,9]))

final_thruster = 0 # to keep updating with maximum value

for setting_list in possible_combinations:
    setting_list=list(setting_list)
    input_amplifiers = np.zeros(5, dtype=int) # first_input to amplifier A
    data_list=data_list_original.copy() #Reset data. Moved in this for now
    pointer_list= np.zeros(5,dtype=int) 
    num_amplifier = 0
    stop_feedback=False
    while True:
        if stop_feedback:
            break
        if len(setting_list)>0:
            setting_amplifier=setting_list.pop(0)
            mode = 'setting_mode'
        else:
            mode = 'input_mode'
        data = data_list[num_amplifier]
        pointer = pointer_list[num_amplifier]

        while True:
            instruction = get_data(data,pointer)
            opcode, m1, m2, m3 = prepare_instruction(instruction)
            if opcode==99:
                stop_feedback = True
                break
            elif opcode==1:
                pointer = add_function(m1, m2, instruction, pointer)
            elif opcode==2:
                pointer = multiply_function(m1, m2, instruction, pointer)
            elif opcode==3:
                if mode =='setting_mode':
                    pointer = input_function(instruction, pointer, int(setting_amplifier))
                    mode = 'input_mode'
                elif mode == 'input_mode':
                    pointer = input_function(instruction, pointer, input_amplifiers[num_amplifier])
                else:
                    raise ValueError
            elif opcode==4:
                output_amplifier, pointer = output_function(m1, instruction, pointer)
                break
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
        
        if stop_feedback==False:
            pointer_list[num_amplifier]=pointer
            num_amplifier, input_amplifiers = advance_system(num_amplifier, input_amplifiers)
        
    output_to_thruster = input_amplifiers[0]
        
    if output_to_thruster > final_thruster:
        final_thruster = output_amplifier
    
print('Max final_thruster', final_thruster)

