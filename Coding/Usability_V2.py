# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 12:11:19 2025

@author: ses271
"""
import os
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg') 
from pathlib import Path
from scipy.io import loadmat
import numpy as np
from Drones import UAM_descriptive, UAM_definition
import utils
import math

plt.close('all')
#%% DATA directories
 
## Folder containder the Recorded DATA
data_path = "../../Drone_DATA_Measurements/"
## Read the file for evaluation
forder_list = ["Ed_M3_10_F05_Y_W_134351_uw",
               "Ed_M3_10_HH_N_C_122827_nw"]

ope = forder_list[0]

file_path = Path(data_path + ope) # Ful Read Recorded data 
# file_path = Path(data_path + forder_list[1]) # Ful Read Recorded data
# 
# List all .mat files in the folder
mat_files = [f for f in file_path.iterdir() if f.suffix == ".mat"]

print(f"{len(mat_files)} available files")

#%% Cases of study

# Load data
n_file = 1
ID = os.path.basename(mat_files[n_file])
data_rec = loadmat(mat_files[n_file])

# Constants

# Case of Study_N
operation = ID[9:10] # flyover or hovering
COS_F = UAM_descriptive(operation,data_rec,"A",t_value=0.125)

# %%Some figures of UAM.Metrics
fig_name = "spectrum"
COS_F.psd_plots(channel=5, scaling="spectrum", on_new_plot=True, f_min=40,f_max=2000, db_min=-10, db_max=50 )
plt.savefig(f"{fig_name}{ope[9:10]}"+".eps", format='eps', dpi=300, bbox_inches='tight')


fig_name = "spectrogram"
COS_F.spectgram_plots(channel=5, scaling="spectrum", f_min=40,f_max=2000, db_min=-10, db_max=60 )
plt.savefig(f"{fig_name}{ope[9:10]}"+".png", dpi=300, bbox_inches='tight')  # High-quality PNG

fig_name = "1_3_oct_band"
COS_F.oct_band_plots(channel=5, limits = [50, 10000])
plt.savefig(f"{fig_name}{ope[9:10]}"+".eps", format='eps', dpi=300, bbox_inches='tight')

mic_number = 4 

fig_name = "pressure"
plt.figure(figsize=(4, 2))
plt.plot(COS_F.time_vec, COS_F.DATA_raw[:,mic_number], 'b')
plt.title(r'p(t)')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude [Pa]')
plt.tight_layout()
plt.savefig(f"{fig_name}{ope[9:10]}"+".eps", format='eps', dpi=300, bbox_inches='tight')


fig_name = "SPL_A"
plt.figure(figsize=(4, 2))
plt.plot(COS_F.time_metrics, COS_F.SPL[:,mic_number],'b')
# plt.plot(COS_F.time_vec, COS_F.DATA_acu[:,mic_number],'r') #Comparison with SPL precalculated in Dewesoft.
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
plt.savefig(f"{fig_name}{ope[9:10]}"+".eps", format='eps', dpi=300, bbox_inches='tight')

# %% %HA People
if operation == 'H':
    
    x_LAE = np.linspace(50, 100, 100)
    #Courves as reference
    HA_D1 = 100/(1+ np.exp(-0.168 *(x_LAE-82.8)))
    HA_D2 = 100/(1+ np.exp(-0.152 *(x_LAE-78.9)))
    HA_D3 = 100/(1+ np.exp(-0.138 *(x_LAE-77.4)))
    HA_D4 = 100/(1+ np.exp(-0.158 *(x_LAE-81.8)))
    HA_El = 100/(1+ np.exp(-0.116 *(x_LAE-92.2)))
    
    #assessed UAS
    # haLAE_D1 = 100/(1+ math.exp(-0.168*(COS_F.LE[mic_number]-82.8)))
    # haLAE_D2 = 100/(1+ math.exp(-0.152*(COS_F.LE[mic_number]-78.9)))
    # haLAE_D3 = 100/(1+ math.exp(-0.138*(COS_F.LE[mic_number]-77.4)))
    # haLAE_D4 = 100/(1+ math.exp(-0.158*(COS_F.LE[mic_number]-81.8)))
    # haLAE_El = 100/(1+ math.exp(-0.116*(COS_F.LE[mic_number]-92.2)))

    
    fig_name = "%HA"
    fig,ax =plt.subplots(figsize=(6, 3))
    plt.plot(x_LAE, HA_D1, '--k', label='Drone 1 by Aalmoes-EASA') # reference curve
    plt.plot(x_LAE, HA_D2, ':k', label='Drone 2 by Aalmoes-EASA') # reference curve
    plt.plot(x_LAE, HA_D3, '-.k', label='Drone 3 by Aalmoes-EASA') # reference curve
    plt.plot(x_LAE, HA_D4, linestyle=(0, (3, 5, 1, 5, 1, 5)) , color ='k', label='Drone 4 by Aalmoes-EASA') # reference curve
    plt.plot(x_LAE, HA_El, '--k',  label='Helicopter 1 by Aalmoes-EASA') # reference curve
    
    
    plt.plot(COS_F.LE[mic_number], 50,'ob', label= 'UAS') # evaluated drone
    # plt.plot(COS_F.LE[mic_number], haLAE_D1,'ob', label= 'UAS') # evaluated drone
    # plt.plot(COS_F.LE[mic_number], haLAE_D2,'ob') # evaluated drone
    # plt.plot(COS_F.LE[mic_number], haLAE_D3,'ob') # evaluated drone
    # plt.plot(COS_F.LE[mic_number], haLAE_D4,'ob') # evaluated drone
    # plt.plot(COS_F.LE[mic_number], haLAE_El,'ob') # evaluated drone

    plt.axhline(50, color='green',linestyle=':',  label = '50%') # reference at 50%
    plt.legend(fontsize=8,ncol=1)
    plt.title('%HA curves for the noise of vehicles')
    plt.xlabel(r'$LA_{eq}$')
    plt.ylabel('%HA')
    plt.tight_layout()
    
elif operation == 'F':
    
    x_LAeq = np.linspace(50, 100, 100)
    #Courves as reference
    HA_med_3kg = 100/(1+ np.exp(13.470 - 0.178 * x_LAeq))
    HA_large = 100/(1+ np.exp(12.184 - 0.165 * x_LAeq))
    HA_civ_aircr = 100/(1+ np.exp(18.940 - 0.229 * x_LAeq)) 
    
    #assessed UAS
    # haLAeq_1 = 100/(1+ math.exp(13.470 - 0.178 * COS_F.Leq[mic_number]))
    # haLAeq_2 = 100/(1+ math.exp(12.184- 0.165 * COS_F.Leq[mic_number]))
    # haLAeq_3 = 100/(1+ math.exp(18.940 - 0.229 * COS_F.Leq[mic_number]))
    
    fig_name = "%HA"
    fig,ax =plt.subplots(figsize=(6, 3))
    plt.plot(x_LAeq, HA_med_3kg, '-k', label='Medium drone (3.0kg) by Gwak') # reference curve
    plt.plot(x_LAeq, HA_large, '-.k', label='Large drone by Gwak') # reference curve
    plt.plot(x_LAeq, HA_civ_aircr, '--k', label='Civil aircraft by Gwak') # reference curve
    
    plt.plot(COS_F.Leq[mic_number], 50,'ob', label= 'UAS') # evaluated drone
    # plt.plot(COS_F.Leq[mic_number], haLAeq_1,'ob') # evaluated drone
    # plt.plot(COS_F.Leq[mic_number], haLAeq_2,'ob') # evaluated drone
    # plt.plot(COS_F.Leq[mic_number], haLAeq_3,'ob') # evaluated drone
    
    plt.axhline(50, color='green',linestyle=':',  label = '50%') # reference at 50%
    plt.legend(fontsize=8,ncol=1)
    plt.title('%HA curves for the noise of vehicles')
    plt.xlabel(r'$LAE$')
    plt.ylabel('%HA')
    plt.tight_layout()
else: 
    print('no courves')
plt.savefig(f"{fig_name}{ope[9:10]}"+".eps", format='eps', dpi=300, bbox_inches='tight')
plt.show()
# %% Wav generation
utils.wav_generation(COS_F.DATA_raw,  ID[0:-4], 
                     channel = 4, 
                     org_fs = COS_F.fs, new_fs=44100)
# %% Save the plot in SVG format
# plt.savefig('saved_figures/'+f'{fig_name}.png', format='png', dpi=200)

# COS_F_dep = UAM_definition(rad_deprop=200)
# COS_F_dep.rad_deprop
# COS_F_dep.radio_dec

