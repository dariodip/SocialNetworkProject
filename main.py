import graphanalysis.loader as loader
import graphanalysis.graphanalyser as ga
import os
import logging
import pandas as pd
from pandas.io.json import json_normalize
import json
from concurrent.futures import ProcessPoolExecutor, as_completed
import traceback

from graphanalysis import influence
from graphanalysis.powerlaw import plot_degree_powerlaw_distribution

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def clear_dict(d):
    nd = dict()
    nd["Nodes"] = d["properties"]["Nodes"]
    nd["Edges"] = d["properties"]["Edges"]
    nd["Directed/Undirected"] = d["properties"]["Type"]
    nd["Connected"] = d["properties"]["Connected"]
    nd["Communities Count"] = d["properties"]["Communities count"]
    nd["Self Loops"] = d["properties"]["Self Loops"]
    nd["Diameter"] = d["properties"]["Diameter"]
    nd["Radius"] = d["properties"]["Radius"]
    nd["Centered Nodes Count"] = len(d["properties"]["Centered nodes"])
    nd["Max Degree"] = d["properties"]["Max Degree"]
    nd["Min Degree"] = d["properties"]["Min Degree"]
    nd["Avg Degree"] = round(d["properties"]["Avg Degree"], 3)
    nd["Degree Variance"] = round(d["properties"]["Degree variance"], 3)
    nd["Max Degree Id"] = d["properties"]["Max Degree Id"]
    nd["Min Degree Id"] = d["properties"]["Max Degree Id"]
    nd["Degree Median"] = d["properties"]["Median"]
    nd["Degree 60th Percentile"] = int(d["properties"]["60th Percentile"])
    nd["Degree 70th Percentile"] = int(d["properties"]["70th Percentile"])
    nd["Max Clustering"] = round(max(d["clustering coefficients"].values()), 3)
    nd["Min Clustering"] = round(min(d["clustering coefficients"].values()), 3)
    nd["Average Clustering"] = round(d["properties"]["Average Clustering"], 3)
    nd["Bridges Count"] = len(d["bridges"])
    nd["Target Set Count Median"] = len(d["target set"]["Median"])
    nd["Target Set Count 60th Perc"] = len(d["target set"]["60th Percentile"])
    nd["Target Set Count 70th Perc"] = len(d["target set"]["70th Percentile"])
    nd["Hits-Hub Min"] = min(d["hits"]["hub"].values())
    nd["Hits-Hub Max"] = max(d["hits"]["hub"].values())
    nd["Hits-Hub Avg"] = sum(d["hits"]["hub"].values())/len(d["hits"]["hub"])
    nd["Hits-Authorities Min"] = min(d["hits"]["authorities"].values())
    nd["Hits-Authorities Max"] = max(d["hits"]["authorities"].values())
    nd["Hits-Authorities Avg"] = sum(d["hits"]["authorities"].values())/len(d["hits"]["authorities"])
    nd["Connected Components Count"] = len(d["connected components"])
    nd["Pagerank Max"] = max(d["pagerank"].values())
    nd["Pagerank Max Id"] = max(d["pagerank"], key=d["pagerank"].get)
    nd["Pagerank Min"] = min(d["pagerank"].values())
    nd["Pagerank Min Id"] = min(d["pagerank"], key=d["pagerank"].get)
    nd["Pagerank Avg"] = sum(d["pagerank"].values())/len(d["pagerank"])
    return nd


def create_dataframe(d):
    nds = pd.DataFrame()
    for k, v in d.items():
        nv = v
        nv["Name"] = k
        nds = nds.append(json_normalize(v))
    return nds.transpose()


def get_stats(file):
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
    influence_dict['60th Percentile'] = list(
        influence.generate_target_set_selection(g, graph_dict['properties']['60th Percentile']))
    logger.info("Influence Targer Set Selection on 70th percentile on " + graph_name)
    influence_dict['70th Percentile'] = list(
        influence.generate_target_set_selection(g, graph_dict['properties']['70th Percentile']))
    graph_dict['target set'] = influence_dict
    # Powerlaw graph
    logger.info("Plotting Power Law")
    return g, graph_name, graph_dict, clear_dict(graph_dict)


def write_to_file(g, graph_name, graph_dict):
    plot_degree_powerlaw_distribution(g, graph_name)
    with open('./resources/results/{}.json'.format(graph_name), 'w+') as f:
        json.dump(graph_dict, f, indent=0)
        logger.info("dirty-{}.json saved".format(graph_name))



def main():
    graph_path = './resources/dataset/'
    tasks = dict()
    cleared_dicts = dict()
    with ProcessPoolExecutor(max_workers=3) as executor:
        files = [f for f in os.listdir(graph_path)]
        for file in files:
            task = executor.submit(get_stats, file)
            tasks[task] = file
        for future in as_completed(tasks):
            g = tasks[future]
            try:
                g, graph_name, graph_dict, cleared_dict = future.result()
            except Exception as ex:
                print('%r generated an exception: %s' % (g, ex))
                traceback.print_exc(ex)
            else:
                write_to_file(g, graph_name, graph_dict)
                cleared_dicts[graph_name] = cleared_dict

    create_dataframe(cleared_dicts).to_latex("table.tex")


if __name__ == '__main__':

    main()
