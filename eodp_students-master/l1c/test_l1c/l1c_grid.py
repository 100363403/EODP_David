from common.io.l1cProduct import readL1c
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from config import globalConfig


# Plot Projection of TOA on ground (Lucia's code)

outdir = '/home/luss/my_shared_folder/EODP_TER_2021/EODP-TS-L1C/test_l1c/'
gC = globalConfig.globalConfig()

for band in gC.bands:

    [toa_l1c, lat_l1c, lon_l1c] = readL1c(outdir, 'l1c_toa_'+ band + '.nc')

    jet = cm.get_cmap('jet', len(lat_l1c))

    toa_l1c[np.argwhere(toa_l1c<0)] = 0

    max_toa = np.max(toa_l1c)

    # Plot stuff

    fig = plt.figure(figsize=(20,10))

    for ii in range(100):  # range(len(lat_l1c)):

        clr = jet(toa_l1c[ii]/max_toa)

        plt.plot(lon_l1c, lat_l1c, '.',color='r', markersize=5)

    plt.title('Projection on ground', fontsize=20)

    plt.xlabel('Longitude [deg]', fontsize=16)

    plt.ylabel('Latitude [deg]', fontsize=16)

    plt.grid()

    plt.axis('equal')

    plt.savefig(outdir + 'l1c_toa_projection_' + band + '.png')

    plt.close(fig)


# Plot values of TOA on ground

for band in gC.bands:

    [toa, lat, lon] = readL1c(outdir, 'l1c_toa_'+ band + '.nc')
    jet = cm.get_cmap('jet', toa.shape[0])

    # convert negative values to 0
    toa[np.argwhere(toa<0)] = 0
    max_toa = np.max(toa)

    plt.figure()
    plt.scatter(lon, lat, c=toa, s=2)
    plt.jet()
    plt.colorbar()

    plt.title('TOA ' + band)
    plt.xlabel("Longitude [deg]")
    plt.ylabel("Latitude [deg]")
    plt.grid()
    plt.axis('equal')
    plt.savefig(outdir + "l1c_toa_map_" + band + '.png')

    plt.close()


