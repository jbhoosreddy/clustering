from __future__ import division
import itertools


def jaccard_coefficient(original, final):
    ids = map(lambda o: o['id'], original)
    combinations = itertools.combinations(ids, 2)
    intersection = union = 0
    for i, j in combinations:
        original_value = final_value = 0
        filtered_original = filter(lambda d: d['id'] in (i, j), original)
        if filtered_original[0]['truth'] == filtered_original[1]['truth']:
            original_value = 1
        filtered_final = filter(lambda d: d['id'] in (i, j), final)
        if filtered_final[0]['cluster'] == filtered_final[1]['cluster']:
            final_value = 1
        if original_value == final_value == 1:
            intersection += 1
            union += 1
        elif original_value == 1 or final_value == 1:
            union += 1
    return intersection/union

    initial = create_matrix(original, 'truth')
    last = create_matrix(final, 'cluster')
    return compute(initial, last, original)


