# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 12:11:19 2025

@author: ses271
"""

from matplotlib import pyplot as plt
from pathlib import Path
from scipy.io import loadmat
import numpy as np
from Drones import UAM_descriptive 


#%% DATA directories
 
## Folder containder the Recorded DATA
data_path = "../../Drone_DATA_Measurements/"
## Read the file for evaluation
forder_list = ["Ed_M3_10_F05_Y_W_134351_uw",
               "Ed_M3_10_HH_N_C_122827_nw"]

file_path = Path(data_path + forder_list[0]) # Ful Read Recorded data 
# file_path = Path(data_path + forder_list[1]) # Ful Read Recorded data
# 
# List all .mat files in the folder
mat_files = [f for f in file_path.iterdir() if f.suffix == ".mat"]

print(f"{len(mat_files)} available files")

#%% Cases of study

# Load data
n_file = 0 # choosing an specific .mat file from the recording's folder
data_rec = loadmat(mat_files[n_file])

# Constants

# Example of metrics calculations
COS_F = UAM_descriptive("F",data_rec,"A")

# Example of Pwer spectral density calcualtion
COS_F.psd_plots(channel=5, scaling="spectrum", on_new_plot=True, f_min=40,f_max=2000, db_min=-10, db_max=50 )

# Example of Spectrogram calculations
COS_F.spectgram_plots(channel=5, scaling="spectrum", f_min=40,f_max=2000, db_min=-10, db_max=60 )

# Example of 1/3 octave band representation
COS_F.oct_band_plots(channel=5, limits = [50, 2000])

# %%Some figures of UAM.Metrics

mic_number = 4 #As measurements are multichannel data, a simgle microhpne could be selected for ploting results.

fig_name = "pressure"
plt.figure(figsize=(4, 2))
plt.plot(COS_F.time_vec, COS_F.DATA_raw[:,mic_number], 'b')
plt.title(r'p(t)')
plt.xlabel('Time [s]')
plt.ylabel('AMplitude [Pa]')
plt.tight_layout()


# fig_name = "SPL_A"
# plt.figure(figsize=(4, 2))
# plt.plot(COS_F.time_metrics, COS_F.SPL[:,mic_number],'b')
# # plt.plot(COS_F.time_vec, COS_F.DATA_acu[:,mic_number],'r') #Comparison with SPL precalculated in Dewesoft.
# plt.title('SPL [A-weighted, fast]')
# plt.xlabel('Time [s]')
# plt.ylim(40,80)
# plt.ylabel('Amplitude [dBA]')
# plt.tight_layout()


fig_name = "Leq_Lax_LAE"
fig,ax =plt.subplots(figsize=(6, 3))
plt.plot(COS_F.time_metrics, COS_F.SPL[:,mic_number], color='blue')
plt.axhline(COS_F.Leq[mic_number], color='g',linestyle='-.',  label = r'$LA_{eq}$')
t_max = np.argmax(COS_F.SPL[:,mic_number])*COS_F.time_metrics[1]
# Plot vertical lines at x=Lmax-10 
mask_Lmax_down_10 = COS_F.SPL[:,mic_number]>( COS_F.Lmax[mic_number] - 10 ) # Levels Lmax-10dB
t_lae_level = np.array(COS_F.time_metrics)[mask_Lmax_down_10]
plt.axvline(x=t_lae_level[0], color='k', linestyle=':', label=r"time @ $LA_{max}-10$[dB]")
plt.axvline(x=t_lae_level[-1], color='k', linestyle=':')
# Plot bax integrating in 1 second 
x_bar = t_max
y_bar = COS_F.LE[mic_number]
bar_width = 1
plt.plot(t_max, COS_F.Lmax[mic_number], 'ko',  label = r'$LA_{max}$')
plt.plot(t_max, COS_F.LE[mic_number], 'b^', label= r'$LAE$')
ax.bar(x_bar, y_bar, width=bar_width, label='1[s]', alpha=0.8)
plt.legend(fontsize=8,ncol=3,loc='lower center' )
plt.title('SPL [A-weighted, fast]')
plt.xlabel('Time [s]')
plt.ylim(40,85)
plt.ylabel('Amplitude [dBA]')
plt.tight_layout()

# %% %HA People
x_LAeq = np.linspace(50, 100, 100)
HA_med_3kg = 100/(1+ np.exp(13.470 - 0.178 * x_LAeq))
HA_civ_aircr = 100/(1+ np.exp(18.940 - 0.229 * x_LAeq)) 

haLAeq_1 = 100/(1+ math.exp(13.470 - 0.178 * COS_F.Leq[mic_number]))
haLAeq_2 = 100/(1+ math.exp(18.940 - 0.229 * COS_F.Leq[mic_number]))

fig_name = "%HA"
fig,ax =plt.subplots(figsize=(6, 3))
plt.plot(x_LAeq, HA_med_3kg, '-k', label='Medium drone (3.0kg) by Gwak') # reference curve
plt.plot(x_LAeq, HA_civ_aircr, '--k', label='Civil aircraft by Gwak') # reference curve
plt.plot(COS_F.Leq[mic_number], haLAeq_1,'ob', label= 'UAS') # evaluated drone
plt.plot(COS_F.Leq[mic_number], haLAeq_2,'ob') # evaluated drone
plt.axhline(50, color='gray',linestyle=':',  label = '50%') # reference at 50%
plt.legend(fontsize=8,ncol=1)
plt.title('%HA curves for the noise of vehicles')
plt.xlabel(r'$LA_{eq} [dB]$')
plt.ylabel('%HA')
plt.tight_layout()


# Un comment for saving any plot in SVG format
#fig_name = "1_3_oct_band"
#plt.savefig('saved_figures/'+f'{fig_name}.png', format='png', dpi=200)
