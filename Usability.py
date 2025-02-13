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
n_file = 0
data_rec = loadmat(mat_files[n_file])

# Constants

# Case of Study_N

COS_F = UAM_descriptive("F",data_rec,"A")


COS_F.psd_plots(channel=5, scaling="spectrum", on_new_plot=True, f_min=40,f_max=2000, db_min=-10, db_max=50 )

# COS_F.spectgram_plots(channel=5, scaling="spectrum", f_min=40,f_max=2000, db_min=-10, db_max=60 )

COS_F.oct_band_plots(channel=5, limits = [50, 2000])

# %%Some figures of UAM.Metrics

mic_number = 4 

fig_name = "pressure"
plt.figure(figsize=(4, 2))
plt.plot(COS_F.time_vec, COS_F.DATA_raw[:,mic_number], 'b')
plt.title(r'p(t)')
plt.xlabel('Time [s]')
plt.ylabel('AMplitude [Pa]')
plt.tight_layout()


fig_name = "SPL_A"
plt.figure(figsize=(4, 2))
plt.plot(COS_F.time_metrics, COS_F.SPL[:,mic_number],'b')
plt.plot(COS_F.time_vec, COS_F.DATA_acu[:,mic_number],'r')
plt.title('SPL [A-weighted, fast]')
plt.xlabel('Time [s]')
plt.ylim(40,80)
plt.ylabel('Amplitude [dBA]')
plt.tight_layout()


fig_name = "Leq_Lax_LAE"
fig,ax =plt.subplots(figsize=(6, 3))
plt.plot(COS_F.time_metrics, COS_F.SPL[:,mic_number], color='gray')
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



#Save the plot in SVG format
fig_name = "1_3_oct_band"
plt.savefig('saved_figures/'+f'{fig_name}.png', format='png', dpi=200)
