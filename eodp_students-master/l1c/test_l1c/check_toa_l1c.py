import numpy as np
from common.io.writeToa import writeToa, readToa
from config import globalConfig
import matplotlib.pyplot as plt


gC = globalConfig.globalConfig()

indir_test = '/home/luss/my_shared_folder/EODP_TER_2021/EODP-TS-L1C/test_l1c/'    # test data
indir_ref = '/home/luss/my_shared_folder/EODP_TER_2021/EODP-TS-L1C/output/'      # reference output data

print('Check error in L1C phase:  \n')

for band in gC.bands:
    toa_test = readToa(indir_test, gC.l1c_toa + band + '.nc')
    toa_ref = readToa(indir_ref, gC.l1c_toa + band + '.nc')

    for i in range(toa_test.shape[0]):

            if toa_test[i] < 0:
                toa_test[i] = 0

            if toa_ref[i] < 0:
                toa_ref[i] = 0

    toa_testSort = np.sort(toa_test)
    toa_refSort = np.sort(toa_ref)

    Error = np.zeros([toa_testSort.shape[0]])

    n_error = 0

    for i in range(Error.shape[0]):

        if toa_refSort[i] == 0:
            Error[i] = np.absolute(toa_refSort[i] - toa_testSort[i])
        else:
            Error[i] = np.absolute((toa_refSort[i] - toa_testSort[i])/toa_refSort[i])

        if Error[i] > 0.01/100:
            n_error = n_error + 1

    n_points = toa_testSort.size

    per_points_out = n_error / n_points * 100

    print('\n  For band ' + band + ', percentage of points with error higher than 0.01% is:  ', per_points_out, '%  \n')
