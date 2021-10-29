
"""
Check for all bands that the differences with respect to the output TOA (l1b_toa_)
are <0.01% for at least 3-sigma of the points.
"""
import numpy

from common.io import writeToa
from config import globalConfig

test_dir = '/home/luss/my_shared_folder/EODP_TER_2021/EODP-TS-L1B/test_l1b'
luss_dir = '/home/luss/my_shared_folder/EODP_TER_2021/EODP-TS-L1B/output/'

gC = globalConfig.globalConfig()


# Equalizer
for ii in range(4):

    test_toa = writeToa.readToa(test_dir, 'l1b_toa_eq_VNIR-' + str(ii) + '.nc')

    luss_toa = writeToa.readToa(luss_dir, 'l1b_toa_eq_VNIR-' + str(ii) + '.nc')

    difference = numpy.max(numpy.absolute((test_toa - luss_toa)/luss_toa))

    print('\nEqualizer error for VNIR-' + str(ii) + ' is:  ' + str(difference) + ' %  \n')


# Restoration
for ii in range(4):

    test_toa = writeToa.readToa(test_dir, 'l1b_toa_VNIR-' + str(ii) + '.nc')

    luss_toa = writeToa.readToa(luss_dir, 'l1b_toa_VNIR-' + str(ii) + '.nc')

    difference = numpy.max(numpy.absolute((test_toa - luss_toa)/luss_toa))

    print('\nRestoration error for VNIR-' + str(ii) + ' is:  ' + str(difference) + ' %  \n')

