# -*- coding: utf-8 -*-
import numpy as np
import utils
from scipy.signal import lfilter
## constants
p_ref = 20e-6  # Reference pressure in Pascals
"""

"""
# % UAM descriptive at recorded possition.
#########################################

class UAM_descriptive:
    """
    Main characterized UAM from recorded operation.
    This class is the blue print for basic noise characterization of a
    Drone Noise signal recorded at listener possition.
    """
    def __init__(self, operation, data_rec, weight_curve, t_value ):
        """

        Parameters
        ----------
        data_rec : array of signals from the mat file
            array of time series
        weight_curve : String "A" or "Z"
            if isophone courves are needed

        Returns
        -------
        None.

        """

        self.data_rec = data_rec
        self.weight_curve = weight_curve
        self.operation = operation
        
        self.fs = int(self.data_rec['Sample_rate'][0][0])
        
        self.num_channels, self.DATA_raw, self.DATA_acu, self.time_vec  = self.raw_and_spl()
        self.Filt_DATA_raw = self.p_t_W_() # weigthed time-series
        self.SPL, self.time_metrics, self.Leq, self.Lmax, self.LE, self.L10, self.L50, self.L90 = self.metrics(t_int=t_value)

    ####### Instance method for separate data_recs from multichannel pressure and SPL  
    ##################################################################################
  
    def raw_and_spl(self, num_channels=9, recorded_metric ='LAFp'):

        """
        This function extrac raw data and pre-calculated SPL from exported .mat files from Dewesoft.
        Parameters
        ----------
        num_channels = 9 # Number of channels of the recordings
                       ALL  subsequent claculations are doing on all the selected channels.

        Returns
        -------
        DATA_raw : list
            multichannel data of acoustic pressure time-series
        DATA_spl : list
            multichannel data of acoustic pressure level time-series
        fs : integer
            Sample rate
        time_vect: array
            time stamp
        """

        # fs = int(self.data_rec['Sample_rate'][0][0])
        ##### LIST of DATA dictionary
        DATA_raw = []
        DATA_acu = []
        
        for m in range(num_channels):
            kr = 'Data1_Mic_'+str(m+1)                      # acces to dictionary key row
            ka = 'Data1_Mic_'+str(m+1)+'_'+ recorded_metric # acces to dictionary key acu
            
            m_raw_data = np.squeeze(self.data_rec[kr])  # acces to data ad squeeze
            m_acu_data = np.squeeze(self.data_rec[ka])  # acces to data ad squeeze
            
            DATA_raw.append(m_raw_data)       # concat data in collumns
            DATA_acu.append(m_acu_data)
            
        print(f'{m+1} channels')
        DATA_raw = np.array(DATA_raw).T # concat data in collumns
        DATA_acu = np.array(DATA_acu).T # concat data in collumns
        
        DATA_acu -6 # = DATA_acu - 6  #correction because of the reflective plate - 6
        DATA_raw /2 # = DATA_raw  /2  #correction because of the reflective plate // 2
        
        time_vec = (np.linspace(0, DATA_raw.shape[0], DATA_raw.shape[0]))/self.fs #time vector
        
        return num_channels, DATA_raw, DATA_acu, time_vec

    ######## Instance method for apppliying A courve if it is required.
    ###################################################################

    def p_t_W_(self):
        ###### A-weigthing application if requiered
        if self.weight_curve =="A":
            b, a = utils.A_weighting_coeffs_design(self.fs)  # generation of the coeficients
            Filt_DATA_raw = lfilter(b, a, self.DATA_raw, axis=0)  #A-weigth filtering, per column (channel)
            print('Aw applied')
            
        elif self.weight_curve =="Z":
            Filt_DATA_raw = self.DATA_raw
            print('Zw applied')
            
        return Filt_DATA_raw
    
    
    ######## Instance method for calculating metrics from acoustic pressure time-series
    ####################################################################################

    def metrics(self, t_int):

        """
        Parameters
        ----------
        t_int : float
            Window size for Metrics calculations. The default is 0.125 [s] for Fast time averaging.
        weight_curve : string
            If frequency filter is needeed. The default is "A".

        Returns
        -------
        Filt_DATA_raw : Filtered raw data, based on A or Z courves
        SPL : Vector of SPL on each window. valueas are weigthed by weigth_curve type
        L50, L10, L90: statistical values of percentage of excedance.

        """
        ###### Calculate Shot-therm SPL 
        ###############################
        
        window_size = int(t_int * self.fs)  # Window size for 0.5-second intervals
        SPL = []
        time_metrics = []
        for start in  range(0, len( self.Filt_DATA_raw), window_size):
            chunk_data = self.Filt_DATA_raw[start:start + window_size] 
            # chunk_data = 
            if len(chunk_data) == 0:
                break
            ch_data_time_sqr = chunk_data**2
            ch_data_time_sqr = utils.time_weighting(ch_data_time_sqr, self.fs, t_int) #Fast, slow or other
            p_rms = np.sqrt(np.mean(ch_data_time_sqr, axis=0))  # RMS of the signal pressure in the window
            SPL_chunk = 20 * np.log10(p_rms/ p_ref)  # SPL in decibels
            SPL.append(SPL_chunk)
            
            time_metrics.append(start / self.fs)  # Time in seconds for each window
        SPL = np.squeeze(SPL) ## Generate an array from the list SPL
        
        ###### Calculate Equivalent Level Leq
        #####################################
        p_rms_leq = np.sqrt(np.mean(self.Filt_DATA_raw**2, axis=0)) # RMS of all the signal
        Leq = 20 * np.log10(p_rms_leq/ p_ref)
        
        ###### Calculate Maximum Level Lmax
        ###################################
        Lmax = np.max(SPL,axis=0)
        
        ###### Calculate Exposure Level LE   # if Flyover LAE_10dB  as Leq_10 + 10log(T/1) 
        ##################################################################################
        LE = []   
        if self.operation[0]=="F":
            for m in range(self.num_channels):
                mask_Lmax_down_10 = SPL[:,m]>( Lmax[m] - 10 ) # Levels Lmax-10dB
                levels = SPL[mask_Lmax_down_10, m]
                p_levels = 10**(levels/10)
                Leq_10 = 10*np.log10( np.mean(p_levels) )
                t_exp = levels.shape[0]*t_int #exposition time to Lmax-10dB
                LE. append(Leq_10 + 10*np.log10(t_exp/1)) # corrected to one-second
            LE = np.squeeze(LE) ## Generate an array from the list LE   
            
          # if Hovering, then LAE is calculated as Leq + 10log(T/1) 
        elif self.operation[0]=="H":
            LE = Leq + 10*np.log10((self.Filt_DATA_raw.shape[0]/self.fs)/1) #correcteedto one second
            
        ###### Calculate Percentiles from SPL 
        ##################################################################################
        N_per= [10,50,99]
        L_nn = []
        for n_p in N_per:
            L_nn.append(utils.percentiles(SPL,n_p))
        L10 = L_nn[0]
        L50 = L_nn[1]
        L90 = L_nn[2]
        
        return  SPL, time_metrics, Leq, Lmax, LE, L10, L50, L90

    ##### Instance method for pploting spectrogrma of specific channel time-series.   
    ################################################################################
 
    def psd_plots (self, channel, scaling, on_new_plot, f_min, f_max, db_min, db_max):
        signal = self.Filt_DATA_raw[:,channel]
        utils.psd_welch(signal, self.fs, scaling, on_new_plot, f_min, f_max, db_min, db_max)
        return
    
    ##### Instance method for pploting spectrogrma of specific channel time-series.   
    ################################################################################
    def spectgram_plots (self, channel, scaling, f_min, f_max, db_min, db_max):
        signal = self.Filt_DATA_raw[:,channel]
        utils.spectrogram(signal, self.fs, scaling, f_min, f_max, db_min, db_max)
        return
    
    ##### Instance method for 1/n octave band representation of specific channel time-series.   
    ################################################################################
    def oct_band_plots (self, channel, limits):
        """
        Based on Jose M. Requena Plens, 2020. 
        https://github.com/jmrplens/PyOctaveBand/tree/master
        """
        signal = self.Filt_DATA_raw[:,channel]
        utils.n_octave_freq_bands(signal, self.fs, n_frac = 3, limits= limits)
        return
    
# % UAM Source Definition by Backpropagation
#####################
class UAM_definition(UAM_descriptive):
    def __init__ (self, rad_deprop):
        self.rad_deprop = rad_deprop 
        self.radio_dec = self.show_radio ()
    
    def show_radio(self):
        radio_dec = self.rad_deprop/100
        
        return radio_dec