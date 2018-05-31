import networkx as nx
import copy

def generate_target_set_selection(g: nx.Graph, threshold):
    target_set = set()
    thresholds = dict()
    graph = copy.deepcopy(g)

    if type(threshold) == dict:
        for th in threshold:
            if th not in graph.nodes:
                raise ValueError("Wrong key in threshold")
        thresholds = copy.deepcopy(threshold)
    else:
        thresholds = {node: threshold for node in graph.nodes}

    while len(graph.nodes) != 0:
        # first case
        empty_threshold_nodes = list(filter(lambda n: thresholds[n] == 0, graph.nodes))
        if len(empty_threshold_nodes) > 0:
            for node in empty_threshold_nodes:
                for neighbor in graph.neighbors(node):
                    thresholds[neighbor] = max(thresholds[neighbor] - 1, 0)

            graph.remove_nodes_from(empty_threshold_nodes)
        else:
            # second case
            high_threshold_node = max(graph.nodes, key=lambda n: thresholds[n] - graph.degree[n])
            if thresholds[high_threshold_node] > graph.degree[high_threshold_node]:
                target_set.add(high_threshold_node)
                for neighbor in graph.neighbors(high_threshold_node):
                    thresholds[neighbor] = thresholds[neighbor] - 1
                graph.remove_node(high_threshold_node)
            else:
                # third case
                v = max(graph.nodes, key=lambda n: thresholds[n] / (graph.degree[n] * (graph.degree[n] + 1)))
                graph.remove_node(v)

    return target_set
