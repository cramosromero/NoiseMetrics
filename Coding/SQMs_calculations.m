% Script for calculating SQMs and Psychoacoustic annoyance based of the code examples from SQAT.
%Gil Felix Greco, Braunschweig 10.02.2025.
% Contributions form Michael Lotinga from Refmap are also included 
% ImAFUSA 2025
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clc; clear all; close all;

%% Load Signal to be assessed (mono .wav file)
base_path = cd;
dir_ref_sounds = [base_path filesep 'UAM_ImaFUSA' filesep 'SQMsMatlab' filesep 'audio_files' filesep ];
mono_signal_label = 'Ed_M3_10_F05_Y_W_134351_1micro5.wav';

% load mono signal [Nx1]
[signal.signal, signal.fs]=audioread([dir_ref_sounds mono_signal_label]);

fieldtype = 'free-frontal'; % string (default: 'free-frontal'; or 'diffuse')
time_skip = 350e-3;% time_skip, in seconds for statistical calculations (default: 304ms - avoids transient responses of the digital filters)
show = 0; % show results, 'false' (disable, default value) or 'true' (enable)
%% Compute Loudness (mono signal) (time-varying)

OUT_LOUD_ISO_mono = Loudness_ISO532_1( signal.signal, signal.fs,...  % input signal and sampling freq.
                                               0,...   % field; free field = 0; diffuse field = 1;
                                               2,...   % method; stationary (from input 1/3 octave unweighted SPL)=0; stationary = 1; time varying = 2; 
                                               0.5,... % time_skip, in seconds for level (stationary signals) and statistics (stationary and time-varying signals) calculations
                                               show);     % show results, 'false' (disable, default value) or 'true' (enable)

fprintf('\nLoudness (ISO532_1): \n');
fprintf('\t- Mean loudness value: %g (sone).\n', OUT_LOUD_ISO_mono.Nmean);
fprintf('\t- 5th percentile value: %g (sone).\n', OUT_LOUD_ISO_mono.N5);

N5_iso = OUT_LOUD_ISO_mono.N5;

%% Compute Loudness ECMA418_2 (mono signal)

OUT_LOUD_ECMA_mono = Loudness_ECMA418_2(signal.signal, signal.fs,... % input signal and sampling freq.
                                        fieldtype,... % string (default: 'free-frontal'; or 'diffuse')
                                        0.5,... % time_skip, in seconds for statistical calculations (default: 304ms - avoids transient responses of the digital filters)
                                        show); % show results, 'false' (disable, default value) or 'true' (enable)

fprintf('\nLoudness (ECMA-418-2:2024 - Hearing Model of Sottek): \n');
fprintf('\t- Overall loudness value: %g (sone).\n', OUT_LOUD_ECMA_mono.loudnessPowAvg);
fprintf('\t- 5th percentile value: %g (sone).\n', OUT_LOUD_ECMA_mono.N5);

N5_hm = OUT_LOUD_ECMA_mono.N5;
%% Compute Sharpness (according to DIN 45692)  (time-varying) from loudness input 
OUT_SHARP_DIN_L = Sharpness_DIN45692_from_loudness(OUT_LOUD_ISO_mono.InstantaneousSpecificLoudness,...  % input (time-varying) specific loudness
                                                          'DIN45692',...  % type of weighting function used for sharpness calculation
                                                              OUT_LOUD_ISO_mono.time,...  % time vector of the loudness calculation
                                                           3.5,...  % time_skip (second) for statistics calculation
                                                                  show);     % show sharpness results; true or false
                                                              
% display result
fprintf('\nSharpness (DIN45692): \n');
fprintf('Reference signal (60 dBSPL at 1kHz) based on a time-varying loudness\n');
fprintf('\t- Mean sharpness value: %g (acum).\n',OUT_SHARP_DIN_L.Smean);
fprintf('\t- 5th percentile value: %g (acum).\n',OUT_SHARP_DIN_L.S5);

S5_din = OUT_SHARP_DIN_L.S5;

%% Roughness (according to Daniel & Weber model)

OUT_ROUGH_DAW_mono = Roughness_Daniel1997(signal.signal, signal.fs,...  % input signal and sampling freq.
                        3.5,...  % time_skip, in seconds for statistical calculations
                                show);     % show results, 'false' (disable, default value) or 'true' (enable)  
                             
