import graphanalysis.loader as loader
import graphanalysis.graphanalyser as ga
import pprint

if __name__ == '__main__':
    g = loader.load('./resources/dataset/karate-club.txt', is_directed=False, sep=" ")
    pprint.pprint(ga.GraphAnalyser(g).get_properties(), width=500)
