import hungarian
import numpy as np
import math
import time
import sys
import matplotlib.mlab as mlab

# announce: given string, prints time + string. 
def announce(message):
    print time.strftime('%H:%M:%S'),message
    sys.stdout.flush()

# row_hungarian: takes cDSD matrix, returns the 
# row-wise hungarian matches as a list of tuples (?).
def row_hungarian(cDSD):
    return hungarian.lap(cDSD)[0]

def full_graph_padded_hungarian(PPI_1_data, PPI_2_data, cDSD):
    announce("Running Full Graph Padded Hungarian Matching")
    rows, cols  = cDSD.shape
    max_element = np.amax(cDSD)
    insert_val  = max_element + 100 # chosen arbitrarily
    
    max_dimension = 0
    if rows < cols:
        cDSD = np.lib.pad(cDSD, ((0,(cols - rows)), (0,0)), 'constant', constant_values=(int(math.ceil(insert_val))))
    else: # rows > cols
        cDSD = np.lib.pad(cDSD, ((0,0), (0,(rows - cols))), 'constant', constant_values=(int(math.ceil(insert_val))))

    assert(cDSD.shape[0] == cDSD.shape[1])
    row_major_matches  = row_hungarian(cDSD)
    row_col_matches    = enumerate(row_major_matches)
    matches            = []
    for row, col in row_col_matches:
        # we must ensure that we only look at matches
        # of "real"rows and columns, not padded ones
        if row >= rows: 
            # means that the padding is in the form of additional rows,
            # so the column is an unmatched PPI2 gene
            print "PPI_2 unmatched: {}".format(PPI_2_data.index_to_name[col])
            continue 
        elif col >= cols:
            # means that the padding is in the form of additional columns, 
            # so the row is an unmatched PPI 1 gene.
            print "PPI_1 unmatched: {}".format(PPI_1_data.index_to_name[row])
            continue
        else:
            r1 = PPI_1_data.index_to_name[row]
            r2 = PPI_2_data.index_to_name[col]
            matches.append((r1, r2))
    return matches

def padded_hungarian(cDSD):
    """
    RETURNS INDICES NOT NAMES
    """
    rows, cols  = cDSD.shape
    max_element = np.amax(cDSD)
    insert_val  = max_element + 100 # chosen arbitrarily
    
    max_dimension = 0
    if rows < cols:
        cDSD = np.lib.pad(cDSD, ((0,(cols - rows)), (0,0)), 'constant', constant_values=(int(math.ceil(insert_val))))
    else: # rows > cols
        cDSD = np.lib.pad(cDSD, ((0,0), (0,(rows - cols))), 'constant', constant_values=(int(math.ceil(insert_val))))

    assert(cDSD.shape[0] == cDSD.shape[1])

    return row_hungarian(cDSD)
    

# selects the index with the smallest value in a row as the match
def greedy_linear(cDSD):
    unverified_matches = []
    used_names         = []
    verified_matches   = []
    for i in xrange(0, cDSD.shape[0]):
        for j in xrange(0, cDSD.shape[1]):
            dream = (i, j, cDSD[i][j])
            unverified_matches.append(dream)

    # sort by the cDSD matrix score for the pair
    unverified_matches.sort(key=lambda x: x[2])
    # confirm the pair with the lowest global score
    for i, j, score in unverified_matches:
        if i not in used_names and j not in used_names:
            match = unverified_matches.pop(0)
            verified_matches.append((match[0], match[1]))
            used_names.append(i)
            used_names.append(j)
    return verified_matches
            
# assumes PPI_1 is across the rows and PPI_2 is across the columns
def correctMatches_Greedy(PPI_1_data, PPI_2_data, cDSD):
    announce("Running Greedy Matching")
    row_col_matches    = greedy_linear(cDSD)
    reciprocals        = zip(PPI_1_data.reciprocals, PPI_2_data.reciprocals)
    successful_matches = []
    for row, col in row_col_matches:
        r1 = PPI_1_data.index_to_name[row]
        r2 = PPI_2_data.index_to_name[col]
        if (r1, r2) in reciprocals:
            successful_matches.append((r1, r2))
    
    return successful_matches

