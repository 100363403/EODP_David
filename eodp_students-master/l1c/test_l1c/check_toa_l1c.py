import numpy as np
from common.io.writeToa import writeToa, readToa
from config import globalConfig
import matplotlib.pyplot as plt


gC = globalConfig.globalConfig()

test_dir = '/home/luss/my_shared_folder/EODP_TER_2021/EODP-TS-L1C/test_l1c/'    # test data
luss_dir = '/home/luss/my_shared_folder/EODP_TER_2021/EODP-TS-L1C/output/'      # reference output data

print('Check error in L1C phase:  \n')

for band in gC.bands:
    toa_test = readToa(test_dir, gC.l1c_toa + band + '.nc')
    toa_ref = readToa(luss_dir, gC.l1c_toa + band + '.nc')

    for i in range(toa_test.shape[0]):

        # convert negative values to 0
        if toa_test[i] < 0:
            toa_test[i] = 0

        if toa_ref[i] < 0:
            toa_ref[i] = 0

    # sort/order elements of vectors
    toa_test_sort = np.sort(toa_test)
    toa_ref_sort = np.sort(toa_ref)

    n_error = 0
    error = np.zeros([toa_test_sort.shape[0]])
    for i in range(error.shape[0]):

        if toa_ref_sort[i] == 0:
            error[i] = np.absolute(toa_ref_sort[i] - toa_test_sort[i])
        else:
            error[i] = np.absolute((toa_ref_sort[i] - toa_test_sort[i]) / toa_ref_sort[i])

        if error[i] > 0.01/100:
            n_error = n_error + 1

    n_points = toa_test_sort.size
    per_points_out = n_error/n_points * 100

    print('\n  For band ' + band + ', percentage of points with error higher than 0.01% is:  ', per_points_out, '%  \n')
