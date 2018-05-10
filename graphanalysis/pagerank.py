import networkx as nx


def run_pagerank(g: nx.Graph, alpha: float, pers: dict, max_iter: int, tol: float) -> dict:
    return nx.pagerank(g, alpha, pers, max_iter, tol)


def run_pagerank_default(g: nx.Graph) -> dict:
    return nx.pagerank(g)
