import json
import networkx as nx
import community
import numpy as np

from networkx.algorithms import cluster


class GraphAnalyser(object):

    def __init__(self, g: nx.Graph):
        self.__g = g
        self.__data_dict = dict()
        self.__communities = dict()
        self.__pagerank = dict()
        self.__hits = dict()
        self.__conn_comp = list()
        self.__bridges = list()
        self.__local_bridges = list()
        self.__neigh_overlap = dict()
        self.__clustering_coefficients = dict()

        if nx.is_directed(self.__g):
            self.__data_dict['Type'] = "Directed"
            self.__data_dict['Connected'] = nx.is_strongly_connected(self.__g)
        else:
            self.__data_dict['Type'] = "Undirected"
            self.__data_dict['Connected'] = nx.is_connected(self.__g)

        self.__degree_stats()
        self.__graph_props()
        self.__basic_info()
        self.__communities_props()
        self.__link_analysis()
        self.__connected_components()

        if self.__data_dict["Type"] == "Undirected":
            self.__find_bridges_overlap()

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
        degree_variance = sum(map(lambda x: (x - avg_degree)**2, degrees)) / len(degrees)
        self.__data_dict['Max Degree'] = max_degree
        self.__data_dict['Max Degree Id'] = max_degree_name
        self.__data_dict['Min Degree'] = min_degree
        self.__data_dict['Min Degree Id'] = min_degree_name
        self.__data_dict['Avg Degree'] = avg_degree
        self.__data_dict['Degree variance'] = degree_variance
        degrees_array = np.array(degrees)
        self.__data_dict['Median'] = np.ceil(np.percentile(degrees_array, 50))
        self.__data_dict['60th Percentile'] = np.ceil(np.percentile(degrees_array, 60))
        self.__data_dict['70th Percentile'] = np.ceil(np.percentile(degrees_array, 70))

    def __graph_props(self):
        if self.__data_dict["Connected"]:
            self.__data_dict['Diameter'] = nx.diameter(self.__g)
            self.__data_dict['Radius'] = nx.radius(self.__g)
            self.__data_dict["Centered nodes"] = list(nx.center(self.__g))
        else:
            self.__data_dict['Diameter'] = None
            self.__data_dict['Radius'] = None
            self.__data_dict["Centered nodes"] = []

        if self.__data_dict["Type"] == "Undirected":
            self.__data_dict['Average Clustering'] = nx.average_clustering(self.__g)
            self.__clustering_coefficients = cluster.clustering(self.__g)
        else:
            self.__data_dict['Average Clustering'] = None


    def __communities_props(self):
        self.__communities = community.best_partition(nx.to_undirected(self.__g))
        self.__data_dict["Communities count"] = len(set(self.__communities.values()))

    def __link_analysis(self):
        self.__pagerank = self.pagerank(self.__g)
        self.__hits = self.hits(self.__g)

    def __connected_components(self):
        if self.__data_dict["Type"] == "Directed":
            self.__conn_comp = list(map(list, nx.strongly_connected_components(self.__g)))
        else:
            self.__conn_comp = list(map(list, nx.connected_components(self.__g)))

    def pagerank(self, g, alpha=0.85, personalization=None, max_iter=100, tol=1e-06, nstart=None, weight='weight',
                 dangling=None):
        return nx.pagerank(g, alpha, personalization, max_iter, tol, nstart, weight, dangling)

    def hits(self, g, max_iter=100, tol=1e-08, nstart=None, normalized=True):
        hubs, authorities = nx.hits(g, max_iter, tol, nstart, normalized)
        return {
            "hub": hubs,
            "authorities": authorities,
        }

    def __find_bridges_overlap(self):
        if nx.is_directed(self.__g):
            raise TypeError("Not implemented for directed graphs")

        self.__bridges = list(nx.bridges(self.__g))
        for edge in self.__g.edges:
            n1, n2 = edge[0], edge[1]

            comm_neighbors = len(list(nx.common_neighbors(self.__g, n1, n2)))
            if comm_neighbors == 0:
                self.__local_bridges.append(edge)

            neighbor_n1 = set(self.__g.neighbors(n1))
            neighbor_n2 = set(self.__g.neighbors(n2))

            total_neighbors = len(neighbor_n1 | neighbor_n2)
            self.__neigh_overlap["{}-{}".format(n1, n2)] = comm_neighbors / total_neighbors

    def get_properties(self) -> dict:
        toReturn = {
            "properties": self.__data_dict,
            "communities": self.__communities,
            "connected components": self.__conn_comp,
            "bridges": self.__bridges,
            "local bridges": self.__local_bridges,
            "neighborhood overlap": self.__neigh_overlap,
            "pagerank": self.__pagerank,
            "hits": self.__hits,
            "clustering coefficients": self.__clustering_coefficients,
        }

        return toReturn

    def save_props(self, filename):
        with open(filename, "w") as f:
            json.dump(self.get_properties(), f)
