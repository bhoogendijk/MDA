import matplotlib.pyplot

import helpers
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# This script is setup to make the plots with the data that was collected in Rotterdam Port while playing the motion
# files for the Equinor TRL5 qualification on 27-09-2022. Four files were played, a selector is created to select which
# one is plotted.

# SECTION 1: SELECTING WHICH FILES TO LOAD

file_selector = 1

# input datafiles
if file_selector == 1: filename_input = "NORMAND_Tp070_Hs200_Hdg000_Parallel.xlsx"
if file_selector == 2: filename_input = "NORMAND_Tp070_Hs200_Hdg000_Perpendicular.xlsx"
if file_selector == 3: filename_input = "NORMAND_Tp110_Hs200_Hdg000_Parallel.xlsx"
if file_selector == 4: filename_input = "NORMAND_Tp110_Hs200_Hdg000_Perpendicular.xlsx"

# output datafiles
initialdiroutput = "C:/Users/b.hoogendijk/PycharmProjects/MDA/Projects/Equinor qualification/Simulations with hostsim/Logging data (output)/TRL5"

if file_selector == 1:
    filenames_output = ['BM_AS10_220927T204056_Tp07Hs200Parallel_na.csv',
                        'BM_AS10_220927T204301_Tp07Hs200Parallel_na.csv']
if file_selector == 2:
    filenames_output = ['BM_AS10_220927T205720_Tp07Hs200Perp_na.csv',
                        'BM_AS10_220927T211145_Tp07Hs200Perp_na.csv']
if file_selector == 3:
    filenames_output = ['BM_AS10_220927T211354_Tp11Hs200Par_na.csv',
                        'BM_AS10_220927T212802_Tp11Hs200Par_na.csv']
if file_selector == 4:
    filenames_output = ['BM_AS10_220927T212940_Tp11Hs200Per_na.csv',
                        'BM_AS10_220927T214410_Tp11Hs200Per_na.csv']

# SECTION 2: SELECT THE PLOTS TO SHOW
save_figures = True  # save  the figures that are plotted
show_figures = True  # show  the figures that are plotted

# SECTION 3: LOADING THE FILES

# load output
pathname = []
for fn in filenames_output:
    pathname.append(os.path.join(initialdiroutput, fn))
df_log = helpers.load(pathname, save_to_feather=False, initialdir=initialdiroutput)

# CALCULATE ADDITIONAL INFORMATION ABOUT LOADED DATA
# calculate cylinder velocities and duty cycle
df_log = helpers.add_derivative_data(df_log)

df_log['Platform_Roll_CIMS'] = np.arctan((1 / 2 * df_log['Cyl1_Pos_CIMS'] + 1 / 2 * df_log['Cyl2_Pos_CIMS'] - df_log[
    'Cyl3_Pos_CIMS']) / 11951.1) * 180 / np.pi  # for 270 degree rotation
df_log['Platform_Pitch_CIMS'] = np.arctan(
    (df_log['Cyl1_Pos_CIMS'] - df_log['Cyl2_Pos_CIMS']) / 13800.0) * 180 / np.pi  # for 270 degree rotation
df_log['Platform_Heave_CIMS'] = (df_log['Cyl1_Pos_CIMS'] + df_log['Cyl2_Pos_CIMS'] + df_log['Cyl3_Pos_CIMS']) / 3 - 1250

df_log['Platform_Roll_MRU4'] = df_log['MRUp_Roll']
df_log['Platform_Pitch_MRU4'] = df_log['MRUp_Pitch']
df_log['Platform_Heave_MRU4'] = df_log['MRUp_Heave']

df_log['Residual_Roll_CIMS'] = df_log['MRU1_Roll'] + df_log['Platform_Roll_CIMS']
df_log['Residual_Pitch_CIMS'] = df_log['MRU1_Pitch'] + df_log['Platform_Pitch_CIMS']
df_log['Residual_Heave_CIMS'] = df_log['MRU1_Heave'] + df_log['Platform_Heave_CIMS']

