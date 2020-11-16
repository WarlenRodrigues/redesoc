from statistics import mean
import seaborn as sns
import networkx as nx
import freeman as fm
from math import log

def make_Eignvector(rede):
    ec = nx.eigenvector_centrality(rede, max_iter=100)
    return ec

def make_Degree(rede):
    dc = nx.degree_centrality(rede)
    return dc

def make_Betweenness(rede):
    bc = nx.betweenness_centrality(rede)
    return bc

def make_Closeness(rede):
    cc = nx.closeness_centrality(rede)
    return cc

def make_AssortividadeGrau(rede):
    c = nx.degree_assortativity_coefficient(rede)
    return c

def proportion(rede, nós, vizinhos):
    return 1 / rede.degree(nós)

def local_effsize(rede, nós, vizinhos):
    s = 1
    for k in rede.neighbors(nós):
        if rede.has_edge(k, vizinhos):
            s -= proportion(rede, nós, k)
    return s

def effsize(rede, nós):
    s = 0
    for vizinhos in rede.neighbors(nós):
        s += local_effsize(rede, nós, vizinhos)
    return s

def local_constraint(rede, nós, vizinhos):
    s = proportion(rede, nós, vizinhos)
    for k in rede.neighbors(nós):
        if rede.has_edge(k, vizinhos):
            s += proportion(rede, nós, k) * proportion(rede, k, vizinhos)
    return s**2

def constraint(rede, nós):
    if rede.degree(nós) == 0:
        return 2
    s = 0
    for vizinhos in rede.neighbors(nós):
        s += local_constraint(rede, nós, vizinhos)
    return s

def hierarchy(rede, nós):
    c = constraint(rede, nós)
    nós = rede.number_of_nodes()
    s = 0
    for vizinhos in rede.neighbors(nós):
        f = local_constraint(rede, nós, vizinhos) / (c / nós)
        s += f * log(f)
    return s / (nós * log(nós))

def make_articulationPoints(rede):
    ap = nx.articulation_points(rede)
    return ap


# vizinhos rede.neighbors
# nós rede.nodes
# exemplo de uso
# for n in rede.nodes:
#     eff[n] = effsize(g, n)