import numpy as np
import time

def compute_fuel(mass):
    return np.floor(mass/3)-2

data = np.loadtxt('input.txt')
fuel = 0
t=time.time()
for module in data:
    temp = module
    while temp > 0:
        temp = compute_fuel(temp)
        if temp <=0:
            break
        fuel = fuel + temp

print('Total fuel is',fuel)
print('Total time is',time.time()-t)


# ## test
fuel = 0
temp = 100756
while temp > 0:
        temp = compute_fuel(temp)
        if temp <=0:
            break
        fuel = fuel + temp
assert fuel == 50346, 'Not passed the test!'
print('Test passed')
