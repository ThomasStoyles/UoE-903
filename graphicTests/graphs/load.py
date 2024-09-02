import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

edges = pd.read_csv('graphs\musae_DE_edges.csv')
print(max(edges['from']))
print(max(edges['to']))
# get highest node number
matrixSize = max(edges.max())
print(matrixSize)
matrix = np.zeros([matrixSize, matrixSize])
for ind in range(matrixSize-1):
    matrix[edges['from'][ind]][edges['to'][ind]] = 1
