import numpy as np

def compute_fuel(mass):
    return np.floor(mass/3)-2

data = np.loadtxt('input.txt')
fuel = 0
for module in data:
    fuel = fuel + compute_fuel(module)

print('Total fuel is',fuel)

