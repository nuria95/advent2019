import numpy as np

def check_criteria(password):
    
    criteria_adjacency = False
    criteria_increase = True
    string_password = [i for i in str(password)]
    string_password.insert(0,str(int(string_password[0])-1))
    string_password.append(str(int(string_password[-1])+1))

    
    for i in range(1,len(string_password)-1):
        criteria_adjacency_pair = False 
        criteria_pair_group = True
        if string_password[i]==string_password[i+1]:
            criteria_adjacency_pair = True
            if string_password[i-1]==string_password[i] or string_password[i+1]==string_password[i+2]:
                    criteria_pair_group = False
        if criteria_adjacency_pair and criteria_pair_group: #we need adjacency and no big groups criteria
            criteria_adjacency = True
        
        if int(string_password[i])>int(string_password[i+1]): #important change to int in this case beacaseu when appening values at the end, we can get 10's 
            criteria_increase = False
            break
    return criteria_adjacency and criteria_increase

num_combinations = 0 
for password in range(134564,585159+1):
#for password in ['111233']:

    if check_criteria(password):
        num_combinations +=1
    

print('Num different combinations', num_combinations)


