import numpy as np
import time
data = np.loadtxt('input.txt', dtype=np.str)

class Node():
    def __init__(self, name):
        self.name = name
        self.tree = []
        self.prev = None
        self.num_orbits = 0
        self.update_all_planets()
        self.num_direct_children = 0
        

    def update_all_planets(self):
        global all_planets
        all_planets.append(self)

    def add_planet_to_tree(self,planet_name):
        if planet_name in [i.name for i in all_planets]:
            planet = self.goto_planet(planet_name) # do not create a new node if it already exists!
        else:
            planet = Node(planet_name)
        self.tree.append(planet)
        self.num_direct_children = len(self.tree)
        planet.prev=self # keep track of all self variables from prev planet
        return planet
    
    def prev_planet(self):
        return self.prev #return previous node

    def goto_planet(self, planet_name): #only possible from top
        for planet in all_planets:
            if planet.name == planet_name:
                return planet
    
    def get_children(self, children_list=[], to_explore_list=[]):
        to_explore_list = to_explore_list + self.tree

        if self.num_direct_children==0 and len(to_explore_list)==0: 
            children_names=[]
            for i in children_list:
                children_names.append(i.name)
            return children_names
            
        elif self.num_direct_children == 0:
            to_explore_list.pop()
            return self.get_children(children_list,to_explore_list)

        else:   
            children_list = children_list + self.tree
            child = to_explore_list[-1]
            return child.get_children(children_list,to_explore_list)

    def get_parents(self, parents_list=[]):
        parent = self.prev
        parents_list = parents_list + [parent]
        
        if parent is None and len(parents_list)==0:
            return None
        elif parent is None:
            parent_names = []
            for i in parents_list[:-1]:
                parent_names.append(i.name)
            return parent_names
        else:  
            return parent.get_parents(parents_list)

    def get_num_parents(self):
        return len(self.get_parents())

    
    
def prepare_input(data_sample):
    parent, child = data_sample.split(')')
    return parent, child

all_planets=[]
BigSystem = Node('COM')  

for i in data:
    parent, child = prepare_input(i)
    parent_node = BigSystem.goto_planet(parent)
    if parent_node is None:
        parent_node = Node(parent)
    child_node = parent_node.add_planet_to_tree(child)
    
    #children_list = parent_node.get_children()
    # print(parent_node.name, 'has children', parent_node.get_children())
    # print(child_node.name, 'has parent', child_node.get_parents())
    # #print(child_node.name, 'has', child_node.get_num_parents(),'parents')
    # print('\n')
    
num_orbits = 0
print('num of planets',len(all_planets))
for planet in all_planets:
    num_orbits = num_orbits + planet.get_num_parents()

print('Num of orbits',num_orbits)



    