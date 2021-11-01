import numpy as np
from common.io.writeToa import writeToa, readToa
from config import globalConfig
import matplotlib.pyplot as plt


gC = globalConfig.globalConfig()

dir_l1b = "/home/luss/my_shared_folder/EODP_TER_2021/EODP-TS-L1B/test_l1b/"
dir_ism = "/home/luss/my_shared_folder/EODP_TER_2021/EODP-TS-ISM/test_ism/"

for band in gC.bands:
    toa_l1b_eq = readToa(dir_l1b, gC.l1b_toa + band + '.nc')
    toa_ism = readToa(dir_ism, gC.ism_toa_isrf + band + '.nc')
    toa_l1b_no_eq = readToa(dir_l1b, gC.l1b_toa + band + '_noEq.nc')

    index_alt = int(toa_l1b_no_eq.shape[0]/2)         # central ALT position
    pixel_vec = range(len(toa_l1b_no_eq[index_alt,:]))

    plt.figure(figsize=(12,6))

    plt.plot(pixel_vec, toa_ism[index_alt,:],label='TOA after ISRF',c='b')
    plt.plot(pixel_vec, toa_l1b_no_eq[index_alt,:],label='TOA l1b without eq',c='k')
    plt.plot(pixel_vec, toa_l1b_eq[index_alt,:],label='TOA l1b with eq',c='r')

    plt.title('Restored Signal Comparison '+ band)
    plt.xlabel('ACT [Pixels]')
    plt.ylabel('TOA [mW/sr/m2]')
    plt.grid()
    plt.legend()

    fig_name = dir_l1b + 'Comparison_TOA_' + band + '.png'
    plt.savefig(fig_name)

    plt.close()
