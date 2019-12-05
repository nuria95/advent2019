import numpy as np

def check_criteria(password):
    criteria_adjacency = False
    criteria_increase = True
    string_password = [i for i in str(password)]
    for i in range(len(string_password)-1):
        if string_password[i]==string_password[i+1]:
            criteria_adjacency = True
        if string_password[i]>string_password[i+1]:
            criteria_increase = False
            break
        
    return criteria_adjacency and criteria_increase

num_combinations = 0 
for password in range(134564,585159+1):
    if check_criteria(password):
        num_combinations +=1
    

print('Num different combinations', num_combinations)


