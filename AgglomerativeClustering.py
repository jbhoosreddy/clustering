'''
--> read input file and create a n X n distance matrix
--> find points / clusters with shortest distance in matrix
--> merge those clusters & recompute the distance matrix
--> repeat till single cluster left in matrix
'''

from __future__ import division
from helper import load_data, print_list, print_dict, distance as _distance
from copy import deepcopy
import itertools
import sys

INPUT_FILE = 'cho.txt'
CLUSTERS = 5


def distance(combination, data):
    filtered = filter(lambda d: d['id'] in combination, data)
    a1, a2 = filtered[0], filtered[1]
    return _distance(a1, a2)


def create_initial_matrix(data):
    matrix = dict()
    ids = set(map(lambda x: x['id'], data))
    combinations = itertools.combinations(ids, 2)
    for combination in combinations:
        matrix[combination] = distance(combination, data)
    return matrix, ids


def find_closest(matrix):
    return min(matrix, key=matrix.get)


def find_min_distance(matrix, newSet):

    d = sys.maxint
    den = 0
    combinations = itertools.combinations(newSet,2)
    for combination in combinations:
        sub_permutation = itertools.permutations(combination, 2)
        for sub_subset in sub_permutation:
            #print sub_subset
            #subset_key = ','.join(sub_subset)
            if sub_subset in matrix.keys():
                den = matrix[sub_subset]
                #print den
                break

        if(den < d):
            d = matrix[sub_subset]

    return d


def update_matrix(initial_matrix, matrix, closest, id_set):

    print 'closest points' , closest
    newMatrix = deepcopy(matrix)
    #cluster = ','.join(closest)
    #print type(cluster)
    del newMatrix[closest] # delete the closest point distance from the matrix

    print 'delete complete'
    newSet = list(closest)
    for key in id_set:
        new_tuple = tuple(newSet)
        newSet.append(key)
        dist = find_min_distance(initial_matrix, new_tuple)
        newMatrix[new_tuple] = dist

    return newMatrix


if __name__ == "__main__":
    data = load_data(INPUT_FILE)
    prev = deepcopy(data)
    initial_matrix, id_set = create_initial_matrix(data)
    print 'id length', len(id_set)
    matrix = deepcopy(initial_matrix)
    matrix_list = list()
    iteration = 0
    matrix_list.append(matrix)
    while len(id_set) > 1:
        closest = find_closest(matrix)
        for id in closest:
            if id in id_set:
                id_set.remove(id)
        matrix = update_matrix(initial_matrix, matrix, closest, id_set)
        matrix_list.append(matrix)
    # clusterSet = dict()
    # iteration = 0
    # clusterSet[iteration] = matrix
    # while len(id_set) > 1:
    #     iteration += 1
    #     print 'iteration ', iteration, ' length ', len(matrix)
    #     closest = find_closest(matrix)
    #     for id in closest:
    #         if id in id_set:
    #             id_set.remove(id)
    #     print 'id length', len(id_set)
    #     matrix = update_matrix(initial_matrix, matrix, closest, id_set)
    #     clusterSet[iteration] = deepcopy(matrix)
    #
    # print len(clusterSet)