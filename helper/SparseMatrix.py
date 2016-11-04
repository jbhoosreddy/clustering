from utils import load_data
from utils import print_dict, print_list
from utils import distance
from copy import deepcopy
import sys
import itertools


class SparseMatrix(object):
    def __init__(self, data):
        self.id = 0
        self.data = data
        self.original = None
        self.matrix = None
        self.history = list()
        self.clusters = list()
        self.points = None
        self.create_matrix()

    def size(self):
        return len(self.matrix)

    def create_matrix(self):
        original = dict()
        matrix = dict()
        data = self.data
        ids = set(map(lambda x: x['id'], data))
        combinations = itertools.combinations(ids, 2)
        for combination in combinations:
            d = self.distance(combination)
            key = tuple(map(lambda c: (c,), combination))
            original[combination] = d
            matrix[key] = d
        self.matrix = matrix
        self.original = original
        self.points = set(map(lambda i: (i,), ids))

    def distance(self, combination):
        data = self.data
        filtered = filter(lambda d: d['id'] in combination, data)
        a1, a2 = filtered[0], filtered[1]
        return distance(a1, a2)

    def find(self, method="closest"):
        matrix = self.matrix
        if method == "closest":
            return min(matrix, key=matrix.get)
        elif method == "furthest":
            return max(matrix, key=matrix.get)

    def update(self, method="closest"):
        self.id += 1
        self.history.append(deepcopy(self.matrix))
        closest = self.find(method)
        for k in closest:
            self.points.remove(k)
            for key in self.matrix.keys():
                if k in key:
                    del self.matrix[key]
        cluster = tuple([item for sublist in closest for item in sublist])
        for p in self.points:
            d = self.find_distance(p, cluster)
            if not isinstance(p, tuple):
                p = (p,)
            self.matrix[(cluster, p)] = d
        self.points.add(cluster)

    def find_distance(self, p, cluster, method="closest"):
        original = self.original
        d = sys.maxint
        points = list(deepcopy(cluster))
        points.extend(p)
        points = list(points)

        combinations = itertools.combinations(points, 2)
        for combination in combinations:
            sub_permutation = itertools.permutations(combination, 2)
            for sub_subset in sub_permutation:
                should_continue = False
                for clusters in self.points:
                    if sub_subset[0] in clusters and sub_subset[1] in clusters:
                        should_continue = True
                        break
                if should_continue:
                    continue
                if sub_subset[0] in cluster and sub_subset[1] in cluster:
                    continue
                if sub_subset in original.keys():
                    den = original[sub_subset]
                    if method == "closest":
                        if den < d:
                            d = original[sub_subset]
                            break
                    elif method == "furthest":
                        if den > d:
                            d = original[sub_subset]
                            break
        return d

    def __repr__(self):
        matrix = self.matrix
        return print_dict(matrix, None, False)

    def __str__(self):
        matrix = self.matrix
        return print_dict(matrix, None, False)
