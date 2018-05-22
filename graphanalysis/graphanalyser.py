import math
import networkx as nx
import networkx.algorithms.approximation as approx
from networkx.algorithms import community


class GraphAnalyser(object):

    def __init__(self, g: nx.Graph):
        self.__g = g
        self.__data_dict = dict()
        self.__degree_stats()
        self.__graph_props()
        self.__basic_info()
        self.__communities_props()
        self.__link_analysis()

    def __basic_info(self):
        self.__data_dict['Edges'] = self.__g.number_of_edges()
        self.__data_dict['Nodes'] = self.__g.number_of_nodes()
        self.__data_dict['Self Loops'] = self.__g.number_of_selfloops()

    def __degree_stats(self):
        degrees = self.__g.degree(list(self.__g.nodes))
        max_degree_name, max_degree = max(degrees, key=lambda i: (i[1], i[0]))
        min_degree_name, min_degree = min(degrees, key=lambda i: (i[1], i[0]))
        names, degrees = zip(*degrees)
        avg_degree = sum(degrees)/len(degrees)
        self.__data_dict['Max Degree'] = max_degree
        self.__data_dict['Max Degree Id'] = max_degree_name
        self.__data_dict['Min Degree'] = min_degree
        self.__data_dict['Min Degree Id'] = min_degree_name
        self.__data_dict['Avg Degree'] = avg_degree

    def __graph_props(self):
        strongly_conn = self.__data_dict['Strongly Connected'] = nx.is_strongly_connected(self.__g)
        self.__data_dict['Diameter'] = nx.diameter(self.__g) if strongly_conn else math.inf
        self.__data_dict['Radius'] = nx.radius(self.__g) if strongly_conn else math.inf
        # self.__data_dict['Average Clustering'] = nx.average_clustering(self.__g) TODO
        self.__data_dict['Max Clique Count'] = len(approx.max_clique(self.__g))
        self.__data_dict['Max Independent Set Count'] = len(approx.maximum_independent_set(self.__g))

    def __communities_props(self):
        self.__communities = list(community.girvan_newman(self.__g))
        self.__best_community = max(self.__communities, key=lambda c: community.performance(self.__g, c))

    def __link_analysis(self):
        self.__pagerank = self.pagerank(self.__g)
        self.__hits = self.hits(self.__g)

    def pagerank(self, g, alpha=0.85, personalization=None, max_iter=100, tol=1e-06, nstart=None, weight='weight',
                 dangling=None):
        return nx.pagerank(g, alpha, personalization, max_iter, tol, nstart, weight, dangling)

    def hits(self, g, max_iter=100, tol=1e-08, nstart=None, normalized=True):
        hubs, authorities = nx.hits(g, max_iter, tol, nstart, normalized)
        return {
            "hub": hubs,
            "authorities": authorities,
        }

    def get_properties(self) -> dict:
        return {
            "properties": self.__data_dict,
            "communities": {
                "all": self.__communities,
                "best": self.__best_community
            },
            "pagerank": self.__pagerank,
            "hits": self.__hits
        }
