#!/bin/env python2.7
import dsd
import networkx as nx
import numpy as np
import random
import argparse
import time
import collections
import sys
from inspect import getargspec
from os.path import basename
import tests
import math

"""
    - PPI1 and PPI2 are made of nodes which are GeneNames (strings)
    - given a GeneName we can look up its index in the HeMatrix because when
      we create the adjacency matrix with which we build the HeMatrix we use the
      nodeset ordering, which is created by the .nodes() functions which is a
      property of the nx graph.
        - Given a string we can find its index in the nodeset, which directly
          corresponds with its index in the HeMatrix.

- read in reciprocals
- parse two PPIs
    - construct nx graph
    - construct PPIData structure

"""

# PPI data NamedTuple used to organize PPI data:
# name_to_id and id_to_name are dictionaries mapping
# Entrez Gene ID strings (like '1977') to a unique
# number and vice versa. 

class PPIData:
    def __init__(self, name_to_index, index_to_name, reciprocals, graph,
                 nodelist, hematrix):
        self.name_to_index = name_to_index
        self.index_to_name = index_to_name
        self.reciprocals   = reciprocals
        self.graph         = graph
        self.nodelist      = nodelist
        self.hematrix      = hematrix

# announce: given string, prints time + string. 
def announce(message):
    print time.strftime('%H:%M:%S'),message
    sys.stdout.flush()

# exits program if there isn't a 1-1 mapping from
# network 1 to network 2's reciprocals. (Avoids duplicates)
def validate_reciprocals(paired_list):
    r1, r2 = zip(*paired_list)
    r1_duplicates = [x for x,y in collections.Counter(r1).items() if y > 1]
    r2_duplicates = [x for x,y in collections.Counter(r2).items() if y > 1]
    should_break = False

    if len(r1_duplicates) != 0: 
        announce("ERROR: Duplicates in network 1 landmark IDs: %s" % str(r1_duplicates))
        should_break = True
    if len(r2_duplicates) != 0:
        announce("ERROR: Duplicates in network 2 landmark IDs: %s" % str(r2_duplicates))
        should_break = True

    if should_break:
        announce("Fatal error, exiting")
        exit(1)

# reciprocals are read in as strings
def read_reciprocals(reciprocals_filename, PPI_1_nodelist, PPI_2_nodelist):
    # read in reciprocals from file as a list of pairs
    reciprocals = []
    for line in open(reciprocals_filename):
        reciprocals_temp = line.strip().split()
        reciprocals.append((reciprocals_temp[0], reciprocals_temp[1]))

    PPI_1_nodelist    = set(PPI_1_nodelist)
    PPI_2_nodelist    = set(PPI_2_nodelist)
    PPI_1_reciprocals = []
    PPI_2_reciprocals = []

    # only maintain reciprocals that exist across both of the PPI graphs
    # because we took the largest connected component of the graphs before
    # entering this function (which might have thrown some of the reciprocals
    # out

    validate_reciprocals(reciprocals)
    for rcp1, rcp2 in reciprocals: 
        if rcp1 in PPI_1_nodelist and rcp2 in PPI_2_nodelist:
            PPI_1_reciprocals.append(rcp1)
            PPI_2_reciprocals.append(rcp2)

    return PPI_1_reciprocals, PPI_2_reciprocals

# read_PPIs: reads PPIs from files, requires known reciprocals
# returns: a PPIData object for both PPIs. The name_to_id and 
# id_to_name objects do not overlap unique IDs, unless 
# the gene is a reciprocal.