fprintf('\nRoughness (Daniel & Weber): \n');
fprintf('Reference signal (60 dB 1 kHz tone 100 %% modulated at 70 Hz)\n');
fprintf('\t- Mean roughness value: %g (asper).\n',OUT_ROUGH_DAW_mono.Rmean);
fprintf('\t- 5th percentile value: %g (asper).\n',OUT_ROUGH_DAW_mono.R5);

R5_dw = OUT_ROUGH_DAW_mono.R5;

%% Compute Roughness ECMA418_2 (mono signal)
% time_skip = 350e-3;% time_skip, in seconds for statistical calculations (default: 304ms - avoids transient responses of the digital filters)
OUT_ROUGH_ECMA_mono = Roughness_ECMA418_2(signal.signal, signal.fs,... % input signal and sampling freq.
                                            fieldtype,... % % string (default: 'free-frontal'; or 'diffuse')
                                            3.5,... % time_skip, in seconds for statistical calculations
                                            show); % show results, 'false' (disable, default value) or 'true' (enable)  
                              
fprintf('\nRoughness (ECMA-418-2:2024 - Hearing Model of Sottek): \n');
fprintf('Reference signal (60 dB 1 kHz tone 100 %% modulated at 70 Hz)\n');
fprintf('\t- Mean roughness value: %g (asper).\n',OUT_ROUGH_ECMA_mono.Rmean);
fprintf('\t- 5th percentile value: %g (asper).\n',OUT_ROUGH_ECMA_mono.R5);

R5_hm = OUT_ROUGH_ECMA_mono.R5;
% %% Compute Sharpness (mono signal) (time-varying)
% 
% OUT_SHARP_DIN_mono = Sharpness_DIN45692(signal.signal, signal.fs,...     % input signal and sampling frequency
%                                         'DIN45692',...     % Weight_Type, type of weighting function used for sharpness calculation
%                                                  0,...     % field used for loudness calculation; free field = 0; diffuse field = 1;
%                                                  2,...     % method used for loudness calculation: stationary (from input 1/3 octave unweighted SPL)=0; stationary = 1; time varying = 2;     
%                                                3.5,...     % time_skip (second) for statistics calculation
%                                                  1,...     % show sharpness results
%                                                  0);       % show loudness results
% 
% % display result
% fprintf('\nSharpness (DIN45692): \n');
% fprintf('Reference signal (60 dBSPL at 1kHz) based on a time-varying loudness\n');
% fprintf('\t- Mean sharpness value: %g (acum).\n',OUT_SHARP_DIN_mono.Smean);
% fprintf('\t- 5th percentile value: %g (acum).\n',OUT_SHARP_DIN_mono.S5);
% 
% S5_din = OUT_SHARP_DIN_mono.S5;
%% Compute Fluctuation strength (mono signal) Osses

OUT_FLUST_OSS_mono = FluctuationStrength_Osses2016(signal.signal, signal.fs,...  % input signal and sampling freq.
                                                    1,...  % method=0, stationary analysis- window size=length(insig); method=1, time_varying analysis - window size=2s
                                                    3.5,...  % time_skip, in seconds for statistical calculations
                                                    show);    % show results, 'false' (disable, default value) or 'true' (enable)

fprintf('\nFluctuation strength (Osses et al. model): \n');
fprintf('Reference signal (60 dB 1 kHz tone 100 %% modulated at 4 Hz)\n');
fprintf('\t- Mean fluctuation strength value of %g (vacil).\n',OUT_FLUST_OSS_mono.FSmean);
fprintf('\t- 5th percentile value: %g (vacil).\n',OUT_FLUST_OSS_mono.FS5);

F5 = OUT_FLUST_OSS_mono.FS5;

%% Compute Tonality Aures (mono signal)

OUT_TONAL_AURES_mono = Tonality_Aures1985(signal.signal, signal.fs,...  % input signal and sampling freq.
                                    0,...  % field for loudness calculation; free field = 0; diffuse field = 1;
                                    3.5,...  % time_skip, in seconds for level (stationary signals) and statistics (stationary and time-varying signals) calculations
                                    show);... % show results, 'false' (disable, default value) or 'true' (enable)
   
fprintf('\nTonality (Aures model): \n') 
fprintf('Reference signal (60 dBSPL 1 kHz tone)\n');
fprintf('\t- Mean tonality value of %g (t.u.).\n',OUT_TONAL_AURES_mono.Kmean);
fprintf('\t- 5th percentile value: %g (t.u.).\n',OUT_TONAL_AURES_mono.K5);

