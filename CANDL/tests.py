import os
import sys
import dsd
import time
import verify
import numpy as np

"""----- Commonly used functions across several tests to prep the data ---- """

# announce: given string, prints time + string. 
def announce(message):
    print time.strftime('%H:%M:%S'),message
    sys.stdout.flush()

# Remaps index-to-name and name-to-index dictionaries in PPI 1 and PPI 2 
# for only the genes inside PPI_1_targets and PPI_2_targets, respectively.
# Uses order of PPI_1_targets and PPI_2_targets to define name-to-index
# and index-to-name mappings.
def reduce_nodeset(PPI_1_data, PPI_2_data, PPI_1_targets, PPI_2_targets):
    PPI_1_name_to_index_targets = {name:index for index, name in enumerate(PPI_1_targets)}
    PPI_1_index_to_name_targets = {index:name for name, index in PPI_1_name_to_index_targets.items()}
    PPI_2_name_to_index_targets = {name:index for index, name in enumerate(PPI_2_targets)}
    PPI_2_index_to_name_targets = {index:name for name, index in PPI_2_name_to_index_targets.items()}

    PPI_1_data.name_to_index = PPI_1_name_to_index_targets
    PPI_1_data.index_to_name = PPI_1_index_to_name_targets
    PPI_2_data.name_to_index = PPI_2_name_to_index_targets
    PPI_2_data.index_to_name = PPI_2_index_to_name_targets

    PPI_1_data.nodelist = PPI_1_targets
    PPI_2_data.nodelist = PPI_2_targets

    return PPI_1_data, PPI_2_data

# Reduces the rows of the hematrices in PPI 1 and PPI 2 to only contain
# genes named in PPI_1_targets and PPI_2_targets.
# Updates the name-to-index and index-to-name mappings associated with each PPI.
# Returns altered PPI-data objects.
def reduce_hematrices(PPI_1_data, PPI_2_data, PPI_1_targets, PPI_2_targets):
    PPI_1_targets_indices = [PPI_1_data.name_to_index[name] for name in PPI_1_targets]
    PPI_2_targets_indices = [PPI_2_data.name_to_index[name] for name in PPI_2_targets]
    
    # only maintain rows in the hematrices that correspond with
    # the target genes sets
    PPI_1_targets_hematrix = PPI_1_data.hematrix[PPI_1_targets_indices]
    PPI_2_targets_hematrix = PPI_2_data.hematrix[PPI_2_targets_indices]
 
    # updates the namedtuple to contain the reduced Hematrix and dictionary
    # mappings
    PPI_1_data, PPI_2_data = reduce_nodeset(PPI_1_data, PPI_2_data, PPI_1_targets, PPI_2_targets)
    PPI_1_data.hematrix = PPI_1_targets_hematrix
    PPI_2_data.hematrix = PPI_2_targets_hematrix

    return PPI_1_data, PPI_2_data

""" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Tests ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ """

def cDSD_full_graph_v_full_graph(PPI_1_data, PPI_2_data):
    announce("Preparing for crossDSD on full graphs")
    reciprocals   = zip(PPI_1_data.reciprocals, PPI_2_data.reciprocals)
    landmarks     = list(reciprocals)
    
    PPI_1_landmarks, PPI_2_landmarks = zip(*landmarks)
    PPI_1_targets = set(PPI_1_data.nodelist) - set(PPI_1_landmarks)
    PPI_2_targets = set(PPI_2_data.nodelist) - set(PPI_2_landmarks)
    
    PPI_1_landmark_indices = [PPI_1_data.name_to_index[n] for n in PPI_1_landmarks]
    PPI_2_landmark_indices = [PPI_2_data.name_to_index[n] for n in PPI_2_landmarks]

    PPI_1_data, PPI_2_data = reduce_hematrices(PPI_1_data, PPI_2_data, PPI_1_targets, PPI_2_targets)

    announce("Running crossDSD")
    cDSD    = dsd.crossDSD(PPI_1_data.hematrix, PPI_2_data.hematrix, PPI_1_landmark_indices, PPI_2_landmark_indices)
    
    matches = verify.full_graph_padded_hungarian(PPI_1_data, PPI_2_data, cDSD)
    return matches
