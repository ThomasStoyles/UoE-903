from enum import Enum
import networkx as nx
import numpy as np
import pandas as pd

class GraphType(Enum):
    DIRECTED_CYCLE = 1
    CYCLE = 2
    STAR = 5
    LINE = 6
    BURST = 7
    TWITCH = 9 
    TISSUE = 10

class MoranGraphGenerator:
    def __init__(self, graph_type: GraphType, total_population: int):
        self.total_population = total_population
        self.graph_type = graph_type

    def getGraph(self) -> nx.Graph:
        if self.graph_type == GraphType.DIRECTED_CYCLE:
            graph = nx.cycle_graph(self.total_population, create_using=nx.DiGraph)
            return graph

        elif self.graph_type == GraphType.CYCLE:
            graph = nx.cycle_graph(self.total_population, create_using=nx.DiGraph)
            return graph
        
        elif self.graph_type == GraphType.LINE:
            graph = nx.DiGraph()
            graph.add_node(0)
            for i in range(1, self.total_population):
                graph.add_node(i)
                graph.add_edge(i - 1, i)
            return graph
        
        elif self.graph_type == GraphType.BURST:
            graph = nx.DiGraph()
            # Add the central node
            graph.add_node(0)
            # Add outside nodes and connect them to the central node
            for i in range(1, self.total_population):
                graph.add_node(i)
                graph.add_edge(0, i)
            return graph
        
        elif self.graph_type == GraphType.STAR:
            graph = nx.DiGraph()
            # Add the central node
            graph.add_node(0)
            # Add outside nodes and connect them to the central node
            for i in range(1, self.total_population):
                graph.add_node(i)
                graph.add_edge(0, i)
                graph.add_edge(i, 0)
            return graph
        
        elif self.graph_type == GraphType.TWITCH:
            edges = pd.read_csv('graphs\musae_DE_edges.csv')
            matrixSize = max(edges.max())
            self.total_population = matrixSize
            graph = nx.DiGraph()
            for i in range(self.total_population):
                graph.add_node(i)
            for ind in range(len(edges) - 1):
                graph.add_edge(edges['from'][ind], edges['to'][ind])
            return graph
        
        elif self.graph_type == GraphType.TISSUE:
            graph = nx.DiGraph()
            # generate honeycomb graph nodes
            for i in range(self.total_population):
                graph.add_node(i)
            # get number of columns and rows needed to represent graph as a 2d square matrix
            size = np.ceil(np.sqrt(self.total_population))
            print('size', size)
            '''
            add edges between current node and the node in these relatives positions (if available)
            [(0,1), (0,-1), (1,0), (-1,0), (1,1), (-1,-1)]
            To move in the y axis we add or substract the calculated size of columns/rows to represent the graph in a matrix
            this generates a slanted-square-like honeycomb
            '''
            # iterate through each node number from 0
            for i in range(self.total_population):
                rEdge = False
                lEdge = False
                # if not in left edge 
                if(i%size > 0):
                    graph.add_edge(i,i-1)
                else: lEdge = True
                # if not in right edge
                if(i%size < size-1):
                    if(i+1 < self.total_population):
                        graph.add_edge(i,i+1)
                # is right edge
                else:
                    rEdge = True
                # if not in bottom edge
                if(i+size < self.total_population):
                    graph.add_edge(i,i+size)
                    # if matrix continues and not in right edge
                    if(i+size+1 < self.total_population and not lEdge):
                        graph.add_edge(i,i+size-1)
                # if not in top edge
                if(i-size >= 0):
                    graph.add_edge(i,i-size)
                    # if not in right edge
                    if(not rEdge):
                        graph.add_edge(i,i-size+1)
            return graph

    def getTheoreticalFixationProbability(self, relative_fitness):
        if self.graph_type in (GraphType.DIRECTED_CYCLE, GraphType.CYCLE):
            # p = (1 - 1/r)/(1 - 1/r^N)
            return (1 - (1/relative_fitness)) / (1 - 1 / (relative_fitness**self.total_population))
        elif self.graph_type in [GraphType.LINE, GraphType.BURST]: #Teach to be changed here for testing purposes
            # p = 1/N
            return (1 / self.total_population)
        elif self.graph_type in [GraphType.STAR]:
            # p = (1 - 1/r^2)/(1 - 1/r^2N)
            return (1 - (1/(relative_fitness**2))) / (1 - (1 / (relative_fitness**(2*self.total_population))))