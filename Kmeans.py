from __future__ import division
from operator import itemgetter
from copy import deepcopy
from helper import load_data, print_list, pick_random


INPUT_FILE = 'cho.txt'
CLUSTERS = 5


def distance(a1, a2):
    a1, a2, l = list(a1['expressions']), list(a2['expressions']), len(a1['expressions'])
    return pow(reduce(lambda x, y: x+y, map(lambda i: pow(a1[i]-a2[i], l), xrange(l))), (1/l))


def compute_distance(centroids, data):
    for d in data:
        d['centroid'] = min(enumerate(map(lambda c: distance(d, c), centroids)), key=itemgetter(1))[0]


def intial_centroids(data):
    centroids = list()
    i = 1
    while len(centroids) < CLUSTERS:
        picked = pick_random(data, i)
        if not len(filter(lambda c: c['id'] == picked['id'], centroids)):
            centroids.append(picked)
            i += 1
    return centroids


def compute_centroids(data):
    centroids = list()
    for i in xrange(CLUSTERS):
        filtered = filter(lambda d: d['centroid'] == i, data)
        expressions = map(lambda f: f['expressions'], filtered)
        centroid = compute_centroid(expressions)
        centroid['centroid'] = i
        centroids.append(centroid)
    return centroids


def compute_centroid(expressions):
    centroid = dict()
    centroid['expressions'] = list()
    length = len(expressions)
    for i in range(len(expressions[0])):
        s = 0
        for expression in expressions:
            s += expression[i]
        s /= length
        centroid['expressions'].append(s)
    return centroid


def converged(prev, next):
    length = len(filter(lambda i: prev[i]['centroid'] != next[i]['centroid'], xrange(len(prev))))
    return length == 0


if __name__ == "__main__":
    # delta = list()
    data = load_data(INPUT_FILE)
    prev = deepcopy(data)
    centroids = intial_centroids(data)
    print_list(centroids)
    # print_list(data, 1)
    compute_distance(centroids, data)
    # print_list(data)
    i = 0
    while not converged(prev, data):
        i += 1
        print "Iteration:", i
        centroids = compute_centroids(data)
        print_list(centroids)
        prev = deepcopy(data)
        compute_distance(centroids, data)
    print data
