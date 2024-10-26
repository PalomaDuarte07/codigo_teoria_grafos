# -*- coding: utf-8 -*-
"""codigo.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1KBARvsOxgi0Xrlg0tJZfY2KPb24PykMY
"""

import networkx as nx
import matplotlib.pyplot as plt

def dgraph(V, C, A, u):
    # Cria um grafo dirigido
    G = nx.DiGraph()

    # Adiciona nós com coordenadas
    for i, v in enumerate(V):
        G.add_node(v, pos=C[i])  # Atribui coordenada a cada nó

    # Adiciona arcos com capacidades
    for i, (start, end) in enumerate(A):
        G.add_edge(start, end, capacity=u[i])  # Define capacidade do arco

    return G

def plot_dgraph(G):
    # Extrai as posições dos nós
    pos = nx.get_node_attributes(G, 'pos')

    # Desenha os nós e as arestas
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_weight="bold", arrows=True)

    # Extrai as capacidades e desenha labels para os arcos
    capacities = nx.get_edge_attributes(G, 'capacity')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=capacities, font_color='red')

    plt.title("Grafo Dirigido com Capacidades")
    plt.show()

def ford_fulkerson(G, s, t):
    # Calcula o fluxo máximo e o dicionário de fluxo para cada arco
    max_flow, flow_dict = nx.maximum_flow(G, s, t, capacity='capacity')

    # Cria o vetor x com o fluxo em cada arco na ordem de A (ordem de arestas do grafo)
    x = [flow_dict[u][v] for u, v in G.edges()]

    return x, max_flow

# Dados do grafo dirigido
V = ['s', '1', '2', '3', '4', 't']
C = [(0, 0), (1, 1), (1, -1), (2, 1), (2, -1), (3, 0)]
A = [('s', '1'), ('s', '2'), ('1', '2'), ('1', '3'), ('2', '4'), ('3', '2'), ('4', '3'), ('3', 't'), ('4', 't')]
u = [7, 3, 1, 6, 8, 3, 2, 1, 8]

# Criando o grafo
G = dgraph(V, C, A, u)

# Plotando o grafo
plot_dgraph(G)

# Calculando o fluxo máximo
fluxos, fluxo_maximo = ford_fulkerson(G, 's', 't')
fluxos, fluxo_maximo

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

def grid(num_node_x=10, num_node_y=5, plot=False):
    G = nx.Graph()
    k = 0
    V = dict()
    for x in range(num_node_x):
        for y in range(num_node_y):
            V[k] = (x, y)
            G.add_node(k, pos=V[k])
            k += 1
    E = set()
    for k1 in V.keys():
        (x1, y1) = V[k1]
        for k2 in V.keys():
            if k2 != k1:
                if ((k1, k2) not in E) and ((k2, k1) not in E):
                    (x2, y2) = V[k2]
                    if abs(x1 - x2) + abs(y1 - y2) == 1:  # Manhattan norm 1
                        E.add((k1, k2))
                        G.add_edge(k1, k2)
    if plot:
        plt.figure()
        nx.draw_networkx(G, pos=V, with_labels=True, node_color='white', edgecolors='black')
        plt.axis('equal')
        plt.title('Grid')
    return G


def maze(G, plot=False):
    M = nx.Graph(nx.minimum_spanning_tree(G))  # Spanning tree T
    gamma = G.number_of_edges() - M.number_of_edges()
    number_of_cycles = random.randint(1, gamma)  # number of cycles to introduce
    E1 = set(M.edges())
    E2 = set(G.edges())
    E3 = E2.difference(E1)
    for e in E3:
        M.add_edge(e[0], e[1])
        number_of_cycles -= 1
        if number_of_cycles == 0:
            break
    if plot:
        V = nx.get_node_attributes(G, 'pos')
        plt.figure()
        nx.draw_networkx(M, pos=V, with_labels=True, node_color='white', edgecolors='black')
        plt.axis('equal')
        plt.title('Maze')
    return M


def dfs_maze_solver(M, v1, v2):
    stack = [(v1, [v1], [])]  # Stack for DFS: (current node, path of nodes, path of edges)
    visited = set()

    while stack:
        current_node, nodes_path, edges_path = stack.pop()
        visited.add(current_node)

        # Check if we've reached the destination
        if current_node == v2:
            return nodes_path, edges_path

        # Explore neighbors
        for neighbor in M.neighbors(current_node):
            if neighbor not in visited:
                stack.append((neighbor, nodes_path + [neighbor], edges_path + [(current_node, neighbor)]))

    # Return empty lists if no path is found
    return [], []


# Define grid G and maze M
G = grid()
M = maze(G, plot=True)

# Define v1 and v2
v1 = np.random.randint(0, M.number_of_nodes())
while True:
    v2 = np.random.randint(0, M.number_of_nodes())
    if v2 != v1:
        break

# Solve the maze from v1 to v2 using DFS
nodes, edges = dfs_maze_solver(M, v1, v2)
nodes, edges