df_log['Residual_Roll_MRU4'] = df_log['MRU1_Roll'] + df_log['Platform_Roll_MRU4']
df_log['Residual_Pitch_MRU4'] = df_log['MRU1_Pitch'] + df_log['Platform_Pitch_MRU4']
df_log['Residual_Heave_MRU4'] = df_log['MRU1_Heave'] + df_log['Platform_Heave_MRU4']

# calculate velocity derivatives
df_log['MRU1_Roll_vel'] = df_log['MRU1_Roll'].diff() / df_log['Timestamp'].diff().dt.total_seconds()
df_log['Platform_Roll_CIMS_vel'] = df_log['Platform_Roll_CIMS'].diff() / df_log['Timestamp'].diff().dt.total_seconds()
df_log['Platform_Roll_MRU4_vel'] = df_log['Platform_Roll_MRU4'].diff() / df_log['Timestamp'].diff().dt.total_seconds()

df_log['MRU1_Pitch_vel'] = df_log['MRU1_Pitch'].diff() / df_log['Timestamp'].diff().dt.total_seconds()
df_log['Platform_Pitch_CIMS_vel'] = df_log['Platform_Pitch_CIMS'].diff() / df_log['Timestamp'].diff().dt.total_seconds()
df_log['Platform_Pitch_MRU4_vel'] = df_log['Platform_Pitch_MRU4'].diff() / df_log['Timestamp'].diff().dt.total_seconds()

df_log['MRU1_Heave_Velocity'] = df_log['MRU1_Heave'].diff() / df_log['Timestamp'].diff().dt.total_seconds()
df_log['Platform_Heave_CIMS_vel'] = df_log['Platform_Heave_CIMS'].diff() / df_log['Timestamp'].diff().dt.total_seconds()
df_log['Platform_Heave_MRU4_vel'] = df_log['Platform_Heave_MRU4'].diff() / df_log['Timestamp'].diff().dt.total_seconds()

# calculate the residuals
df_log['Residual_Heave_CIMS_vel'] = df_log['MRU1_Heave_Velocity'] + df_log['Platform_Heave_CIMS_vel']
df_log['Residual_Heave_MRU4_vel'] = df_log['MRU1_Heave_Velocity'] - df_log['Platform_Heave_MRU4_vel']

# Filter the signals
moving_average = 5
df_log['MRU1_Roll_vel_filtered'] = df_log['MRU1_Roll_vel'].rolling(moving_average).sum() / moving_average
df_log['Platform_Roll_CIMS_vel_filtered'] = df_log['Platform_Roll_CIMS_vel'].rolling(moving_average).sum() / moving_average
df_log['Platform_Roll_MRU4_vel_filtered'] = df_log['Platform_Roll_MRU4_vel'].rolling(moving_average).sum() / moving_average

df_log['MRU1_Pitch_vel_filtered'] = df_log['MRU1_Pitch_vel'].rolling(moving_average).sum() / moving_average
df_log['Platform_Pitch_CIMS_vel_filtered'] = df_log['Platform_Pitch_CIMS_vel'].rolling(moving_average).sum() / moving_average
df_log['Platform_Pitch_MRU4_vel_filtered'] = df_log['Platform_Pitch_MRU4_vel'].rolling(moving_average).sum() / moving_average

df_log['MRU1_Heave_Velocity_filtered'] = df_log['MRU1_Heave_Velocity'].rolling(moving_average).sum() / moving_average
df_log['Platform_Heave_CIMS_vel_filtered'] = df_log['Platform_Heave_CIMS_vel'].rolling(moving_average).sum() / moving_average

# Calculate the filtered residuals
df_log['Residual_Roll_CIMS_vel_filtered'] = df_log['MRU1_Roll_vel_filtered'] + df_log['Platform_Roll_CIMS_vel_filtered']
df_log['Residual_Roll_MRU4_vel_filtered'] = df_log['MRU1_Roll_vel_filtered'] + df_log['Platform_Roll_MRU4_vel_filtered']

