
# MAIN FUNCTION TO CALL THE L1B MODULE

from l1b.src.l1b import l1b

# Directory - this is the common directory for the execution of the E2E, all modules
# auxdir = '/home/luss/EODP/EODP_David/eodp_students-master/auxiliary/'
# indir = '/home/luss/my_shared_folder/EODP_TER_2021/EODP-TS-L1B/input/'
# outdir = '/home/luss/my_shared_folder/EODP_TER_2021/EODP-TS-L1B/test_l1b/'

# E2E test directory
auxdir = '/home/luss/EODP/EODP_David/eodp_students-master/auxiliary/'
indir = '/home/luss/my_shared_folder/EODP_TER_2021/EODP-TS-E2E/ism_out/'
outdir = '/home/luss/my_shared_folder/EODP_TER_2021/EODP-TS-E2E/test_e2e/l1b_e2e_out/'

# Initialise the ISM
myL1b = l1b(auxdir, indir, outdir)
myL1b.processModule()
