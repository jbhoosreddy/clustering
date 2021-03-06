from helper.SparseMatrix import SparseMatrix as Matrix
from helper.utils import print_list, print_dict
from helper.utils import load_data
from copy import deepcopy
from helper.validation import jaccard_coefficient
import pickle
from helper.graph import plot
import time

filename = 'cho'
THRESHOLD = 5
start = time.time()
data = load_data('data/' + filename + '.txt')
original = deepcopy(data)
CACHE = False
if CACHE:
    handle = open('output/agglomerative-' + filename + ".pickle", 'r')
    matrix = pickle.load(handle)
    handle.close()
else:
    matrix = Matrix(data)
i = 0
while matrix.size()-1:
    i += 1
    # print i, matrix.size()
    matrix.update() if not CACHE else None
end = time.time()
print "time elapsed", end-start
matrix.save("agglomerative-" + filename)
clusters = list(matrix.history[THRESHOLD])
print_list(clusters)
truths = map(lambda cluster: map(lambda point: filter(lambda d: d['id'] == point, data)[0]['truth'], cluster), clusters)

ids = map(lambda d: d['id'], data)
for i in range(THRESHOLD):
    truth = map(lambda t: t.count(i+1), truths)
    # print truth
    idx = max(xrange(len(truth)), key=truth.__getitem__)
    for p in clusters[idx]:
        idx = ids.index(p)
        data[idx]['cluster'] = i+1

print "Jaccard Coefficient", jaccard_coefficient(original, data)

i = 1
for cluster in clusters:
    for p in cluster:
        dp = filter(lambda d: d['id'] == p, data)[0]
        dp['cluster'] = i
    i += 1

plot(data, n=THRESHOLD, filename="output/agglomerative-"+filename+".png")