df_log['Residual_Pitch_CIMS_vel_filtered'] = df_log['MRU1_Pitch_vel_filtered'] + df_log['Platform_Pitch_CIMS_vel_filtered']
df_log['Residual_Pitch_MRU4_vel_filtered'] = df_log['MRU1_Pitch_vel_filtered'] + df_log['Platform_Pitch_MRU4_vel_filtered']

df_log['Residual_Heave_MRU4_vel_filtered'] = df_log['MRU1_Heave_Velocity_filtered'] - df_log['Platform_Heave_MRU4_vel']
df_log['Residual_Heave_CIMS_vel_filtered'] = df_log['MRU1_Heave_Velocity_filtered'] + df_log['Platform_Heave_CIMS_vel_filtered']

# # PLOTTING SECTION

# PLOT ROLL PITCH AND HEAVE MOTIONS. MRU MEASURED MOTION AND CIMS CALCULATED PLATFORM MOTION
figRPH, ax = plt.subplots(3, 2, sharex=True, sharey='row')

# Share the Y axis between the roll and pitch values
ax[0, 0].get_shared_y_axes().join(ax[0, 0], ax[1, 0])

df_log.plot(ax=ax[0, 0], y=['MRU1_Roll'], x='Timestamp', kind='line')
df_log.plot(ax=ax[0, 0], y=['Platform_Roll_CIMS'], x='Timestamp', kind='line')
# df_source.plot(ax=ax[0, 0], y=['ROLL'], x='Timestamp', kind='line')
ax[0, 0].set_ylabel('Roll [deg]')
ax[0, 0].legend(['Vessel Roll Amplitude', 'Platform Roll Amplitude'])

df_log.plot(ax=ax[1, 0], y=['MRU1_Pitch'], x='Timestamp', kind='line')
df_log.plot(ax=ax[1, 0], y=['Platform_Pitch_CIMS'], x='Timestamp', kind='line')
# df_source.plot(ax=ax[1, 0], y=['PITCH'], x='Timestamp', kind='line')
ax[1, 0].set_ylabel('Pitch [deg]')
ax[1, 0].legend(['Vessel Pitch Amplitude', 'Platform Pitch Amplitude'])

df_log.plot(ax=ax[2, 0], y=['MRU1_Heave'], x='Timestamp', kind='line')
df_log.plot(ax=ax[2, 0], y=['Platform_Heave_CIMS'], x='Timestamp', kind='line')
# df_source.plot(ax=ax[2, 0], y=['HEAVE'], x='Timestamp', kind='line')
ax[2, 0].set_ylabel('Heave [mm]')
ax[2, 0].legend(['Vessel Heave Amplitude', 'Platform Heave Amplitude'])

# limit the heave values to 6 times the standard deviation to prevent unstable heave signal dominating the plot
std = df_log['MRU1_Heave'].std()
plt.ylim(-6 * std, 6 * std)

df_log.plot(ax=ax[0, 1], y=['Residual_Roll_CIMS'], x='Timestamp', kind='line')
ax[0, 1].set_ylabel('Roll [deg]')
ax[0, 1].legend(['Residual Roll Amplitude'])

df_log.plot(ax=ax[1, 1], y=['Residual_Pitch_CIMS'], x='Timestamp', kind='line')
ax[1, 1].set_ylabel('Pitch [deg]')
ax[1, 1].legend(['Residual Pitch Amplitude'])

df_log.plot(ax=ax[2, 1], y=['Residual_Heave_CIMS'], x='Timestamp', kind='line')
ax[2, 1].set_ylabel('Heave [mm]')
ax[2, 1].legend(['Residual Heave Amplitude'])

# PLOT ROLL PITCH AND HEAVE VELOCITIES. MRU MEASURED MOTION AND CIMS CALCULATED PLATFORM MOTION
figRPHvel, ax = plt.subplots(3, 2, sharex=True, sharey='row')

# Share the Y axis between the roll and pitch values
ax[0, 0].get_shared_y_axes().join(ax[0, 0], ax[1, 0])
df_log['Residual_Heave_CIMS_vel_filtered']

