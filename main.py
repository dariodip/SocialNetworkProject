import graphanalysis.loader as loader
import graphanalysis.graphanalyser as ga
import os
import logging
import pandas as pd
import json

from graphanalysis import influence
from graphanalysis.powerlaw import plot_degree_powerlaw_distribution

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':

    graph_path = './resources/dataset/'

    for file in [f for f in os.listdir(graph_path) if f.startswith('CA-Gr')]:
        graph_name = file.split('.')[0]
        full_graph_path = os.path.join('.', 'resources', 'dataset', file)
        logger.info("Loading " + graph_name)
        g = loader.load(full_graph_path, is_directed=False, sep="\t")
        logger.info("Starting analysis on " + graph_name)
        graph_dict = ga.GraphAnalyser(g).get_properties()

        influence_dict = dict()
        logger.info("Influence Targer Set Selection on median on " + graph_name)
        influence_dict['Median'] = list(influence.generate_target_set_selection(g, graph_dict['properties']['Median']))
        logger.info("Influence Targer Set Selection on 60th percentile on " + graph_name)
        influence_dict['60th Percentile'] = list(influence.generate_target_set_selection(g, graph_dict['properties']['60th Percentile']))
        logger.info("Influence Targer Set Selection on 70th percentile on " + graph_name)
        influence_dict['70th Percentile'] = list(influence.generate_target_set_selection(g, graph_dict['properties']['70th Percentile']))

        graph_dict['target set'] = influence_dict

        # Powerlaw graph
        logger.info("Plotting Power Law")
        plot_degree_powerlaw_distribution(g, graph_name)

        with open('./resources/results/{}.json'.format(graph_name), 'w+') as f:
            json.dump(graph_dict, f, indent=0)
            logger.info("dirty-{}.json saved".format(graph_name))

