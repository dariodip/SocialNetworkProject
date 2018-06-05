import powerlaw
import networkx as nx
import matplotlib.pyplot as plt


def get_powerlaw_distribution(g):
    degree = []
    if nx.is_directed(g):
        degree = [t[1] for t in g.in_degree]
    else:
        degree = [t[1] for t in g.degree]

    return powerlaw.Fit(degree, xmin=min(degree), xmax=max(degree))

def plot_degree_powerlaw_distribution(g):
    fit = get_powerlaw_distribution(g)

    fig = fit.plot_pdf(color='r', marker="o", linestyle="None", original_data=True)
    fit.power_law.plot_pdf(color='b', linestyle='--', ax=fig)

    plt.show()
