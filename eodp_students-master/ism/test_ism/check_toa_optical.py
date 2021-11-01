import numpy as np
from common.io.writeToa import writeToa, readToa
from config import globalConfig
import matplotlib.pyplot as plt


gC = globalConfig.globalConfig()

test_dir = "/home/luss/my_shared_folder/EODP_TER_2021/EODP-TS-ISM/test_ism/"    # test data
luss_dir = "/home/luss/my_shared_folder/EODP_TER_2021/EODP-TS-ISM/output/"      # reference output data

print('Check error in Optical Phase:\n')

for band in gC.bands:
    toa_test = readToa(test_dir, gC.ism_toa_optical + band + '.nc')
    toa_luss = readToa(luss_dir, gC.ism_toa_optical + band + '.nc')

    n_points = toa_luss.shape[0] * toa_luss.shape[1]

    relative_err = np.absolute((toa_test - toa_luss)/toa_luss)
    mean_err = np.mean(relative_err)
    standard_err = np.std(relative_err)

    points_out = np.sum(np.absolute(relative_err - mean_err) > (3 * standard_err))   # number of points outside of the 3 sigma
    points_out_per = points_out/n_points * 100      # percentage of points outside of the 3 sigma

    print("\n  For band " + band + ": " + str("%0.3f" % points_out_per) + '% of points are outside 3 sigma \n')


"""
gC = globalConfig.globalConfig()

dir_test = "/home/luss/my_shared_folder/EODP_TER_2021/EODP-TS-ISM/test_ism/"    # test data
dir_luss = "/home/luss/my_shared_folder/EODP_TER_2021/EODP-TS-ISM/output/"      # reference data

print('Check error in Optical Phase:\n')

for band in gC.bands:
    toa_test = readToa(dir_test, gC.ism_toa_optical + band + '.nc')
    toa_luss = readToa(dir_luss, gC.ism_toa_optical + band + '.nc')

    n_points = toa_luss.shape[0] * toa_luss.shape[1]

    relative_err = np.absolute((toa_test - toa_luss)/toa_luss)
    mean_err = np.mean(relative_err)
    standard_err = np.std(relative_err)

    points_out = np.sum(np.absolute(relative_err - mean_err) > (3 * standard_err))   # number of points outside of the 3 sigma
    points_out_per = points_out/n_points * 100      # percentage of points outside of the 3 sigma
    print("For band " + band + ": " + str("%0.3f" % points_out_per) + '% of points are outside 3 sigma')
"""
