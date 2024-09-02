# https://github.com/AngryMaciek/angry-moran-simulator/blob/master/moranpycess/MoranProcess.py

import copy
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
            # use same algorithm used to create tissue graph to find neighbors
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
        # run until healthy or infected win within given parameters
        while self.low_thresh < self.getMutantPopulation() < self.high_thresh:
                parent = self.select_parent()
                offspring = self.getOffspringLocation(parent)
                self.addOffspring(parent, offspring)
        # check if healthy or infected won
        return 1 if self.getMutantPopulation() > self.low_thresh else 0

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
            results = [future.result() for future in list(concurrent.futures.as_completed(futures), total=number_of_simulations)]
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
def parallel_analysis(graph, relative_fitness, initial_infected_count, low_thresh, high_thresh, simulations_per_run):
    moran_graph = MoranGraph(graph, relative_fitness, initial_infected_count=initial_infected_count, low_thresh=low_thresh, high_thresh=high_thresh, isTissue=True)
    moran_simulation = MoranSimulation(moran_graph)
    fixation_probability = moran_simulation.run(simulations_per_run)
    print('end of one analysis')
    return [relative_fitness, initial_infected_count, fixation_probability]        

def analysis():
    # fixed graph parameters
    graph_type = GraphType.TISSUE
    total_population = 500
    simulations_per_run = 385
    fitness_count = 25
    initial_count_num = 2
    # 0.5% low threshold
    low_thresh = 5
    # 70% high threshold
    high_thresh = 700
    # generate graph structure
    generator = MoranGraphGenerator(graph_type, total_population)
    graph = generator.getGraph()

        # variable parameters (to be analysed)
    # test relative fitness in increments
    relative_fitnesses = np.linspace(start=1.04, stop=2, num=fitness_count)
    # test initail infected count in increments
    initial_infected_counts = np.linspace(start=10, stop=100, num=initial_count_num, dtype=np.int16)

    # testing/data collection
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(parallel_analysis,graph=graph, relative_fitness=relative_fitness, initial_infected_count=initial_infected_count, low_thresh=low_thresh, high_thresh=high_thresh, simulations_per_run=simulations_per_run) for relative_fitness in relative_fitnesses for initial_infected_count in initial_infected_counts]
        results = [future.result() for future in tqdm(concurrent.futures.as_completed(futures))]
    df = pd.DataFrame(results, columns=['relative_fitness', 'initial_infected_count', 'fixation_probability'])
    df.to_csv('results.csv')

analysis()
            