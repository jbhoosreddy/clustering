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


def print_list(l, c=None):
    for i in l:
        print i
        if c:
            c -= 1
            if not c:
                break


def pick_random(ll, i):
    return random.choice(filter(lambda l: l['truth'] == i, ll))


def distance(a1, a2):
    a1, a2, l = list(a1['expressions']), list(a2['expressions']), len(a1['expressions'])
    return pow(reduce(lambda x, y: x+y, map(lambda i: pow(a1[i]-a2[i], l), xrange(l))), (1/l))


def join(l1, l2, key, method, l):
    idx1 = set(map(lambda x: x[key], l1))
    idx2 = set(map(lambda x: x[key], l2))
    if method == 'union':
        idx = idx1.union(idx2)
    elif method == 'intersection':
        idx = idx1.intersection(idx2)
    return filter(lambda x: x[key] in idx, l)
