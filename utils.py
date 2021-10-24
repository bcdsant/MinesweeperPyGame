import os


def find(name, path, ext='.txt'):
    for root, dirs, files in os.walk(path):
        if name+ext in files:
            return os.path.join(root, name+ext)


def array_to_matrix(array, num_rows):
    if (len(array) % num_rows == 0):
        matrix = []
        slice_size = len(array)//num_rows
        for row in range(num_rows):
            matrix.append(array[slice_size*row:slice_size*(1+row)])
        return matrix
    else:
        error = ValueError(
            "Can't break array in {} rows with the same size".format(num_rows))
        raise error
