from __future__ import division
import random
random.seed(0)


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
            'cluster': 0,
            'visited': False
        })
    return filter(lambda x: x['truth'] != -1, output)


def print_list(l, c=None, should_print=True):
    output = ""
    for i in l:
        if should_print:
            print i
        output += str(i)+"\n"
        if c:
            c -= 1
            if not c:
                break
    return output


def print_dict(d, c=None, should_print=True):
    output = ""
    for k,v in d.items():
        if should_print:
            print k,v
        output += str(k)+": "+str(v)+"\n"
        if c:
            c -= 1
            if not c:
                break
    return output


def pick_random(ll, i):
    return random.choice(filter(lambda l: l['truth'] == i, ll))

def pick(ll, i):
    return filter(lambda l: l['id'] == i, ll)[0]

def distance(a1, a2):
    a1, a2, l = list(a1['expressions']), list(a2['expressions']), len(a1['expressions'])
    p = 2
    return pow(reduce(lambda x, y: x+y, map(lambda i: pow(abs(a1[i]-a2[i]), p), xrange(l))), (1/p))


def join(l1, l2, key, method, l):
    idx1 = set(map(lambda x: x[key], l1))
    idx2 = set(map(lambda x: x[key], l2))
    if method == 'union':
        idx = idx1.union(idx2)
    elif method == 'intersection':
        idx = idx1.intersection(idx2)
    return filter(lambda x: x[key] in idx, l)
