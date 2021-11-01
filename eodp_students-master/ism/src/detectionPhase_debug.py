
from ism.src.initIsm import initIsm
import numpy as np
from common.io.writeToa import writeToa
from common.plot.plotMat2D import plotMat2D
from common.plot.plotF import plotF

class detectionPhase(initIsm):

    def __init__(self, auxdir, indir, outdir):
        super().__init__(auxdir, indir, outdir)

        # Initialise the random see for the PRNU and DSNU
        np.random.seed(self.ismConfig.seed)


    def compute(self, toa, band):

        self.logger.info("EODP-ALG-ISM-2000: Detection stage")

        # Irradiance to photons conversion
        # -------------------------------------------------------------------------------
        self.logger.info("EODP-ALG-ISM-2010: Irradiances to Photons")
        area_pix = self.ismConfig.pix_size * self.ismConfig.pix_size # [m2]
        toa = self.irrad2Phot(toa, area_pix, self.ismConfig.t_int, self.ismConfig.wv[int(band[-1])])

        self.logger.debug("TOA [0,0] " +str(toa[0,0]) + " [ph]")

        # Photon to electrons conversion
        # -------------------------------------------------------------------------------
        self.logger.info("EODP-ALG-ISM-2030: Photons to Electrons")
        toa = self.phot2Electr(toa, self.ismConfig.QE)

        self.logger.debug("TOA [0,0] " +str(toa[0,0]) + " [e-]")

        if self.ismConfig.save_after_ph2e:
            saveas_str = self.globalConfig.ism_toa_e + band
            writeToa(self.outdir, saveas_str, toa)

        # PRNU
        # -------------------------------------------------------------------------------
        if self.ismConfig.apply_prnu:

            self.logger.info("EODP-ALG-ISM-2020: PRNU")
            toa = self.prnu(toa, self.ismConfig.kprnu)

            self.logger.debug("TOA [0,0] " +str(toa[0,0]) + " [e-]")

            if self.ismConfig.save_after_prnu:
                saveas_str = self.globalConfig.ism_toa_prnu + band
                writeToa(self.outdir, saveas_str, toa)

        # Dark-signal
        # -------------------------------------------------------------------------------
        if self.ismConfig.apply_dark_signal:

            self.logger.info("EODP-ALG-ISM-2020: Dark signal")
            toa = self.darkSignal(toa, self.ismConfig.kdsnu, self.ismConfig.T, self.ismConfig.Tref,
                                  self.ismConfig.ds_A_coeff, self.ismConfig.ds_B_coeff)

            self.logger.debug("TOA [0,0] " +str(toa[0,0]) + " [e-]")

            if self.ismConfig.save_after_ds:
                saveas_str = self.globalConfig.ism_toa_ds + band
                writeToa(self.outdir, saveas_str, toa)

        # Bad/dead pixels
        # -------------------------------------------------------------------------------
        if self.ismConfig.apply_bad_dead:

            self.logger.info("EODP-ALG-ISM-2050: Bad/dead pixels")
            toa = self.badDeadPixels(toa,
                               self.ismConfig.bad_pix,
                               self.ismConfig.dead_pix,
                               self.ismConfig.bad_pix_red,
                               self.ismConfig.dead_pix_red)


        # Write output TOA
        # -------------------------------------------------------------------------------
        if self.ismConfig.save_detection_stage:
            saveas_str = self.globalConfig.ism_toa_detection + band

            writeToa(self.outdir, saveas_str, toa)

            title_str = 'TOA after the detection phase [e-]'
            xlabel_str='ACT'
            ylabel_str='ALT'
            plotMat2D(toa, title_str, xlabel_str, ylabel_str, self.outdir, saveas_str)

            idalt = int(toa.shape[0]/2)
            saveas_str = saveas_str + '_alt' + str(idalt)
            plotF([], toa[idalt,:], title_str, xlabel_str, ylabel_str, self.outdir, saveas_str)

        return toa


    def irrad2Phot(self, toa, area_pix, tint, wv):
        """
        Conversion of the input Irradiances to Photons
        :param toa: input TOA in irradiances [mW/m2]
        :param area_pix: Pixel area [m2]
        :param tint: Integration time [s]
        :param wv: Central wavelength of the band [m]
        :return: Toa in photons
        """
        h = 6.6260608696*1e-34
        c = 2.99792458*1e8

        E_in = toa * area_pix * tint *1e-3
        E_ph = h*c/wv

        toa_ph = E_in/E_ph

        factor = area_pix*tint/E_ph
        self.logger.info('Irrad2Phot factor: ' + str("%1.3e" % factor) + '\n')

        return toa_ph

    def phot2Electr(self, toa, QE):
        """
        Conversion of photons to electrons
        :param toa: input TOA in photons [ph]
        :param QE: Quantum efficiency [e-/ph]
        :return: toa in electrons
        """

        toae = toa*QE
        self.logger.info('Phot2Electr factor: ' + str("%0.3f" % QE) + '\n')
        n_pix = toa.shape[0]*toa.shape[1]

        fwc = self.ismConfig.FWC # Full well Capacity
        n_sat = 0

        for i in range(toa.shape[0]):
            for j in range(toae.shape[1]):
                if toae[i,j] > fwc:
                    toae[i,j] = fwc # Saturation reached
                    n_sat = n_sat + 1

        sat_per = n_sat/n_pix*100

        self.logger.info('Number saturated pixels: ' + str('%i' % n_sat))
        self.logger.info('Percentage saturated pixels: ' + str("%1.3e" % sat_per) + ' % \n')
        return toae

    def badDeadPixels(self, toa,bad_pix,dead_pix,bad_pix_red,dead_pix_red):
        """
        Bad and dead pixels simulation
        :param toa: input toa in [e-]
        :param bad_pix: Percentage of bad pixels in the CCD [%]
        :param dead_pix: Percentage of dead pixels in the CCD [%]
        :param bad_pix_red: Reduction in the quantum efficiency for the bad pixels [-, over 1]
        :param dead_pix_red: Reduction in the quantum efficiency for the dead pixels [-, over 1]
        :return: toa in e- including bad & dead pixels
        """

        toa_act = toa.shape[1]

        n_pix_bad  = int(bad_pix*toa_act/100)
        n_pix_dead = int(dead_pix*toa_act/100)

        if n_pix_bad != 0:
            step_bad  = int(toa_act/n_pix_bad)
            idx_bad  = range(5, toa_act, step_bad)
            toa[:, idx_bad]  = toa[:, idx_bad] * (1 - bad_pix_red)

        if  n_pix_dead != 0:
            step_dead = int(toa_act/n_pix_dead)
            idx_dead = range(0, toa_act, step_dead)
            toa[:, idx_dead] = toa[:, idx_dead] * (1 - dead_pix_red)

        return toa

    def prnu(self, toa, kprnu):
        """
        Adding the PRNU effect
        :param toa: TOA pre-PRNU [e-]
        :param kprnu: multiplicative factor to the standard normal deviation for the PRNU
        :return: TOA after adding PRNU [e-]
        """
        for i in range(toa.shape[1]):
            prnu = np.random.normal(0, 1.0)*kprnu
            toa[:,i] = toa[:,i]*(1 + prnu)

        return toa


    def darkSignal(self, toa, kdsnu, T, Tref, ds_A_coeff, ds_B_coeff):
        """
        Dark signal simulation
        :param toa: TOA in [e-]
        :param kdsnu: multiplicative factor to the standard normal deviation for the DSNU
        :param T: Temperature of the system
        :param Tref: Reference temperature of the system
        :param ds_A_coeff: Empirical parameter of the model 7.87 e-
        :param ds_B_coeff: Empirical parameter of the model 6040 K
        :return: TOA in [e-] with dark signal
        """
        Sd = ds_A_coeff * (T / Tref)**3 * np.exp(-ds_B_coeff * (1/T - 1/Tref))

        toa_dsnu = np.zeros(toa.shape)
        for i in range(toa.shape[1]):
            dsnu = np.abs(np.random.normal(0,1))*kdsnu
            ds = Sd * (1+dsnu)

            toa_dsnu[:,i] = toa[:,i] + ds

        return toa_dsnu


        # Sd = ds_A_coeff * (T / Tref)**3 * np.exp(-ds_B_coeff * (1/T - 1/Tref))
        #
        # for i in range(toa.shape[1]):
        #     dsnu = np.abs(np.random.normal(0,1))*kdsnu
        #     ds = Sd*(1+dsnu)
        #     toa[:,i] = toa[:,i] + ds
        #
        # return toa