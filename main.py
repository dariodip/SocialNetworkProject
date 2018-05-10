import graphanalysis.loader as loader
import graphanalysis.graphanalyser as ga

if __name__ == '__main__':
    g = loader.load('./resources/dataset/wiki-Vote.txt', is_directed=True)
    ga.GraphAnalyser(g)