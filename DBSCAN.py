from __future__ import division
from helper.utils import load_data, print_list, join


INPUT_FILE = 'data/cho.txt'
EPS = 2
MIN_POINTS = 100


def region_query(P, eps, remaining):
    return filter(lambda p: distance(p['expressions'], P['expressions']) <= eps, remaining)


def distance(a1, a2):
    l = len(a1)
    return pow(reduce(lambda x, y: x+y, map(lambda i: pow(a1[i]-a2[i], l), xrange(l))), (1/l))


def expand_cluster(P, neighbors, C, eps, min_points, remaining, D):
    P['cluster'] = C
    while True:
        remaining_points = get_remaining(neighbors)
        if not len(remaining_points):
            break
        for P_prime in remaining_points:
            if not P_prime['visited']:
                P_prime['visited'] = True
                remaining = get_remaining(remaining)
                neighbors_prime = region_query(P_prime, eps, D)
                if len(neighbors_prime) >= min_points:
                    neighbors = join(neighbors, neighbors_prime, 'id', 'union', D)
            if not P_prime['cluster']:
                P_prime['cluster'] = C


def get_remaining(data):
    return filter(lambda p: not p['visited'], data)


def DBSCAN(D, eps, min_points):
    C = 0
    while True:
        remaining = get_remaining(D)
        if not len(remaining):
            break
        print "main", len(remaining)
        for P in remaining:
            P['visited'] = True
            neighbors = region_query(P, eps, D)
            if len(neighbors) < min_points:
                if not P['cluster']:
                    P['cluster'] = -1
            else:
                C += 1
                expand_cluster(P, neighbors, C, eps, min_points, remaining, D)


if __name__ == "__main__":
    D = load_data(INPUT_FILE)
    # print_list(D)
    DBSCAN(D, EPS, MIN_POINTS)
    print_list(D)

