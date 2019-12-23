import numpy as np
import time
data = np.loadtxt('input.txt',delimiter=',').astype(int)
data = np.append(data,np.zeros((100000,1),dtype=int))

class Intcode():
    def __init__2(self, pointer, offset):
        self.pointer = pointer
        self.offset = offset

    def to_string(self, array_to_transform): #[1240] --> ['1','2','4','0']
        return [i for i in str(array_to_transform)]

    def get_data(self, data):
        string=self.to_string(data[self.pointer])
        if int(string[-1])==4 or int(string[-1])==3 or int(string[-1])==9: #check if last element of instruction opcode is a 3 or 4 or 9
            length_instr = 2
        else:
            length_instr = 4  
        return data[self.pointer:self.pointer+length_instr]

    def prepare_instruction(self, instruction):
        instruction_opcode_str= self.to_string(instruction[0])
        m3, m2,m1,temp1,temp2 = ['0']*(5-len(instruction_opcode_str)) + instruction_opcode_str #in case some parameter modes missing fill with 0s
        opcode=''.join([temp1,temp2])

        return int(opcode),int(m1),int(m2),int(m3)


    def add_function(self, m1,m2,m3, instruction):
        value1 = data[instruction[1]] if m1==0 else instruction[1] if m1==1 else data[instruction[1]+self.offset]
        value2 = data[instruction[2]] if m2 ==0 else instruction[2] if m2==1 else data[instruction[2]+self.offset]
        position = instruction[3] if m3==0 else (instruction[3]+self.offset)
        number = value1 + value2
        data[position]=number
        self.pointer=self.pointer+4


    def multiply_function(self, m1,m2,m3,instruction):
        value1 = data[instruction[1]] if m1==0 else instruction[1] if m1==1 else data[instruction[1]+self.offset]
        value2 = data[instruction[2]] if m2 ==0 else instruction[2] if m2==1 else data[instruction[2]+self.offset]
        number = value1 * value2
        position = instruction[3] if m3==0 else (instruction[3]+self.offset)
        data[position]=number
        self.pointer=self.pointer+4

    def input_function(self, m1, instruction):
        the_input=input('Provide me an input (give a 2): ')
        position = instruction[1] if m1==0 else (instruction[1]+self.offset)
        data[position]=int(the_input)
        self.pointer=self.pointer+2

    def output_function(self, m1,instruction):
        self.pointer=self.pointer+2
        output = data[instruction[1]] if m1==0 else data[1] if m1==1 else data[instruction[1]+self.offset]
        return output

    def jump_if_true(self, m1,m2,instruction):
        parameter1 = data[instruction[1]] if m1==0 else instruction[1] if m1==1 else data[instruction[1]+self.offset]
        parameter2 = data[instruction[2]] if m2==0 else instruction[2] if m2==1 else data[instruction[2]+self.offset]
        if parameter1!=0:
            self.pointer = parameter2
        else:
            self.pointer = self.pointer + 3

    def jump_if_false(self, m1,m2,instruction):
        parameter1 = data[instruction[1]] if m1==0 else instruction[1] if m1==1 else data[instruction[1]+self.offset]
        parameter2 = data[instruction[2]] if m2==0 else instruction[2] if m2==1 else data[instruction[2]+self.offset]
        if parameter1==0:
            self.pointer = parameter2
        else:
            self.pointer = self.pointer + 3

    def less_than(self, m1,m2,m3,instruction):
        parameter1 = data[instruction[1]] if m1==0 else instruction[1] if m1==1 else data[instruction[1]+self.offset]
        parameter2 = data[instruction[2]] if m2==0 else instruction[2] if m2==1 else data[instruction[2]+self.offset]
        position = instruction[3] if m3==0 else (instruction[3]+self.offset)
        if parameter1<parameter2:
            data[position]=1
        else:
            data[position]=0
        self.pointer = self.pointer + 4

    def equals_than(self, m1,m2,m3,instruction):
        parameter1 = data[instruction[1]] if m1==0 else instruction[1] if m1==1 else data[instruction[1]+self.offset]
        parameter2 = data[instruction[2]] if m2==0 else instruction[2] if m2==1 else data[instruction[2]+self.offset]
        position = instruction[3] if m3==0 else (instruction[3]+self.offset)
        if parameter1==parameter2:
            data[position]=1
        else:
            data[position]=0
        self.pointer = self.pointer + 4

    def change_offset(self, m1, instruction):
        parameter1 = data[instruction[1]] if m1==0 else instruction[1] if m1==1 else data[instruction[1]+self.offset]
        self.offset = self.offset + parameter1
        self.pointer=self.pointer+2

pointer = 0
offset = 0
intcode = Intcode(pointer,offset)
while True:
    
    instruction = intcode.get_data(data)
    #print('Instruction',instruction)
    opcode, m1, m2, m3 = intcode.prepare_instruction(instruction)
    #print(opcode, m1, m2, m3)
    if opcode==99:
        print('End!')
        break
    elif opcode==1:
        intcode.add_function(m1, m2, m3, instruction)
    elif opcode==2:
        intcode.multiply_function(m1, m2, m3, instruction)
    elif opcode==3:
        intcode.input_function(m1,instruction)
    elif opcode==4:
        output = intcode.output_function(m1, instruction)
        print('output',output)
    elif opcode==5:
        intcode.jump_if_true(m1,m2,instruction)
    elif opcode==6:
         intcode.jump_if_false(m1,m2,instruction)
    elif opcode==7:
        intcode.less_than(m1,m2,m3,instruction)
    elif opcode==8:
        intcode.equals_than(m1,m2,m3,instruction)
    elif opcode==9:
        intcode.change_offset(m1,instruction)
    else:
        print('No valid opcode')
        raise ValueError