T5_aur = OUT_TONAL_AURES_mono.K5;

%% Compute Tonality ECMA418_2 (mono signal)
OUT_TONAL_ECMA_mono = Tonality_ECMA418_2(signal.signal, signal.fs,... % input signal and sampling freq.
                                            fieldtype,... % string (default: 'free-frontal'; or 'diffuse')
                                            3.5,... % time_skip, in seconds for level (stationary signals) and statistics (stationary and time-varying signals) calculations
                                            show); % show results, 'false' (disable, default value) or 'true' (enable)
                 
fprintf('\nTonality (ECMA-418-2:2024 - Hearing Model of Sottek): \n');
fprintf('Reference signal  (1-kHz pure tone with 40 dBSPL)\n');
fprintf('\t- Mean tonality value: %g (tu).\n',OUT_TONAL_ECMA_mono.tonalityAvg);
fprintf('\t- 5th percentile value: %g (tu).\n',OUT_TONAL_ECMA_mono.T5);

T5_hm = OUT_TONAL_ECMA_mono.T5;


%% PsychoacousticAnnoyance Model Zwicker1999

PA_Zwicker = PsychoacousticAnnoyance_Zwicker1999_from_percentile(N5_iso,... %5th percentile Loudness ISO 532-1:2017      
                                                                 S5_din,... %5th percentile Sharpness_DIN45692_from_loudness
                                                                 R5_dw,...  %5th percentile Roughness_Daniel1997
                                                                 F5);       %5th percentile FluctuationStrength_Osses2016
fprintf('\n Psychoacoustic Annoyance by Zwicker Model: \n');     
fprintf('\t- PA_Zwicker: %g (nd).\n',PA_Zwicker);

%% PsychoacousticAnnoyance Model Di2016
PA_Di  = PsychoacousticAnnoyance_Di2016_from_percentile(N5_iso,... %5th percentile Loudness ISO 532-1:2017
                                                        S5_din,... %5th percentile Sharpness_DIN45692_from_loudness
                                                        R5_dw,...  %5th percentile Roughness_Daniel1997
                                                        F5,...     %5th percentile FluctuationStrength_Osses2016
                                                        T5_aur);   %5th percentile Tonality_Aures1985

fprintf('\n Psychoacoustic Annoyance by Di Model: \n');     
fprintf('\t- PA_Di: %g (nd).\n',PA_Di);
%% PsychoacousticAnnoyance Model Boucher2024
PA_Boucher = PsychoacousticAnnoyance_Boucher2024_from_percentile(N5_iso,...  %5th percentile Loudness ISO 532-1:2017      
                                                                 S5_din,... %5th percentile Sharpness_DIN45692_from_loudness
                                                                 R5_hm,...  %5th percentile Roughness_ECMA418_2
                                                                 F5, ...    %5th percentile FluctuationStrength_Osses2016
                                                                 T5_hm);    %5th percentile Tonality_ECMA418_2
fprintf('\n Psychoacoustic Annoyance by Boucher Model: \n');     
fprintf('\t- PA_Boucher: %g (nd).\n',PA_Boucher);



%% EPNL calculation - method == 1 ( a calibrated sound file is used as input)
%#############################################################################

% same calibration as DO_slm  in Loudness_ECMA418_2 :
dBFS = 94; % a priori knowledge
dBoffset = 0.93; % determined empirically on to obtain the same values as DEWESOFT
                 % with this implementation and the one in PsySound.
calCoeff = 10.^((dBFS+dBoffset-93)/20);
signal.signal = calCoeff*signal.signal; % same as: insig = setdbspl(insig,rmsdb(insig)+dBFS,'dboffset',94);

% Target sampling rate
Fs_target = 48000; 
% Resample the signal
signal.signal = resample(signal.signal, Fs_target, signal.fs);
signal.fs = Fs_target;


% input parameters
method = 1;
dt = 0.5;
threshold = 10;

EPNL = EPNL_FAR_Part36(signal.signal, signal.fs,... % input signal and sampling freq.
                       method,... % method = 0, insig is a SPL[nTime,nFreq] matrix; method = 1, insig is a sound file
                       dt,... % time-step in which the third-octave SPLs are averaged, in seconds.
                       threshold,... % threshold value used to calculate the PNLT decay from PNLTM during the calculation of the duration correction
                       show);
