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



for planet in all_planets:
    if planet.name == 'SAN':
        path_san_to_COM = tuple(planet.get_parents())
    if planet.name == 'YOU':
        path_you_to_COM = tuple(planet.get_parents())

#get first element that coincides between the two paths (paths are from node TO COM)
path_together=[]
for node_name in path_san_to_COM:
    if node_name in path_you_to_COM:
        first_element = node_name
        break
#get the number of orbital transfers from YOU to common element
num_orbital_transfers = 0      
for node_name in path_you_to_COM:
    if node_name == first_element:
        break
    else:
        num_orbital_transfers+=1
#get the number of orbital transfers from common element to SAN
for node_name in path_san_to_COM:
    if node_name == first_element:
        break
    else:
        num_orbital_transfers+=1

print(num_orbital_transfers)