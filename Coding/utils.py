# -*- coding: utf-8 -*-
import numpy as np
from scipy.signal.filter_design import bilinear, zpk2tf
from scipy.signal import lfilter
import scipy.signal as ss
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import PyOctaveBand 
import soundfile as sf
import resampy

"""
Created on Tue Jan 28 16:52:22 2025

@author: ses271

Some General Filters used across the DSP tasks for Drone Noise characterization.
"""

def A_weighting_coeffs_design(sample_rate):
    """Returns b and a coeff of a A-weighting filter.
    https://siggigue.github.io/pyfilterbank/splweighting.html (mofified from:)
    Parameters
    ----------
    sample_rate : scalar
        Sample rate of the signals that well be filtered.

    Returns
    -------
    b, a : ndarray
        Filter coefficients for a digital weighting filter.

    Examples
    --------
    >>> b, a = a_weighting_coeff_design(sample_rate)

    To Filter a signal use scipy lfilter:

    >>> from scipy.signal import lfilter
    >>> y = lfilter(b, a, x)

    See Also
    --------
    b_weighting_coeffs_design : B-Weighting coefficients.
    c_weighting_coeffs_design : C-Weighting coefficients.
    weight_signal : Apply a weighting filter to a signal.
    scipy.lfilter : Filtering signal with `b` and `a` coefficients.
    """
    pi = np.pi
    f1 = 20.598997
    f2 = 107.65265
    f3 = 737.86223
    f4 = 12194.217
    A1000 = 1.9997
    numerators = [(2*pi*f4)**2 * (10**(A1000 / 20.0)), 0., 0., 0., 0.];
    denominators = np.convolve(
        [1., +4*pi * f4, (2*pi * f4)**2],
        [1., +4*pi * f1, (2*pi * f1)**2]
    )
    denominators = np.convolve(
        np.convolve(denominators, [1., 2*pi * f3]),
        [1., 2*pi * f2]
    )
    return bilinear(numerators, denominators, sample_rate)

