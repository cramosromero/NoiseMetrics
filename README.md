# NoiseMetrics
NoiseMetrics for ImAFUSA\
Date:13-Feb-2025\
This repository contains the first group of Noise Metrics calculated at receiver positions.

The directory structure is:\
 * MAIN
 * Coding
   * Scripts
     * .py files
 * Drone_DATA_Measurements
   * Ed_M3_10_F05_Y_W_134351_uw
     * .mat files
   * Ed_M3_10_HH_N_C_122827_nw
     * .mat files

## Python Files description:

Drones.py :\ 
It contains the Class UAM, which is the blueprint for a basic acpustic characterization of a UAM noise signal measured at specific location.

utils.py :\
It contains some filtering functions for the measured signals.

PyOctaveBand.py:\
This script contains the definitions for calculating 1/3 octave band frequency representation.
from: https://github.com/jmrplens/PyOctaveBand

Usability.py : \
This iscript present an example of using the class UAM for characterizing UAM noise measurements.
The imputs are a 9-channel measurements .mat files contained in the the folder: "Drone_DATA_Measurements"

## Some results
### Pressure time-series
 
![00 pressure](https://github.com/user-attachments/assets/a87b3a87-969c-4e61-a81b-7f03af1293a5)

### Sound Pressurer Level

![01 SPL_A](https://github.com/user-attachments/assets/c226b16d-8a74-40bd-90ff-c8569aa4ac24)
   
### Power Spectral Density

![02 spectrum](https://github.com/user-attachments/assets/ef56331f-998f-4854-99f2-6941ee6b6344)
   
### Frequency band representation

![03 bands](https://github.com/user-attachments/assets/0da526bd-70ec-4ed3-aa67-43a6406fb813)
   
### Spectrogram

![04 spectrogram](https://github.com/user-attachments/assets/efb24596-e22d-4cef-80db-136f4b8d79d5)
   
### LAmax, LAeq, LAE

![05 Leq_Lax_LAE](https://github.com/user-attachments/assets/d8e5a9cf-6962-4d10-88e8-d216e31d2f29)

## UAM measurements data description:
Drone_DATA_Measurements folter contains two subfolders which could have more than one measurement of the same UAM operation. 

 * Ed_M3_10_F05_Y_W_134351_uw
 * Ed_M3_10_HH_N_C_122827_nw

The self explained folder names structure is "Aa_Bb_Cc_Dd_E_F_GGGGGG_hh" as follow:\

Aa:      Pylot (Ed) Edinburgh Drone Company\
Bb:      Drone Model (M3) DJI Matrice RTK 300\
Cc:      Flyover altiture (10m) above the ground level\
Dd:      UAM Operation Flyover(F) speed (05 m/s) or hovering (HH)\
E:       If pyload is attached (Y/N)\
F:       Starting point of te UAM manouver (W) coming form west, (C) above the central microphone\ 
GGGGGG:  Timestamp (hhmmss)\
hh:      Operational direction respect to wind (uw) upwind, (nw) no-wind\

> Drone noise measurements were obtained as described in https://doi.org/10.1016/j.ast.2023.108537
> Ramos-Romero, C., Green, N., Torija, A. J., & Asensio, C. (2023). On-field noise measurements and acoustic characterisation of multi-rotor small unmanned aerial systems. Aerospace Science and Technology, 141, 108537.

> Sound quality metrics were calculated by SQUAT  in https://doi.org/10.5281/zenodo.7934709 https://github.com/ggrecow/SQAT
> Felix Greco, G., Merino-Martínez, R., & Osses, A. (2023). SQAT: a sound quality analysis toolbox for MATLAB. Zenodo.
