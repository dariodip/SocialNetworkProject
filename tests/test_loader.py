import unittest
import os
import graphanalysis.loader as loader


class GraphAnalysisLoaderTest(unittest.TestCase):
    def test_loader(self):
        dataset = "resources/dataset/CA-GrQc.txt"

        exists = os.path.exists(dataset)
        self.assertTrue(exists, "{} does not exists".format(dataset))  # Check if we give the right path

        g = loader.load(dataset, is_directed=False)
        self.assertIsNotNone(g, "the graph cannot be None")

        expectedNodes = 5242  # Nodes contained in wiki-Vote.txt
        self.assertEqual(len(g.nodes()), expectedNodes,
                         "Missing some nodes. Found {}, expected {}".format(len(g.nodes), expectedNodes))
        expectedEdges = 14496  # Edges contained in wiki-Vote.txt
        self.assertEqual(len(g.edges()), expectedEdges,
                         "Missing some edges. Found {}, expected {}".format(len(g.edges), expectedEdges))

        g = loader.load(dataset, is_directed=True)

        self.assertEqual(len(g.nodes()), expectedNodes,
                         "Missing some nodes. Found {}, expected {}".format(len(g.nodes), expectedNodes))
        # if we suppose that CA-GrQc is directed, then each edge must be counted twice
        expectedDirectedEdges = 28980
        self.assertEqual(len(g.edges()), expectedDirectedEdges,
                         "Missing some edges. Found {}, expected {}".format(len(g.edges), expectedEdges))
