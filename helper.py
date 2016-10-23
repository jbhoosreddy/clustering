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
            'centroid': 0
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