# correctMatches: given a cDSD matrix and list of pairs 
# of reciprocal genes (by indices in cDSD matrix), 
# returns the correctly matched pairs of reciprocal 
# genes.

# assumes PPI_1 is across the rows and PPI_2 is across the columns
def correctMatches_Hungarian(PPI_1_data, PPI_2_data, cDSD):
    announce("Running Hungarian Matching")
    row_major_matches  = row_hungarian(cDSD)
    row_col_matches    = enumerate(row_major_matches)
    reciprocals        = zip(PPI_1_data.reciprocals, PPI_2_data.reciprocals)
    successful_matches = []
    for row, col in row_col_matches:
        r1 = PPI_1_data.index_to_name[row]
        r2 = PPI_2_data.index_to_name[col]
        if (r1, r2) in reciprocals:
            successful_matches.append((r1, r2))
    
    return successful_matches

# Runs the hungarian matching algorithm on a non-square matrix by
# padding the matrix (forcing it to be square) by adding rows or columns
# of "infinity" values
def correctMatches_Rectangle(PPI_1_data, PPI_2_data, cDSD):
    announce("Running Rectangle Matching")
    rows, cols  = cDSD.shape
    max_element = np.amax(cDSD)
    insert_val  = max_element + 100 # chosen arbitrarily
    
    max_dimension = 0
    if rows < cols:
        cDSD = np.lib.pad(cDSD, ((0,(cols - rows)), (0,0)), 'constant', constant_values=(int(math.ceil(insert_val))))
    else: # rows > cols
        cDSD = np.lib.pad(cDSD, ((0,0), (0,(rows - cols))), 'constant', constant_values=(int(math.ceil(insert_val))))

    assert(cDSD.shape[0] == cDSD.shape[1])
    row_major_matches  = row_hungarian(cDSD)
    row_col_matches    = enumerate(row_major_matches)
    reciprocals        = zip(PPI_1_data.reciprocals, PPI_2_data.reciprocals)
    successful_matches = []
    for row, col in row_col_matches:
        # we must ensure that we only look at matches
        # of "real"rows and columns, not padded ones
        if row >= rows: 
            # means that the padding is in the form of additional rows,
            # so the column is an unmatched PPI2 gene
            print "PPI_2 unmatched: {}".format(PPI_2_data.index_to_name[col])
            continue 
        elif col >= cols:
            # means that the padding is in the form of additional columns, 
            # so the row is an unmatched PPI 1 gene.
            print "PPI_1 unmatched: {}".format(PPI_1_data.index_to_name[row])
            continue
        else:
            r1 = PPI_1_data.index_to_name[row]
            r2 = PPI_2_data.index_to_name[col]
        
        if (r1, r2) in reciprocals:
            successful_matches.append((r1, r2))
#    print "rows: {} cols {}".format(rows, cols)
    return successful_matches

def match_edges(row_col_matches, PPI_1_data, PPI_2_data):
    match_count = 0 

    for u, v in PPI_1_data.graph.edges():
        try:
            if PPI_2_data.graph.has_edge(row_col_matches[u], row_col_matches[v]):
                match_count += 1
        except KeyError:
            continue

    return match_count

    

def edgeMatching(PPI_1_data, PPI_2_data, cDSD):
    """
        Edge matching is defined as follows:
            Let e be an edge in graph A, with endpoints 1 and 2
            Using any mapping of nodes in A to nodes in B (in this example
            we use the Hungarian algorithm), we map nodes 1 and 2 to their 
            corresponding counterparts in B, call them 1' and 2'. 

            If there exists an edge (1',2') in B, it is a match.
    """
    hungarian = padded_hungarian(cDSD)
    match     = {PPI_1_data.index_to_name[i]:PPI_2_data.index_to_name[j]
                       for i, j in enumerate(hungarian)}
    match_count = match_edges(match, PPI_1_data, PPI_2_data)

