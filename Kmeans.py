from __future__ import division
import random
from operator import itemgetter
from copy import deepcopy

random.seed(0)

INPUT_FILE = 'cho.txt'
CLUSTERS = 5


def load_data(file_name):
    file = open(file_name)
    data = file.read()
    file.close()
    output = []
    for line in data.split("\n"):
        tokens = line.split("\t")
        output.append({
            'id': tokens[0],
            'truth': int(tokens[1]),
            'expressions': map(lambda x: float(x), tokens[2:]),
            'centroid': 0
        })
    return filter(lambda x: x['truth'] != -1, output)


def pick_random(l):
    return random.choice(l)


def print_list(l, c=None):
    for i in l:
        print i
        if c:
            c -= 1
            if not c:
                break


def distance(a1, a2):
    a1, a2, l = list(a1['expressions']), list(a2['expressions']), len(a1['expressions'])
    return pow(reduce(lambda x, y: x+y, map(lambda i: pow(a1[i]-a2[i], l), xrange(l))), (1/l))


def compute_distance(centroids, data):
    for d in data:
        d['centroid'] = min(enumerate(map(lambda c: distance(d, c), centroids)), key=itemgetter(1))[0]


def intial_centroids(data):
    centroids = list()
    while len(centroids) < CLUSTERS:
        picked = pick_random(data)
        if not len(filter(lambda c: c['id'] == picked['id'], centroids)):
            centroids.append(picked)
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
    length = len(filter(lambda i: comparing(prev[i]['centroid'], next[i]['centroid']), xrange(len(prev))))
    return length == 0


def comparing(p_centroid, n_centroid):
    return p_centroid != n_centroid


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
