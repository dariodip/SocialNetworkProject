import powerlaw
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

np.seterr(divide='ignore', invalid='ignore')

def get_node_degree(g):
    if nx.is_directed(g):
        degree = [t[1] for t in g.in_degree]
    else:
        degree = [t[1] for t in g.degree]

    return degree

def get_powerlaw_distribution_alpha(g):
    degree = get_node_degree(g)

    fit = powerlaw.Fit(degree, xmin=min(degree), xmax=max(degree))
    return fit.power_law.alpha

def plot_degree_powerlaw_distribution(g):
    # Degree frequencies
    degree = pd.Series(get_node_degree(g))
    degree_count = degree.value_counts()
    degree_freq = {d: degree_count[d]/sum(degree_count) for d in degree_count.index}
    xvalue = list(degree_freq.keys())
    yvalue= list(degree_freq.values())
    plt.plot(xvalue, yvalue, 'ro')

    # Powerlaw distribution
    alpha = get_powerlaw_distribution_alpha(g)
    print(min(degree_count.index), max(degree_count.index))
    xvalue = np.linspace(min(degree_count.index), max(degree_count.index), 100)
    yvalue = list(map(lambda x: x**(-alpha), xvalue))
    plt.plot(xvalue, yvalue, 'b-')
    plt.show()