df_log.plot(ax=ax[0, 0], y=['MRU1_Roll_vel_filtered'], x='Timestamp', kind='line')
df_log.plot(ax=ax[0, 0], y=['Platform_Roll_CIMS_vel_filtered'], x='Timestamp', kind='line')
# df_source.plot(ax=ax[0, 0], y=['ROLL'], x='Timestamp', kind='line')
ax[0, 0].set_ylabel('Roll Velocity [deg/s]')
ax[0, 0].legend(['Vessel Roll Velocity', 'Platform Roll Velocity'])

df_log.plot(ax=ax[1, 0], y=['MRU1_Pitch_vel_filtered'], x='Timestamp', kind='line')
df_log.plot(ax=ax[1, 0], y=['Platform_Pitch_CIMS_vel_filtered'], x='Timestamp', kind='line')
# df_source.plot(ax=ax[1, 0], y=['PITCH'], x='Timestamp', kind='line')
ax[1, 0].set_ylabel('Pitch Velocity [deg/s]')
ax[1, 0].legend(['Vessel Pitch Velocity', 'Platform Pitch Velocity'])

df_log.plot(ax=ax[2, 0], y=['MRU1_Heave_Velocity_filtered'], x='Timestamp', kind='line')
df_log.plot(ax=ax[2, 0], y=['Platform_Heave_CIMS_vel_filtered'], x='Timestamp', kind='line')
# df_source.plot(ax=ax[2, 0], y=['HEAVE'], x='Timestamp', kind='line')
ax[2, 0].set_ylabel('Heave Velocity [mm/s]')
ax[2, 0].legend(['Vessel Heave Velocity', 'Platform Heave Velocity'])

# limit the heave values to 6 times the standard deviation to prevent unstable heave signal dominating the plot
std = df_log['MRU1_Heave_Velocity_filtered'].std()
plt.ylim(-6 * std, 6 * std)

df_log.plot(ax=ax[0, 1], y=['Residual_Roll_CIMS_vel_filtered'], x='Timestamp', kind='line')
ax[0, 1].set_ylabel('Roll Velocity [deg/s]')
ax[0, 1].legend(['Residual Roll Velocity'])

df_log.plot(ax=ax[1, 1], y=['Residual_Pitch_CIMS_vel_filtered'], x='Timestamp', kind='line')
ax[1, 1].set_ylabel('Pitch Velocity [deg/s]')
ax[1, 1].legend(['Residual Pitch Velocity'])

df_log.plot(ax=ax[2, 1], y=['Residual_Heave_CIMS_vel_filtered'], x='Timestamp', kind='line')
ax[2, 1].set_ylabel('Heave Velocity [mm]')
ax[2, 1].legend(['Residual Heave Velocity'])



# PLOT THE HEAVE VELOCITY ONLY
fig_heave_vel, ax = plt.subplots(1, 2, sharex=True, sharey=True)

df_log.plot(ax=ax[0], y=['MRU1_Heave_Velocity_filtered'], x='Timestamp', kind='line')
df_log.plot(ax=ax[0], y=['Platform_Heave_CIMS_vel_filtered'], x='Timestamp', kind='line')
ax[0].set_ylabel('Heave Velocity [mm/s]')
ax[0].legend(['Vessel Heave Velocity', 'Platform Heave Velocity'])

df_log.plot(ax=ax[1], y=['Residual_Heave_CIMS_vel_filtered'], x='Timestamp', kind='line')
ax[1].set_ylabel('Heave Velocity [mm/s]')
ax[1].axhline(356, color='k')
ax[1].axhline(-356, color='k')
ax[1].legend(['Residual Heave Velocity', 'Residual Heave Velocity limit'])

plt.ylim(-800, 800)


# show the plots
if show_figures:
    plt.show()

if save_figures:
    figRPH.savefig(filename_input[:-4]+' - RPH Amplitude.png')
    figRPHvel.savefig(filename_input[:-4]+' - RPH Velocity.png')
    fig_heave_vel.savefig(filename_input[:-4]+' - Heave Velocity.png')

