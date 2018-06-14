import networkx as nx
import os


def load(path: str, is_directed: bool, sep='\t', comm='#') -> nx.Graph:
    if not os.path.exists(path):
        raise FileNotFoundError
    props = {'create_using': nx.Graph() if not is_directed else nx.DiGraph(),
             'comments': comm,
             'delimiter': sep}
    g = nx.read_edgelist(path=path, **props)
    return g