def read_PPIs(PPI_1_filename, PPI_2_filename, reciprocals_filename, is_perturbation_test):
    # read PPI1 and PPI2 into nx graphs where the nodes are strings
    PPI_1_graph = nx.read_edgelist(PPI_1_filename, nodetype = str)
    PPI_2_graph = nx.read_edgelist(PPI_2_filename, nodetype = str)

    # create lists of strings that represent all the nodes in each PPI's graph
    PPI_1_nodelist = sorted(PPI_1_graph.nodes())
    PPI_2_nodelist = sorted(PPI_2_graph.nodes())

    # dictionaries that map Gene Names (strings) to their IDs, and vice versa
    PPI_1_name_to_index = {name:index for index, name in enumerate(PPI_1_nodelist)}
    PPI_1_index_to_name = {index:name for name, index in PPI_1_name_to_index.items()} 
    PPI_2_name_to_index = {name:index for index, name in enumerate(PPI_2_nodelist)}
    PPI_2_index_to_name = {index:name for name, index in PPI_2_name_to_index.items()} 

    if reciprocals_filename:
        announce("Reading in Provided Reciprocals")
        PPI_1_reciprocals, PPI_2_reciprocals = read_reciprocals(reciprocals_filename, PPI_1_nodelist, PPI_2_nodelist)
    else:
        announce("Generating Random Reciprocals")
        num_recips        = int(math.ceil(0.1 * len(PPI_1_nodelist)))
        PPI_1_reciprocals = random.sample(PPI_1_nodelist, num_recips)
        if is_perturbation_test:
            # since its perturbation, we will match each node with itself
            PPI_2_reciprocals = list(PPI_1_reciprocals)
        else:
            PPI_2_reciprocals = random.sample(PPI_2_nodelist, num_recips)

    # generate new class objects
    PPI_1_data = PPIData(PPI_1_name_to_index,
                         PPI_1_index_to_name,
                         PPI_1_reciprocals,
                         PPI_1_graph,
                         PPI_1_nodelist,
                         None) # the hematrix
    PPI_2_data = PPIData(PPI_2_name_to_index,
                         PPI_2_index_to_name,
                         PPI_2_reciprocals,
                         PPI_2_graph,
                         PPI_2_nodelist,
                         None) # the hematrix

    return PPI_1_data, PPI_2_data 

def read_HeMatrix(HeMatrix):
    return np.load(HeMatrix)

def calculate_HeMatrix(graph, nodelist, ppi_name, quiet):
    HeMatrix = dsd.hematrix(np.array(nx.adjacency_matrix(graph, nodelist).todense()))
    # saving compressed versions of Hematrices
    if not quiet:
        announce("Saving HeMatrix to File")
        # np.save("/data/ifried01/STRING/Perturbation_HeMatrices/" + basename(ppi_name) + ".hematrix", HeMatrix)
    return HeMatrix

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ppi_1",       help="edge list of graph 1")
    parser.add_argument("ppi_2",       help="edge list of graph 2")
    parser.add_argument("-hemat1",     help="hematrix of PPI 1 (Human)")
    parser.add_argument("-hemat2",     help="hematrix of PPI 2 (Mouse)")
    parser.add_argument("-reciprocals", help="reciprocals represented as list \
                                            of pairs: [ppi1_node]\t[ppi2_node]")
    parser.add_argument("-t","--test", required=True,
                                       help="name of function in test_suite/\
                                             tests.py to run. NOTE: only works\
                                             for single-run tests!")
    parser.add_argument("-o", required=True, help="output file for matches")
    parser.add_argument("-q", action='store_true', help="Do not save HeMatrices")
    parser.add_argument("-p", action='store_true', help="Tells program we are running a perturbation test")

    args = parser.parse_args()

    # populate data structures
    announce("Building PPIs from files")
    PPI_1_data, PPI_2_data = read_PPIs(args.ppi_1, args.ppi_2, args.reciprocals, args.p)
 
    if args.hemat1:
        announce("Reading in HeMatrix for PPI 1")
        PPI_1_hematrix = read_HeMatrix(args.hemat1)
    else:
        announce("Creating HeMatrix for PPI 1")
        PPI_1_hematrix = calculate_HeMatrix(PPI_1_data.graph,
                                            PPI_1_data.nodelist, args.ppi_1,
                                            args.q)
    if args.hemat2:
        announce("Reading in HeMatrix for PPI 2")
        PPI_2_hematrix = read_HeMatrix(args.hemat2)
    else:
        announce("Creating HeMatrix for PPI 2")
        PPI_2_hematrix = calculate_HeMatrix(PPI_2_data.graph,
                                            PPI_2_data.nodelist, args.ppi_2,
                                            args.q)

    PPI_1_data.hematrix = PPI_1_hematrix
    PPI_2_data.hematrix = PPI_2_hematrix

    # make sure user-desired test function exists
    try:
        test_function = getattr(tests, args.test)
    except AttributeError:
        announce("Error: tests module has no test named {}.".format(args.test))
        exit(1)
    announce("Running test {}".format(args.test))
    matches = test_function(PPI_1_data, PPI_2_data)
    outfile = open(args.o, 'w')
    for match in matches:
        outfile.write("{}\t{}\n".format(match[0], match[1]))
    landmarks = zip(PPI_1_data.reciprocals, PPI_2_data.reciprocals)
    for (p1, p2) in landmarks:
        outfile.write("{}\t{}\n".format(p1, p2))


if __name__ == "__main__":
    main()
