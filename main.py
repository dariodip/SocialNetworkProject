import graphanalysis.loader as loader
import graphanalysis.graphanalyser as ga
import pprint

from graphanalysis import influence
from graphanalysis.powerlaw import plot_degree_powerlaw_distribution

if __name__ == '__main__':
    g = loader.load('./resources/dataset/karate-club.txt', is_directed=True, sep=" ")
    pprint.pprint(ga.GraphAnalyser(g).get_properties(), width=500)
    print("target set:", influence.generate_target_set_selection(g, 1))

    # Powerlaw graph
    plot_degree_powerlaw_distribution(g)
