from helper.SparseMatrix import SparseMatrix as Matrix
from helper.utils import print_list, print_dict
from helper.utils import load_data
filename = 'new_dataset_2'
data = load_data('data/' + filename + '.txt')
matrix = Matrix(data)
i = 0
while matrix.size():
    i += 1
    print i, matrix.size()
    matrix.update()
matrix.save("agglomerative-" + filename)
print_list(matrix.history)
