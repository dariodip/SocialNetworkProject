import graphanalysis.loader as loader
import graphanalysis.graphanalyser as ga

if __name__ == '__main__':
    g = loader.load('./resources/dataset/random-graph.txt', is_directed=True, sep=" ")
    ga.GraphAnalyser(g)