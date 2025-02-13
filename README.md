# NoiseMetrics
NoiseMetrics for ImAFUSA
Date:13-Feb-2025
This repository contains the first group of Noise Metrics calculated at receiver positions.

The directory structure is:
MAIN---> Coding ---> Scripts ---> .py files
      ¦
    ---> Drone_DATA_Measurements ---> Ed_M3_10_F05_Y_W_134351_uw
                                  ¦
                                 ---> Ed_M3_10_HH_N_C_122827_nw
########################
Python Files description:

Drones.py : 
It contains the Class UAM, which is the blueprint for a basic acpustic characterization of a UAM noise signal measured at specific location.

utils.py :
It contains some filtering functions for the measured signals.

PyOctaveBand.py:
This script contains the definitions for calculating 1/3 octave band frequency representation.
from: https://github.com/jmrplens/PyOctaveBand

Usability.py : 
This iscript present an example of using the class UAM for characterizing UAM noise measurements.
The imputs are a 9-channel measurements .mat files contained in the the folder: "Drone_DATA_Measurements"

########################
Drone_DATA_Measurements folter contains two subfolders which could have more than one measurement of the same UAM operation. 

--> Ed_M3_10_F05_Y_W_134351_uw 
--> Ed_M3_10_HH_N_C_122827_nw

The self explained folder names structure is "Aa_Bb_Cc_Dd_E_F_GGGGGG_hh" wich means as follow:
Aa: Pylot (Ed) Edinburgh Drone Company
Bb: Drone Model (M3) DJI Matrice RTK 300
Cc: Flyover altiture (10m) above the ground level. 
Dd: UAM Operation Flyover(F) speed (05 m/s) or hovering (HH).
E: If pyload is attached (Y/N).  
F: Starting point of te UAM manouver (W) coming form west, (C) above the central microphone. 
GGGGGG: timestamp (hhmmss)
hh: operational direction respect to wind (uw) upwind, (nw) no-wind

Drone noise measurements were obtained as described in https://doi.org/10.1016/j.ast.2023.108537
Ramos-Romero, C., Green, N., Torija, A. J., & Asensio, C. (2023). On-field noise measurements and acoustic characterisation of multi-rotor small unmanned aerial systems. Aerospace Science and Technology, 141, 108537.