def inducedCorrectness(PPI_1_data, PPI_2_data, cDSD):
    match = padded_hungarian(cDSD)
    match_names = {}
    for m1, m2 in enumerate(match):
        try:
            match_names[PPI_1_data.index_to_name[m1]] = PPI_2_data.index_to_name[m2]
        except KeyError: 
            print "skipping out-of-bounds match"

    match_count = match_edges(match_names, PPI_1_data, PPI_2_data)

    us, vs = zip(*match_names.items())
    Induced = PPI_2_data.graph.subgraph(vs)
    return float(match_count) / float(Induced.number_of_edges())   
    

def verifyMatches(PPI_1_data, PPI_2_data, row_col_matches, cDSD):
    rows, cols  = cDSD.shape
    reciprocals = zip(PPI_1_data.reciprocals, PPI_2_data.reciprocals)
    successful_matches = []
    for row, col in row_col_matches:
        # we must ensure that we only look at matches
        # of "real"rows and columns, not padded ones
        if row >= rows: 
            # means that the padding is in the form of additional rows,
            # so the column is an unmatched PPI2 gene
            print "PPI_2 unmatched: {}".format(PPI_2_data.index_to_name[col])
            continue 
        elif col >= cols:
            # means that the padding is in the form of additional columns, 
            # so the row is an unmatched PPI 1 gene.
            print "PPI_1 unmatched: {}".format(PPI_1_data.index_to_name[row])
            continue
        else:
            r1 = PPI_1_data.index_to_name[row]
            r2 = PPI_2_data.index_to_name[col]
        
        if (r1, r2) in reciprocals:
            successful_matches.append((r1, r2))
#    print "rows: {} cols {}".format(rows, cols)
    
    return successful_matches

def precision_and_recall(num_successful_matches, num_targets, num_matches):
    # number of relevant records retrieved
    A = num_successful_matches
    # number of relevant records not retrieved
    B = num_targets - num_successful_matches
    # number of irrelevant records retrieved
    C = num_matches - num_successful_matches
    
    precision  = float(A) / float((A + C))
    recall     = float(A) / float((A + B))

    return precision, recall

def bestRankMatch(D,k):
    # a is a list of indices, sorted, into matrix D.
    # code returns a list of best rank-match indices.
    a = np.argsort(D,axis=1)
    return [set(a[i,0:k]) for i in range(np.shape(D)[0])]

def recipMatch(cDSD, k):
    num_rows = cDSD.shape[0]
    num_cols = cDSD.shape[1]
    n = num_rows
    row_matches = bestRankMatch(cDSD, k)
    col_matches = bestRankMatch(cDSD.T, k)

    bothMatch = [[(j in row_matches[i])&(i in col_matches[j]) for j in xrange(num_cols)] for i in xrange(num_rows)]
    
    r, c = np.unravel_index(mlab.find(bothMatch),np.shape(bothMatch))
    return [[r[i],c[i]] for i in xrange(len(r))]


# NOTE: this function DOES NOT produce duplicate node matches. 
# Every node is mentioned exactly once in the match set. 
def recipMatchCorrect(PPI_1_data, PPI_2_data, cDSD, k, num_targets):
    matches            = recipMatch(cDSD, k)
    nodes_seen = set()
    matches_unique = []
    for m1, m2 in matches:
        if m1 not in nodes_seen and m2 not in nodes_seen:
            matches_unique.append((m1,m2))
        nodes_seen.update([m1, m2])

    successful_matches = verifyMatches(PPI_1_data, PPI_2_data, matches_unique, cDSD)
    precision, recall  = precision_and_recall(len(successful_matches), num_targets, len(matches_unique))
    print "Precision %.4f and Recall %.4f" %(precision, recall)

    return successful_matches
