import unittest
import os
import graphanalysis.loader as loader


class GraphAnalysisLoaderTest(unittest.TestCase):
    def test_loader(self):
        dataset = "../resources/dataset/wiki-Vote.txt"

        exists = os.path.exists(dataset)
        self.assertTrue(exists, "{} does not exists".format(dataset))  # Check if we give the right path

        g = loader.load(dataset, is_directed=True)
        self.assertIsNotNone(g, "the graph cannot be None")

        expectedNodes = 7115  # Nodes contained in wiki-Vote.txt
        self.assertEqual(len(g.nodes()), expectedNodes,
                         "Missing some nodes. Found {}, expected {}".format(len(g.nodes), expectedNodes))
        expectedEdges = 103689  # Edges contained in wiki-Vote.txt
        self.assertEqual(len(g.edges()), expectedEdges,
                         "Missing some edges. Found {}, expected {}".format(len(g.edges), expectedEdges))
