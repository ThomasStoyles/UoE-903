from enum import Enum
import networkx as nx
import numpy as np
import pandas as pd

class GraphType(Enum):
    DIRECTED_CYCLE = 1
    CYCLE = 2
    FUNNEL = 3
    SUPERSTAR = 4 
    STAR = 5
    LINE = 6
    BURST = 7
    TEACH = 8
    TWITCH = 9 # just to see if it works, later will add all
    TISSUE = 10
    # BARABASI_ALBERT = X
    # 2D weight matrix at every index looking at row 0 thats all nodes that could be connected to node 0 and if any cell have value grater than 0 they are connected to that node

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
        
        # elif self.graph_type == GraphType.TEACH:
        #     graph = nx.DiGraph()
        #     for i in range (1, self.total_population +1):
        #         graph.add_node(i)
        #     return graph
        
        elif self.graph_type == GraphType.LINE:
            graph = nx.DiGraph()
            for i in range(self.total_population):
                graph.add_node(i)
                if i != self.total_population - 1:
                    graph.add_edge(i, i + 1)
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
            graph = nx.star_graph(self.total_population - 1)
            return graph
        
        elif self.graph_type == GraphType.TWITCH:
            edges = pd.read_csv('graphs\musae_DE_edges.csv')
            matrixSize = max(edges.max())
            self.total_population = matrixSize
            graph = nx.DiGraph()
            for ind in range(len(edges) - 1):
                graph.add_edge(edges['from'][ind], edges['to'][ind])
            return graph
        
        elif self.graph_type == GraphType.TISSUE:
            graph = nx.DiGraph()
            # generate honeycomb graph
            for i in range(self.total_population):
                graph.add_node(i)
            # get number of columns and rows needed to represent graph as a 2d square matrix
            size = np.ceil(np.sqrt(self.total_population))
            print('size', size)
            '''
            add edges between current node and the node in these relatives positions
            [(0,1), ]
            To move in the y axis we add or substract the calculated size of columns/rows to represent the graph in a matrix
            this generates a square-like honeycomb
            '''
            # aux variable
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
                    print('redge')
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
##############################################################################################################################################################
        # if self.graph_type == GraphType.DIRECTED_CYCLE:
        #     weight_matrix = np.zeros((self.total_population, self.total_population))
        #     for i in range(self.total_population):
        #         if i < self.total_population - 1:
        #             weight_matrix[i][i+1] = 1
        #         else:
        #             weight_matrix[i][0] = 1
        #     return weight_matrix

        # elif self.graph_type == GraphType.CYCLE:
        #     weight_matrix = np.zeros((self.total_population, self.total_population))
        #     for i in range(self.total_population):
        #         if i < self.total_population - 1:
        #             weight_matrix[i][i+1] = 0.5
        #         else:
        #             weight_matrix[i][0] = 0.5
        #         if i == 0:
        #             weight_matrix[i][-1] = 0.5
        #         else:
        #             weight_matrix[i][i-1] = 0.5
        #     return weight_matrix
        
        # elif self.graph_type == GraphType.LINE:
        #     weight_matrix = np.zeros((self.total_population, self.total_population))
        #     for i in range(self.total_population):
        #         if i < self.total_population - 1:
        #             weight_matrix[i][i+1] = 1
        #         else:
        #             weight_matrix[i][i] = 1
        #     return weight_matrix
        
        # elif self.graph_type == GraphType.TEACH:
        #     weight_matrix = np.zeros((self.total_population, self.total_population))
        #     for i in range(self.total_population):
        #         weight_matrix[i, (i % self.total_population)] = 1/2
        #     return weight_matrix
        
        # elif self.graph_type == GraphType.BURST:
        #     weight_matrix = np.zeros((self.total_population, self.total_population))

        #     # Calculate value for the top row
        #     weight_value = 1 / (self.total_population - 1)

        #     # Assign values to the top row
        #     weight_matrix[0, 1:] = weight_value  # All elements except the first

        #     # Assign 1s to diagonal and zeros elsewhere
        #     for i in range(self.total_population):
        #         weight_matrix[i, i] = 1

        #     return weight_matrix

        # elif self.graph_type == GraphType.STAR:
        #     weight_matrix = np.zeros((self.total_population+1, self.total_population+1))

        #     # weight_matrix = np.zeros((5, 5))

        #     # Set non-zero weights between the central node (index 0) and all other nodes
        #     weight_matrix[0, 1:] = 1
        #     weight_matrix[1:, 0] = 1

        #     # print(weight_matrix)
        #     # weight_matrix = np.array([
        #     #     [0, 0.25, 0.25, 0.25, 0.25],
        #     #     [1, 0, 0, 0, 0],
        #     #     [1, 0, 0, 0, 0],
        #     #     [1, 0, 0, 0, 0],
        #     #     [1, 0, 0, 0, 0],
        #     # ])
        #     # weight_matrix = nx.adjacency_matrix(self.getGraph()).toarray()
        #     return weight_matrix
        
        # elif self.graph_type == GraphType.FUNNEL:
        #     for layer in range(len(self.layers) - 1):
        #         current_layer_nodes = range(sum(self.layers[:layer]), sum(self.layers[:layer + 1]))
        #         next_layer_nodes = range(sum(self.layers[:layer + 1]), sum(self.layers[:layer + 2]))
        #         for node_curr in current_layer_nodes:
        #             for node_next in next_layer_nodes:
        #                 weight_matrix[node_curr][node_next] = 1.0

        #     return weight_matrix

    def getTheoreticalFixationProbability(self, relative_fitness):
        if self.graph_type in (GraphType.DIRECTED_CYCLE, GraphType.CYCLE, GraphType.FUNNEL):
            # p = (1 - 1/r)/(1 - 1/r^N)
            return (1 - (1/relative_fitness)) / (1 - 1 / (relative_fitness**self.total_population))
        elif self.graph_type in [GraphType.LINE, GraphType.BURST, GraphType.TEACH]: #Teach to be changed here for testing purposes
            # p = 1/N
            return (1 / self.total_population)
        elif self.graph_type in [GraphType.STAR]:
            # p = (1 - 1/r^2)/(1 - 1/r^2N)
            return (1 - (1/(relative_fitness**2))) / (1 - 1 / (relative_fitness**(2*self.total_population)))
        elif self.graph_type in [GraphType.SUPERSTAR]:
            # p = (1 - 1/r^k)/(1 - 1/r^kN)
            return (1 - (1/(relative_fitness**self.K))) / (1 - 1 / (relative_fitness**(self.K * self.total_population)))