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


def plot_degree_powerlaw_distribution(g, name: str, show=False):

    plt.rc('text', usetex=True) # Text formatting with LaTeX

    # Degree frequencies
    fig = plt.figure()
    degree = pd.Series(get_node_degree(g))
    degree_count = degree.value_counts()
    degree_freq = {d: degree_count[d]/sum(degree_count) for d in degree_count.index}
    degree_x_value = list(degree_freq.keys())
    degree_y_value= list(degree_freq.values())

    degree_x_value = np.log10(degree_x_value)
    degree_y_value = np.log10(degree_y_value)
    plt.plot(degree_x_value, degree_y_value, 'ro')

    # Powerlaw distribution
    alpha = get_powerlaw_distribution_alpha(g)

    pow_x_value = np.linspace(min(degree_count.index), max(degree_count.index), 100)
    pow_y_value = list(map(lambda x: x**(-alpha), pow_x_value))

    pow_x_value = np.log10(pow_x_value)
    pow_y_value = np.log10(pow_y_value)
    plt.plot(pow_x_value, pow_y_value, 'b-')

    plt.xlabel(r"$k$")
    plt.ylabel(r"$f_k$")
    alpha_exponent = round(-alpha, 3)
    plt.title(r'Distribuzione dei gradi e funzione $f(k) = k^{' + str(alpha_exponent) + r'}$')
    plt.savefig("resources/results/img/{}.png".format(name), dpi=fig.dpi)

    if show:
        plt.show()
