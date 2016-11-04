from helper.SparseMatrix import SparseMatrix as Matrix
from helper.utils import print_list, print_dict
from helper.utils import load_data
data = load_data('cho.txt')
matrix = Matrix(data)
i = 0
while matrix.size():
    i += 1
    print i, matrix.size()
    matrix.update()
print_list(matrix.history)