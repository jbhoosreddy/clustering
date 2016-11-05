from __future__ import division
from operator import itemgetter
from scipy.spatial import distance_matrix
from scipy.sparse.csgraph import laplacian
from scipy.sparse.linalg import eigs
from copy import deepcopy
from helper.validation import jaccard_coefficient
from helper.graph import plot
from helper.utils import load_data, pick
import time

iterations = None

filename = 'new_dataset_1'
# IDS = "1,68,203,278,332"
# IDS = "2,102,263,301,344,356,394,411,474,493"
IDS = "1,10,20"
# IDS = "1,4"
INPUT_FILE = 'data/'+filename+'.txt'
IDS = IDS.split(',')
CLUSTERS = len(IDS)
start = time.time()
data = load_data('data/' + filename + '.txt')

points = map(lambda d: d['expressions'], data)
matrix = distance_matrix(points, points, p=2)
laplacian_matrix = laplacian(matrix)

vals, vecs = eigs(laplacian_matrix, k=3)
# for i in xrange(len(data)):
#     data[i]['expressions'] = vecs[i]


def distance(a1, a2):
    l = len(a1)
    p = 2
    return pow(reduce(lambda x, y: x+y, map(lambda i: pow(a1[i]-a2[i], p), xrange(l))), (1/p))


def compute_distance(centroids, data):
    for d in data:
        d['cluster'] = min(enumerate(map(lambda c: distance(d['expressions'], c['expressions']), centroids)), key=itemgetter(1))[0] + 1


def intial_centroids(data):
    centroids = list()
    while len(centroids) < CLUSTERS:
        for i in IDS:
            picked = pick(data, i)
            centroids.append(picked)
    return centroids


def compute_centroids(data):
    centroids = list()
    for i in xrange(CLUSTERS):
        filtered = filter(lambda d: d['cluster'] == i+1, data)
        expressions = map(lambda f: f['expressions'], filtered)
        centroid = compute_centroid(expressions)
        centroid['cluster'] = i+1
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
    length = len(filter(lambda i: prev[i]['cluster'] != next[i]['cluster'], xrange(len(prev))))
    return length == 0


original = deepcopy(data)
prev = deepcopy(data)
centroids = intial_centroids(data)
compute_distance(centroids, data)
i = 0
while not converged(prev, data):
    if iterations:
        if i == iterations:
            break
        i += 1
        print i
    centroids = compute_centroids(data)
    prev = deepcopy(data)
    compute_distance(centroids, data)

for i in range(0, CLUSTERS):
    print centroids[i]['cluster'],
    print map(lambda c: c['id'], filter(lambda d: d['cluster'] == i+1, data))
end = time.time()
print "time elapsed", end-start
print "Jaccard Coefficient", jaccard_coefficient(original, data)
for i in range(len(data)):
    data[i]['expressions'] = points[i]

plot(data, centroids=centroids, filename="output/spectral-"+filename+".png")