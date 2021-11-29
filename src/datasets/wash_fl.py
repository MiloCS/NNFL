import subprocess
import numpy as np


def convert_plus_or_minus(to_convert):
    if to_convert == '+':
        return 0 # this may seem counter intuitive, but failing tests indicate a fault
    elif to_convert == '-':
        return 1
    else:
        assert False


def data_formatted(pid, bid):
    TMP_DIR = 'tmp/'
    gzoltar_tar_gz_file = 'data/fault-localization.cs.washington.edu/data/' + pid + '/' + bid + '/gzoltar-files.tar.gz'
    command = ['tar', '-xzf', gzoltar_tar_gz_file, '-C', TMP_DIR]
    subprocess.Popen(command).wait()

    matrix_file = TMP_DIR + 'gzoltars/' + pid + '/' + bid + '/matrix'
    with open(matrix_file) as f:
        lines = f.readlines()
        N = len(lines)
        D = len(lines[0].split(' ')) - 1   # test result label for - 1
        X = np.zeros((N, D), dtype=np.single)
        tests_passed = []
        for i, line in enumerate(lines):

            curr_list = line.split(' ')
            X[i, :] = curr_list[:-1]
            tests_passed.append(convert_plus_or_minus(curr_list[-1][0]))
        Y = np.array(tests_passed, dtype=np.single, ndmin=2).T

    spectra_file = TMP_DIR + 'gzoltars/' + pid + '/' + bid + '/spectra'
    d_lab = []
    with open(spectra_file) as f:
        for line in f.readlines():
            d_lab.append(line[:-1])

    tests_file = TMP_DIR + 'gzoltars/' + pid + '/' + bid + '/tests'
    n_lab = []
    try:
        with open(tests_file) as f:
            for line in f.readlines():
                line_id, res, _ = tuple(line.split(','))
                n_lab.append(line_id)
    except FileNotFoundError:
        print('File not found, n_lab empty list')

    return X, Y, n_lab, d_lab


