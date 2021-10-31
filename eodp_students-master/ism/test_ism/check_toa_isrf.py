from common.io.writeToa import readToa
import numpy as np

indir_test = '/home/luss/my_shared_folder/EODP_TER_2021/EODP-TS-ISM/test_ism/'
indir_ref = '/home/luss/my_shared_folder/EODP_TER_2021/EODP-TS-ISM/output/'

isrf_toa_VNIR_0_Test = readToa(indir_test, 'ism_toa_isrf_VNIR-0.nc')
isrf_toa_VNIR_0_Ref = readToa(indir_ref, 'ism_toa_isrf_VNIR-0.nc')

isrf_toa_VNIR_1_Test = readToa(indir_test, 'ism_toa_isrf_VNIR-1.nc')
isrf_toa_VNIR_1_Ref = readToa(indir_ref, 'ism_toa_isrf_VNIR-1.nc')

isrf_toa_VNIR_2_Test = readToa(indir_test, 'ism_toa_isrf_VNIR-2.nc')
isrf_toa_VNIR_2_Ref = readToa(indir_ref, 'ism_toa_isrf_VNIR-2.nc')

isrf_toa_VNIR_3_Test = readToa(indir_test, 'ism_toa_isrf_VNIR-3.nc')
isrf_toa_VNIR_3_Ref = readToa(indir_ref, 'ism_toa_isrf_VNIR-3.nc')


Error_VNIR_0 = np.zeros([isrf_toa_VNIR_0_Test.shape[0], isrf_toa_VNIR_0_Test.shape[1]])
Error_VNIR_1 = np.zeros(([isrf_toa_VNIR_1_Test.shape[0], isrf_toa_VNIR_1_Test.shape[1]]))
Error_VNIR_2 = np.zeros(([isrf_toa_VNIR_2_Test.shape[0], isrf_toa_VNIR_2_Test.shape[1]]))
Error_VNIR_3 = np.zeros(([isrf_toa_VNIR_3_Test.shape[0], isrf_toa_VNIR_3_Test.shape[1]]))

Nerror_VNIR_0 = 0
Nerror_VNIR_1 = 0
Nerror_VNIR_2 = 0
Nerror_VNIR_3 = 0



for i in range(isrf_toa_VNIR_0_Test.shape[0]):
    for j in range(isrf_toa_VNIR_0_Test.shape[1]):

        # --------------------------------------------------------------------------------------------------------------
        # Error in VNIR 0 band
        if isrf_toa_VNIR_0_Test[i, j] == 0:
            Error_VNIR_0[i, j] = np.absolute((isrf_toa_VNIR_0_Ref[i, j] -isrf_toa_VNIR_0_Test[i, j]))
        else:
            Error_VNIR_0[i, j] = np.absolute((isrf_toa_VNIR_0_Ref[i, j] -isrf_toa_VNIR_0_Test[i, j])/isrf_toa_VNIR_0_Test[i, j])*100

        if Error_VNIR_0[i, j] > 0.01/100:
            Nerror_VNIR_0 = Nerror_VNIR_0+1

        # --------------------------------------------------------------------------------------------------------------
        # Error in VNIR 1 band
        if isrf_toa_VNIR_1_Test[i, j] == 0:
            Error_VNIR_1[i, j] = np.absolute((isrf_toa_VNIR_1_Ref[i, j] -isrf_toa_VNIR_1_Test[i, j]))
        else:
            Error_VNIR_1[i, j] = np.absolute((isrf_toa_VNIR_1_Ref[i, j] -isrf_toa_VNIR_1_Test[i, j] )/isrf_toa_VNIR_1_Ref[i, j])*100

        if Error_VNIR_1[i, j] > 0.01/100:
            Nerror_VNIR_1 = Nerror_VNIR_1+1

        # --------------------------------------------------------------------------------------------------------------
        # Error in VNIR 2 band

        if isrf_toa_VNIR_2_Test[i, j] == 0:
            Error_VNIR_2[i, j] = np.absolute((isrf_toa_VNIR_2_Ref[i, j] -isrf_toa_VNIR_2_Test[i, j]))
        else:
            Error_VNIR_2[i, j] = np.absolute((isrf_toa_VNIR_2_Ref[i, j] -isrf_toa_VNIR_2_Test[i, j] )/isrf_toa_VNIR_2_Ref[i, j])*100

        if Error_VNIR_2[i, j] > 0.01/100:
            Nerror_VNIR_2 = Nerror_VNIR_2+1

        # --------------------------------------------------------------------------------------------------------------
        # Error in VNIR 3 band
        if isrf_toa_VNIR_3_Ref[i, j] == 0:
            Error_VNIR_3[i, j] = np.absolute((isrf_toa_VNIR_3_Ref[i, j] -isrf_toa_VNIR_3_Test[i, j]))
        else:
            Error_VNIR_3[i, j] = np.absolute((isrf_toa_VNIR_3_Ref[i, j] -isrf_toa_VNIR_3_Test[i, j] )/isrf_toa_VNIR_3_Ref[i, j])*100

        if Error_VNIR_3[i, j] > 0.01/100:
            Nerror_VNIR_3 = Nerror_VNIR_3+1


sizeToa = isrf_toa_VNIR_0_Ref.size

PercError_VNIR_0 = Nerror_VNIR_0/sizeToa*100
PercError_VNIR_1 = Nerror_VNIR_1/sizeToa*100
PercError_VNIR_2 = Nerror_VNIR_2/sizeToa*100
PercError_VNIR_3 = Nerror_VNIR_3/sizeToa*100

print('The percentage of wrong elements comparing the reference and the obtained isrf TOA in VNIR 0 is ', PercError_VNIR_0, '%')
print('The percentage of wrong elements comparing the reference and the obtained isrf TOA in VNIR 1 is ', PercError_VNIR_1, '%')
print('The percentage of wrong elements comparing the reference and the obtained isrf TOA in VNIR 2 is ', PercError_VNIR_2, '%')
print('The percentage of wrong elements comparing the reference and the obtained isrf TOA in VNIR 3 is ', PercError_VNIR_3, '%')

print('')
