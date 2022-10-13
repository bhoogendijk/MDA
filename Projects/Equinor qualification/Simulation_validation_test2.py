import helpers
import plotters
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# import mplcursors
import os

# input datafiles
initialdirinput = "C:/Users/b.hoogendijk/PycharmProjects/MDA\Projects/Equinor qualification\Simulations with hostsim/Time traces (input)\OrcaFlex"
filename_input = "NORMAND_Tp070_Hs200_Hdg000_Parallel.xlsx"

# output datafiles
initialdiroutput = "C:/Users/b.hoogendijk/Desktop/BM folder copies/281 Equinor - Qualification process Equinor T700/Engineering\Simulations with hostsim/autosave"

filenames_output = [
    'BM_AS10_221009T071137_endurance_test_offshore_na.csv',
    'BM_AS10_221009T072637_endurance_test_offshore_na.csv',
    'BM_AS10_221009T074137_endurance_test_offshore_na.csv',
    'BM_AS10_221009T075637_endurance_test_offshore_na.csv',
    'BM_AS10_221009T081137_endurance_test_offshore_na.csv',
    'BM_AS10_221009T082637_endurance_test_offshore_na.csv',
    'BM_AS10_221009T084137_endurance_test_offshore_na.csv',
    'BM_AS10_221009T085637_endurance_test_offshore_na.csv',
    'BM_AS10_221009T091137_endurance_test_offshore_na.csv',
    'BM_AS10_221009T092637_endurance_test_offshore_na.csv',
    'BM_AS10_221009T094137_endurance_test_offshore_na.csv',
    'BM_AS10_221009T095637_endurance_test_offshore_na.csv',
    'BM_AS10_221009T101137_endurance_test_offshore_na.csv',
    'BM_AS10_221009T102637_endurance_test_offshore_na.csv',
    'BM_AS10_221009T104137_endurance_test_offshore_na.csv',
    'BM_AS10_221009T105637_endurance_test_offshore_na.csv',
    'BM_AS10_221009T111137_endurance_test_offshore_na.csv',
    'BM_AS10_221009T112637_endurance_test_offshore_na.csv',
    'BM_AS10_221009T114137_endurance_test_offshore_na.csv',
    'BM_AS10_221009T115637_endurance_test_offshore_na.csv',
    'BM_AS10_221009T121137_endurance_test_offshore_na.csv',
    'BM_AS10_221009T122637_endurance_test_offshore_na.csv',
    'BM_AS10_221009T124137_endurance_test_offshore_na.csv',
    'BM_AS10_221009T125637_endurance_test_offshore_na.csv',
    'BM_AS10_221009T131137_standby_na.csv']

# load output
pathname = []
for fn in filenames_output:
    pathname.append(os.path.join(initialdiroutput, fn))
df_log = helpers.load(pathname, save_to_feather=True, initialdir=initialdiroutput)

# load input
pathname_input = os.path.join(initialdirinput, filename_input)
df_source = pd.read_excel(pathname_input)
#
# CHANGE THE SOURCE UNITS TO MATCH THE OUTPUT
df_source['HEAVE'] *= 1000  # Source uses meters as input, we will adjust to mm
# give timestamp to input
timestamps = []
for i in range(df_source.shape[0]):
    timestamp = pd.Timestamp(
        df_log['Timestamp'].values[0] + pd.Timedelta(seconds=df_source['TIME'].values[i]))
    timestamps.append(timestamp)
df_source.insert(0, "Timestamp", timestamps, allow_duplicates=False)
df_source.set_index(df_source['Timestamp'], inplace=True)

df_source['HEAVE_vel'] = df_source['HEAVE'].diff() / df_source['Timestamp'].diff().dt.total_seconds()

df_log = helpers.add_derivative_data(df_log)

standard_deviations = np.array([[df_source['ROLL'].std(), df_log['MRU1_Roll'].std()],
                                [df_source['PITCH'].std(), df_log['MRU1_Pitch'].std()],
                                [df_source['HEAVE'].std(), df_log['MRU3_Heave'].std()],
                                [df_source['HEAVE_vel'].std(), df_log['MRU3_Heave_Velocity'].std()]
                                ])

print(standard_deviations * 3)

# PLOT ROLL PITCH AND HEAVE. MRU MEASURED MOTION AND SIMULATION MOTIONS
figRPH, ax = plt.subplots(4, 2, sharex='col', sharey='row')

df_source.plot(ax=ax[0, 0], y=['ROLL'], x='Timestamp', kind='line')
df_log.plot(ax=ax[0, 1], y=['MRU1_Roll'], x='Timestamp', kind='line')
ax[0, 0].set_ylabel('Roll [deg]')
ax[0, 0].legend(['Simulated Roll'])
ax[0, 1].legend(['Measured Roll'])

df_source.plot(ax=ax[1, 0], y=['PITCH'], x='Timestamp', kind='line')
df_log.plot(ax=ax[1, 1], y=['MRU1_Pitch'], x='Timestamp', kind='line')
ax[1, 0].set_ylabel('Pitch [deg]')
ax[1, 0].legend(['Simulated Pitch'])
ax[1, 1].legend(['Measured Pitch'])

df_source.plot(ax=ax[2, 0], y=['HEAVE'], x='Timestamp', kind='line')
df_log.plot(ax=ax[2, 1], y=['MRU3_Heave'], x='Timestamp', kind='line')
ax[2, 0].set_ylabel('Heave [mm]')
ax[2, 0].legend(['Simulated Heave'])
ax[2, 1].legend(['Measured Heave'])

df_source.plot(ax=ax[3, 0], y=['HEAVE_vel'], x='Timestamp', kind='line')
df_log.plot(ax=ax[3, 1], y=['MRU3_Heave_Velocity'], x='Timestamp', kind='line')
ax[3, 0].set_ylabel('Heave velocity [mm/s]')
ax[3, 0].legend(['Simulated Heave Velocity'])
ax[3, 1].legend(['Measured Heave Velocity'])

# PLOT ROLL PITCH AND HEAVE. MRU MEASURED MOTION AND SIMULATION MOTIONS
fig, ax = plt.subplots(1, 1, sharex='col', sharey='row')
df_log.plot(ax=ax, y=['Utilisation_Ratio'], x='Timestamp', kind='line')

# MRU1_Heave_Velocity_unfiltered

plt.show()
