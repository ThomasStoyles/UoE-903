# https://github.com/AngryMaciek/angry-moran-simulator/blob/master/moranpycess/MoranProcess.py

import copy
import random
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from Moran.graph import GraphType, MoranGraphGenerator

class MoranGraph:

    def __init__(self, graph: nx.Graph, relative_fitness: int, initial_infected: list = None):
        if not initial_infected:
            initial_infected = []
        self.graph = graph
        self.W = nx.to_numpy_array(graph)
        self.r = relative_fitness
        self.relative_fitness = [self.r if node in initial_infected else 1 for node in graph.nodes]
        self.population = [1 if node in initial_infected else 0 for node in graph.nodes]
        self.infected_nodes = set(node for node, status in zip(graph.nodes, self.population) if status == 1)
    
    def getTotalPopulation(self) -> int:
        return len(self.population)
    
    def getMutantPopulation(self) -> int:
        return len(self.infected_nodes)
    
    def getAdjacentNodes(self, node: int) -> list:
        neighbours = [index for index, n in enumerate(self.W[node]) if n > 0]
        return neighbours

    def addOffspring(self, parent: int, offspring: int):
        '''
        TODO: support for different methods of updating
        Only copying the parent type
        can add later: weight updates
        '''
        parent_type = self.population[parent]
        offspring_type = self.population[offspring]
        self.population[offspring] = parent_type
        if offspring not in self.infected_nodes and parent_type == 1:
            self.infected_nodes.add(offspring)
            self.relative_fitness[offspring] = self.r
        if offspring_type == 1 and parent_type == 0:
            self.infected_nodes.remove(offspring)
            self.relative_fitness[offspring] = 1

    def getOffspringLocation(self, parent: int) -> int:
        neighbors = self.getAdjacentNodes(parent)
        if(len(neighbors) > 0):
            return random.choice(neighbors)
        else:
            return parent

    def getFitness(self, node: int) -> int:
        # print(self.relative_fitness)
        # print(node)
        return self.relative_fitness[node]/sum(self.relative_fitness)

    def reset(self):
        random_infected = np.random.randint(low=0, high=self.getTotalPopulation()-1)
        self.relative_fitness = [self.r if node == random_infected else 1 for node in self.graph.nodes]
        self.population = [1 if node == random_infected else 0 for node in self.graph.nodes]
        self.infected_nodes = set(node for node, status in zip(self.graph.nodes, self.population) if status == 1)

class MoranSimulation:

    def __init__(self, moran_graph: MoranGraph):
        self.__original_graph = moran_graph
        self.moran_graph = moran_graph
        self.generation = 1
        self.total_simulations = 0
        self.fixation_count = 0
        self.simulationMemory = None

    def run(self, number_of_simulations: int):
        self.simulationMemory = []
         #for k in tqdm(range(number_of_simulations), desc="Simulations"):
            #self.reset()
        mem = list(self.moran_graph.infected_nodes)
        self.simulationMemory.append(mem)
        while 0 < self.moran_graph.getMutantPopulation() < self.moran_graph.getTotalPopulation():
            self.generation += 1
            parent = self.select_parent()
            offspring = self.moran_graph.getOffspringLocation(parent)
            self.moran_graph.addOffspring(parent, offspring)
            mem = list(self.moran_graph.infected_nodes)
            self.simulationMemory.append(mem)
            # print(f'Mem: ' + str(mem) + '\nsimMem: ' + str(self.simulationMemory))
            
        self.collect_data()

    def select_parent(self) -> int:
        fitness_values = [self.moran_graph.getFitness(node) for node in self.moran_graph.graph.nodes()]
        selected_parent = random.choices(list(self.moran_graph.graph.nodes()), weights=fitness_values, k=1)[0]
        return selected_parent

    def collect_data(self):
        self.total_simulations += 1
        if self.moran_graph.getMutantPopulation() == self.moran_graph.getTotalPopulation():
            self.fixation_count += 1
        
    def get_fixation_probability(self) -> float:
        if self.total_simulations == 0:
            return 0.0
        return self.fixation_count / self.total_simulations

    def reset(self):
        self.generation = 1
        self.moran_graph = copy.deepcopy(self.__original_graph)
        self.moran_graph.reset()


################################################################

# Visualization
# pos = nx.spring_layout(graph)  # Layout for the nodes
# # Draw the graph
# nx.draw(graph, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=8)
# # Add labels for edge weights
# # edge_labels = {(i, j): f"{weight_matrix[i-1, j-1]:.2f}" for i, j in graph.edges()}
# nx.draw_networkx_edge_labels(graph, pos)
# plt.show()

# For first graph that supervisor mentioned, where all nodes are connected. the weights on each edge should be 1/(N-1)