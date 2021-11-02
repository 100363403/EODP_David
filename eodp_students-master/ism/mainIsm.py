
# MAIN FUNCTION TO CALL THE ISM MODULE

from ism.src.ism import ism

# Directory - this is the common directory for the execution of the E2E, all modules
# auxdir = '/home/luss/EODP/EODP_David/eodp_students-master/auxiliary/'
# indir = '/home/luss/my_shared_folder/EODP_TER_2021/EODP-TS-ISM/input/gradient_alt100_act150/' # small scene
# outdir = '/home/luss/my_shared_folder/EODP_TER_2021/EODP-TS-ISM/test_ism/'

# E2E test directory
auxdir = '/home/luss/EODP/EODP_David/eodp_students-master/auxiliary/'
indir = '/home/luss/my_shared_folder/EODP_TER_2021/EODP-TS-E2E/sgm_out/'
outdir = '/home/luss/my_shared_folder/EODP_TER_2021/EODP-TS-E2E/test_e2e/ism_e2e_out/'


# Initialise the ISM
myIsm = ism(auxdir, indir, outdir)
myIsm.processModule()
