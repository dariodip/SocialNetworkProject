import graphanalysis.loader as loader
import graphanalysis.graphanalyser as ga
import pprint
import networkx as nx
from graphanalysis import influence

if __name__ == '__main__':
    g = loader.load('./resources/dataset/karate-club.txt', is_directed=True, sep=" ")
    pprint.pprint(ga.GraphAnalyser(g).get_properties(), width=500)

    print("target set:", influence.generate_target_set_selection(g, 1))
