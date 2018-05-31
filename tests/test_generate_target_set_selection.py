import networkx as nx

from unittest import TestCase
from graphanalysis import influence


class TestGenerate_target_set_selection(TestCase):
    def test_generate_target_set_selection(self):
        g = nx.Graph()
        g.add_edges_from([(1, 4), (1, 5), (2, 4), (3, 4), (3, 5), (4, 5)])

        expected = {2, 3}
        target_set = influence.generate_target_set_selection(g, 2)
        self.assertSetEqual(expected, target_set,
                            "Wrong target set. Found {}, expected {}.".format(expected, target_set))