def time_weighting(data, sample_rate, t_int):
    """Integrate the sound pressure squared using exponential integration.

    :param data: Energetic quantity, e.g. :math:`p^2`.
    :param sample_rate: Sample rate.
    :param integration_time: Integration time.
    :returns:

    Time weighting is applied by applying a low-pass filter with one real pole at :math:`-1/\\tau`.

    .. note::

        Because :math:`f_s \\cdot t_i` is generally not an integer, samples are discarded.
        This results in a drift of samples for longer signals (e.g. 60 minutes at 44.1 kHz).
        from: https://github.com/python-acoustics/python-acoustics/blob/master/acoustics/standards/iec_61672_1_2013.py
        NOTE: When apply time integration, differences of 3dB could appear when compared with Dewesoft calculations.
    """
    b, a = zpk2tf([1.0], [1.0, t_int], [1.0])    
    b, a = bilinear(b, a, sample_rate)
    n = np.floor(t_int * sample_rate).astype(int)
    data= data[..., 0:n * (data.shape[0] // n)]
    return lfilter(b, a, data, axis=0)/t_int # Perform the integration. Select the final value of the integration.

###############################################
###############################################
def psd_welch( signal, sample_rate, scaling, on_new_plot,f_min, f_max, db_min, db_max):
    """
    This funtion calculates and plots the Power spectral density acordingly with Welch method
    Parameters
    ----------
    signal : array
        time-series single channel in pascals
    sample_rate : scalar
        Sample rate of the signals
    scaling : string
        Selects between computing the power spectral density (‘density’) where Pxx 
       has units of V**2/Hz and computing the squared magnitude spectrum (‘spectrum’) 
       where Pxx has units of V**2, if x is measured in V and fs is measured in Hz. from SciPy.
    on_new_plot : Boolean
        If draw in a new plot
    f_min, fmax : int
        Frequecny range in the plot
    db_min, db_max : int
        AMplitude range in the plot

    Returns
    -------
    freq_welch : array
        frequecny bin array of the PSD
    psd_data : array
        PSD amplitude in dB or dB/Hz acordingly to scaling

    """

    if scaling == "density":
        amp_lab = "[dBA/Hz]"
    elif scaling == "spectrum":
        amp_lab = "[dBA]"
        
    Ndft    = 2**16
    p_ref   = 20e-6
    WINDOW = 'hann'
    
    freq_welch, psd_data = ss.welch(signal, sample_rate, window = WINDOW, 
                                    nperseg = Ndft, noverlap=Ndft // 8, scaling=scaling) # noverlap=Noverlap,
    # freq_welch,psd_data =ss.welch(signal, sample_rate, window = WINDOW,
    #                           nperseg = Ndft//6, noverlap = Ndft // 8, scaling = scaling, nfft=2**18)
    if on_new_plot==True:
       plt.figure(figsize=(4, 2))
       print('new figure')
    
    plt.semilogx(freq_welch, 10*np.log10(psd_data/p_ref**2), 'b')
    plt.title('PSD')
    plt.xlabel("Frequency [Hz]")
    plt.ylabel(f'Amplitude {amp_lab}')#' ref.'+f'{p_ref}'+r'$(\mu$[Pa])')
    plt.xlim(f_min, f_max)
    plt.ylim(db_min, db_max)
    plt.tight_layout()
    
    return  freq_welch, psd_data

###############################################
###############################################
def spectrogram (signal, sample_rate, scaling, f_min, f_max, db_min, db_max):
    """
    This function calculates and plots the Spectrogram

    Parameters
    ----------
    signal : array
        time-series single channel in pascals
    sample_rate : scalar
        Sample rate of the signals
    scaling : string
        Selects between computing the power spectral density (‘density’) where Pxx 
       has units of V**2/Hz and computing the squared magnitude spectrum (‘spectrum’) 
       where Pxx has units of V**2, if x is measured in V and fs is measured in Hz. from SciPy.
    f_min, fmax : int
        Frequecny range in the plot
    db_min, db_max : int
        AMplitude range in the plot

    Returns
    -------
    freq_ : array
        frequecny bin array of the spectrums
    t_ : array
        time array where each spectrum was calculated
    Sxx : array
        Amplitude of the acoustic power, not yet in dB scale

    """
    
    Ndft = 2**16
    WINDOW = 'hann'
    p_ref   = 20e-6
    
    if scaling == "density":
        amp_lab = "[dBA/Hz]"
    elif scaling == "spectrum":
        amp_lab = "[dBA]"
    
    freq_, t_, Sxx = ss.spectrogram (signal, sample_rate, window = WINDOW,
                              nperseg = Ndft//6, noverlap = Ndft // 8, scaling = scaling, nfft=2**18)
    
    plt.figure(figsize=(4, 2))
    
    plt.pcolormesh(t_, freq_, 10*np.log10(Sxx/( p_ref )**2), vmin=db_min, vmax=db_max, cmap='viridis', shading='auto') # vmin=10,vmax=60 
    plt.title('Spectrogram')
    plt.xlabel("Time [s]")
    plt.ylabel("Frequency [Hz]")
    plt.ylim(f_min, f_max)
    plt.yscale('log')
    cbar = plt.colorbar()
    cbar.set_label(f'Amplitude {amp_lab}')# ref.'+f'{p_ref}'+r'$(\mu$[Pa])')
    plt.tight_layout()

    return freq_, t_, Sxx

###############################################
###############################################
def percentiles (SPL, v_perc):
    """
    Calculate the percentile value of SPL(t)

    Parameters
    ----------
    SPL : array
        time series of SPL
    v_perc : scalar
        Percentage of excedance [%]

    Returns
    -------
    N_n : scalar
        Value of SPL exceded the [%] of the time

    """
    N_n = np.percentile(SPL, v_perc, axis=0, method="closest_observation")
    return N_n
###############################################
###############################################
def n_octave_freq_bands(signal, sample_rate, n_frac, limits):
    splb, freqb  = PyOctaveBand.octavefilter(signal, fs=sample_rate, fraction=n_frac, limits = limits, order=6, show=0)
    freqb_list = [f"{num:.0f}" for num in freqb ]
    
    
    fig, ax = plt.subplots(figsize=(4, 2))

    plt.bar(freqb_list, splb, color='gray', edgecolor='black')
    plt.title(f'1/{int(n_frac)} oct. Bands')
    plt.ylabel('Amplitude [dBA]')
    plt.xlabel("Frequency [Hz]")
    plt.xticks(rotation=45)
    plt.ylim(-5,60)
    
    # Enable minor ticks (secondary grid)
    plt.grid(axis='y')
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())  
    ax.grid(which='minor', axis='y', linestyle='--', linewidth=0.5, alpha=0.5)

    plt.tight_layout()
        
    return splb, freqb

###############################################
###############################################
def wav_generation (multichannel_data_raw, name_file, channel, org_fs, new_fs=44100):
    data = multichannel_data_raw[:,channel]
    samp_rate = org_fs
    if org_fs != new_fs:
        # Downsample the audio data
        data = resampy.resample(data, org_fs, new_fs)
        samp_rate =  new_fs

    sf.write(name_file+f"micro{channel+1}.wav", data, samp_rate)