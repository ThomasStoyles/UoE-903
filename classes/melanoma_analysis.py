# https://github.com/AngryMaciek/angry-moran-simulator/blob/master/moranpycess/MoranProcess.py

import copy
from multiprocessing import Pool
import random
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import concurrent.futures
from tqdm import tqdm
from graph import GraphType, MoranGraphGenerator

class MoranGraph:

    def __init__(self, graph: nx.Graph, relative_fitness: int, initial_infected_count = 1, low_thresh = 0, high_thresh = -1, isTissue = False):
        self.graph = graph
        self.isTissue = isTissue
        if(not isTissue):
            self.W = nx.to_numpy_array(graph, dtype=np.uint8)
        self.r = relative_fitness
        # start relative_fitness array with only 1's as simulation/infection hasn't started
        self.relative_fitness = [1 for _ in graph.nodes]
        if(high_thresh < 0):
            self.high_thresh = len(graph)
        else:
            self.high_thresh = high_thresh
        self.initial_infected_count = initial_infected_count
        self.low_thresh = low_thresh
    
    def getTotalPopulation(self) -> int:
        return len(self.graph.nodes)
    
    def getMutantPopulation(self) -> int:
        # total population - healthy population
        return len(self.relative_fitness) - self.relative_fitness.count(1)
    
    def getAdjacentNodes(self, node: int) -> list:
        if(not self.isTissue):
            # check adjacency matrix and return index where entry is > 0
            neighbours = [index for index, n in enumerate(self.W[node]) if n > 0]
        else:
            neighbours = []
            rEdge = False
            lEdge = False
            totalPopulation = self.getTotalPopulation()
            size = np.ceil(np.sqrt(totalPopulation))
            # if not in left edge
            if(node%totalPopulation > 0):
                neighbours.append(int(node-1))
            else: 
                lEdge = True
            # if not in right edge
            if(node%size < size-1):
                if(node+1 < totalPopulation):
                    neighbours.append(int(node+1))
            # is right edge
            else:
                rEdge = True
            # if not in bottom edge
            if(node+size < totalPopulation):
                neighbours.append(int(node+size))
                # if matrix continues and not in right edge
                if(node+size+1 < totalPopulation and not lEdge):
                    neighbours.append(int(node+size+1))
            # if not in top edge
            if(node-size >= 0):
                neighbours.append(int(node - size))
                # if not in right edge
                if(not rEdge):
                    neighbours.append(int(node - size + 1))
        return neighbours

    def addOffspring(self, parent: int, offspring: int):
        self.relative_fitness[offspring] = self.relative_fitness[parent]

    def select_parent(self) -> int:
        selected_parent = random.choices(list(self.graph.nodes()), weights=self.relative_fitness, k=1)[0]
        return selected_parent

    def getOffspringLocation(self, parent: int) -> int:
        neighbors = self.getAdjacentNodes(parent)
        if(len(neighbors) > 0):
            return random.choice(neighbors)
        else:
            return parent
    def simulation(self):
        self.reset()
        steps = 0
        # run until healthy or infected win within given parameters
        while steps < 100000 and self.low_thresh < self.getMutantPopulation() < self.high_thresh:
                parent = self.select_parent()
                offspring = self.getOffspringLocation(parent)
                self.addOffspring(parent, offspring)
                steps += 1
        # check if healthy or infected won
        return 0 if self.getMutantPopulation() < self.high_thresh else 1

    def reset(self):
        # select new random inital infected nodes
        random_infected_list = random.sample(range(self.getTotalPopulation()), self.initial_infected_count)
        # reset relative fitness array with 1's except for inital infected node
        self.relative_fitness = [self.r if i in random_infected_list else 1 for i in range(self.getTotalPopulation())]

class MoranSimulation:

    def __init__(self, moran_graph: MoranGraph):
        self.__original_graph = moran_graph
        self.moran_graph = moran_graph
        self.total_simulations = 0
        self.fixation_count = 0

    def run_simulation(self, graph_copy):
        return graph_copy.simulation()
    
    def run(self, number_of_simulations: int):
         # run simulations in parallel
         with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.run_simulations) for _ in range(number_of_simulations)]
            results = [future.result() for future in tqdm(concurrent.futures.as_completed(futures), total=number_of_simulations)]
         self.fixation_count = results.count(1)
         self.total_simulations = number_of_simulations
         return self.get_fixation_probability()
    
    def run_simulations(self):
        graph = copy.deepcopy(self.__original_graph)
        return graph.simulation()

        
    def get_fixation_probability(self) -> float:
        if self.total_simulations == 0:
            return 0.0
        return self.fixation_count / self.total_simulations

    def reset(self):
        self.generation = 1
        self.moran_graph = copy.deepcopy(self.__original_graph)
        self.moran_graph.reset()


# For first graph that supervisor mentioned, where all nodes are connected. the weights on each edge should be 1/(N-1)
def parallel_analysis(graph, relative_fitness, simulations_per_run):
    moran_graph = MoranGraph(graph, relative_fitness, isTissue=True)
    moran_simulation = MoranSimulation(moran_graph)
    fixation_probability = moran_simulation.run(simulations_per_run)
    # print('end of one analysis')
    return fixation_probability        

def analysis(population, a, b):
    # fixed graph parameters
    graph_type = GraphType.TISSUE
    simulations_per_run = 10000
    # calculate theoretical fixation probability
    target_fixation_probability = a * (population**b)
    # tolerance calculation for 10%
    tolerance = target_fixation_probability * .1
    # initial relative fitness of 2
    relative_fitness = 1
    # initial steps to search for optimum
    step = 0.49
    # generate graph structure
    generator = MoranGraphGenerator(graph_type, population)
    graph = generator.getGraph()
    data = []
    # testing/data collection
    fixation_probability = parallel_analysis(graph=graph, relative_fitness=relative_fitness, simulations_per_run=simulations_per_run)
    data.append([population, relative_fitness, fixation_probability])
    # get initial estimatino and compare to target
    previous_diff = target_fixation_probability - fixation_probability
    # if fixation probability is higher than target, lower relative fitness
    if(previous_diff < 0):
        step *= -1
    count = 0
    # iterate until we achieve 95% accuracy
    while count < 1000 and abs(fixation_probability - target_fixation_probability) > tolerance and abs(step) > 1/10000000:
         fixation_probability = parallel_analysis(graph=graph, relative_fitness=relative_fitness, simulations_per_run=simulations_per_run)
         data.append([population, relative_fitness, fixation_probability])
         diff = target_fixation_probability - fixation_probability
         # if difference have same sign optimum hasn't been passed over
         # if difference have different sign the optimum is between the current and last test
         if(diff * previous_diff < 0):
             #change direction of step and cut in half
             step *= -1/2
         if(relative_fitness + step <= 0):
            step = relative_fitness/3
         relative_fitness += step
         previous_diff = diff
         count += 1
         print(relative_fitness, diff)
    df = pd.DataFrame(data, columns=['population', 'relative_fitness', 'fixation_probability'])
    df.to_csv('results'+ str(population) + '.csv')
    return(target_fixation_probability)

         

    
# population_targets = [10, 50, 100, 500, 1000]
population_targets = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
a = 0.027
b = -0.7836
results = []
for population in population_targets:
    results.append([population, analysis(population, a, b)])
            