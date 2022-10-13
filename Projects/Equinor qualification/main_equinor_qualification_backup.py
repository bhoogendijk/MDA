import helpers
import plotters
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#import mplcursors
import os

# input datafiles
initialdirinput = 'M:/Projects/281 Equinor - Qualification process Equinor T700/Engineering/Simulations with hostsim/Time traces (input)/OrcaFlex'
initialdirinput = "C:/Users/b.hoogendijk/PycharmProjects/MDA\Projects/Equinor qualification\Simulations with hostsim/Time traces (input)\OrcaFlex"
filename_input = "NORMAND_Tp070_Hs200_Hdg000_Parallel.xlsx"
#filename_input = "NORMAND_Tp110_Hs200_Hdg000_Parallel.xlsx"


# output datafiles
initialdiroutput = 'M:/Projects/281 Equinor - Qualification process Equinor T700/Engineering/Simulations with hostsim/Logging data (output)/dryrun without skids'
initialdiroutput = "C:/Users/b.hoogendijk/PycharmProjects/MDA/Projects/Equinor qualification/Simulations with hostsim/Logging data (output)"

filenames_output = ['BM_AS10_200917T111111_Nokken_Normand_Tp070_Hs200_Parallel.csv',
                    'BM_AS10_200917T101840_Nokken_Normand_Tp070_Hs200_Parallel.csv',
                    'BM_AS10_200917T102611_Nokken_Normand_Tp070_Hs200_Parallel.csv',
                    'BM_AS10_200917T104111_Nokken_Normand_Tp070_Hs200_Parallel.csv',
                    'BM_AS10_200917T105611_Nokken_Normand_Tp070_Hs200_Parallel.csv']

# filenames_output = ['BM_AS10_200917T122611_Nokken_Normand_Tp070_Hs200_Perpendic.csv',
#                     'BM_AS10_200917T112052_Nokken_Normand_Tp070_Hs200_Perpendic.csv',
#                     'BM_AS10_200917T112611_Nokken_Normand_Tp070_Hs200_Perpendic.csv',
#                     'BM_AS10_200917T114111_Nokken_Normand_Tp070_Hs200_Perpendic.csv',
#                     'BM_AS10_200917T115611_Nokken_Normand_Tp070_Hs200_Perpendic.csv',
#                     'BM_AS10_200917T121111_Nokken_Normand_Tp070_Hs200_Perpendic.csv']

#filenames_output = ['BM_AS10_200917T125611_Nokken_Normand_Tp110_Hs200_Parallel.csv',
#                    'BM_AS10_200917T131111_Nokken_Normand_Tp110_Hs200_Parallel.csv',
#                    'BM_AS10_200917T132611_Nokken_Normand_Tp110_Hs200_Parallel.csv',
#                    'BM_AS10_200917T123844_Nokken_Normand_Tp110_Hs200_Parallel.csv',
#                    'BM_AS10_200917T124111_Nokken_Normand_Tp110_Hs200_Parallel.csv']

# filenames_output = ['BM_AS10_200917T141111_Nokken_Normand_Tp110_Hs200_Perpendic.csv',
#                     'BM_AS10_200917T142611_Nokken_Normand_Tp110_Hs200_Perpendic.csv',
#                     'BM_AS10_200917T144111_Nokken_Normand_Tp110_Hs200_Perpendic.csv',
#                     'BM_AS10_200917T134033_Nokken_Normand_Tp110_Hs200_Perpendic.csv',
#                     'BM_AS10_200917T134111_Nokken_Normand_Tp110_Hs200_Perpendic.csv',
#                     'BM_AS10_200917T135611_Nokken_Normand_Tp110_Hs200_Perpendic.csv']

# offset between input and output datafiles
offset_in_seconds = 12.5  # Add seconds if MRU values are to the right of input value.

plot_sync = True  # plot the figure that allows easily to sync
plot_RPH = False  # plot the RPH figure
plot_platform_residual = True  # plot the residual heave figure

plot_orcaflex_MRU1 = True
plot_ideal_pos = False
plot_ideal_vel = True
plot_CIMS_pos = True
plot_CIMS_vel = True
plot_MRU4_vel = True
plot_MRU4_pos = True

plot_roll = False
plot_pitch = False
plot_heave = False
plot_heave_vel = False

save_figures = False  # save  the figures that are plotted
show_figures = True  # show  the figures that are plotted

# code execution
# load output
pathname = []
for fn in filenames_output:
    pathname.append(os.path.join(initialdiroutput, fn))
df_log = helpers.load(pathname, save_to_feather=False, initialdir=initialdiroutput)


# load input
pathname_input = os.path.join(initialdirinput, filename_input)
df_source = pd.read_excel(pathname_input)

# give timestamp to input
timestamps = []
for i in range(df_source.shape[0]):
    timestamp = pd.Timestamp(
        df_log['Timestamp'].values[0] + pd.Timedelta(seconds=df_source['TIME'].values[i] + offset_in_seconds))
    timestamps.append(timestamp)
df_source.insert(0, "Timestamp", timestamps, allow_duplicates=False)
df_source.set_index(df_source['Timestamp'], inplace=True)

# CHANGE THE SOURCE UNITS TO MATCH THE OUTPUT
df_source['HEAVE'] *= 1000  # Source uses meters as input, we will adjust to mm
df_log['MRU1_Heave'] *= -1  # BM003 uses heave moving down as positive, so we will adjust to our reference frame
df_log['MRU1_Pitch'] *= -1  # BM003 uses roll portside down down as positive, so we will adjust to our reference frame

# CALCULATE ADDITIONAL INFORMATION ABOUT LOADED DATA
# calculate cylinder velocities and duty cycle
df_log = helpers.add_derivative_data(df_log)

df_log['Platform_Roll_Ideal'] = np.arctan((1 / 2 * df_log['Cyl1_Pos_Ideal'] + 1 / 2 * df_log['Cyl2_Pos_Ideal'] - df_log[
    'Cyl3_Pos_Ideal']) / 11951.1) * 180 / np.pi  # for 270 degree rotation
df_log['Platform_Pitch_Ideal'] = np.arctan(
    (df_log['Cyl1_Pos_Ideal'] - df_log['Cyl2_Pos_Ideal']) / 13800.0) * 180 / np.pi  # for 270 degree rotation
df_log['Platform_Heave_Ideal'] = (df_log['Cyl1_Pos_Ideal'] + df_log['Cyl2_Pos_Ideal'] + df_log['Cyl3_Pos_Ideal']) / 3

df_log['Platform_Roll_CIMS'] = np.arctan((1 / 2 * df_log['Cyl1_Pos_CIMS'] + 1 / 2 * df_log['Cyl2_Pos_CIMS'] - df_log[
    'Cyl3_Pos_CIMS']) / 11951.1) * 180 / np.pi  # for 270 degree rotation
df_log['Platform_Pitch_CIMS'] = np.arctan(
    (df_log['Cyl1_Pos_CIMS'] - df_log['Cyl2_Pos_CIMS']) / 13800.0) * 180 / np.pi  # for 270 degree rotation
df_log['Platform_Heave_CIMS'] = (df_log['Cyl1_Pos_CIMS'] + df_log['Cyl2_Pos_CIMS'] + df_log['Cyl3_Pos_CIMS']) / 3

df_log['Platform_Roll_MRU4'] = df_log['MRUp_Roll']
df_log['Platform_Pitch_MRU4'] = df_log['MRUp_Pitch']
df_log['Platform_Heave_MRU4'] = df_log['MRUp_Heave']

# adjust heave gain since BM003 software assumes it is only running at 2/3th capacity
df_log['Heave_Gain'] = df_log['Heave_Gain'] * 3 / 2
df_log['Heave_Gain'][df_log['Heave_Gain'] > 1] = 1
df_log['Platform_Heave_Ideal_HG'] = df_log['Platform_Heave_Ideal'] * df_log['Heave_Gain']

df_log['Residual_Roll_Ideal'] = df_log['MRU1_Roll'] + df_log['Platform_Roll_Ideal']
df_log['Residual_Pitch_Ideal'] = df_log['MRU1_Pitch'] + df_log['Platform_Pitch_Ideal']
df_log['Residual_Heave_Ideal'] = df_log['MRU1_Heave'] + df_log['Platform_Heave_Ideal']
df_log['Residual_Heave_Ideal_HG'] = df_log['MRU1_Heave'] + df_log['Platform_Heave_Ideal_HG']

df_log['Residual_Roll_CIMS'] = df_log['MRU1_Roll'] + df_log['Platform_Roll_CIMS']
df_log['Residual_Pitch_CIMS'] = df_log['MRU1_Pitch'] + df_log['Platform_Pitch_CIMS']
df_log['Residual_Heave_CIMS'] = df_log['MRU1_Heave'] + df_log['Platform_Heave_CIMS']

df_log['Residual_Roll_MRU4'] = df_log['MRU1_Roll'] + df_log['Platform_Roll_MRU4']
df_log['Residual_Pitch_MRU4'] = df_log['MRU1_Pitch'] + df_log['Platform_Pitch_MRU4']
df_log['Residual_Heave_MRU4'] = df_log['MRU1_Heave'] + df_log['Platform_Heave_MRU4']

# calculate heave velocity derivatives
df_log['MRU1_Heave_Velocity'] = df_log['MRU1_Heave'].diff() / df_log['Timestamp'].diff().dt.total_seconds()
df_log['Platform_Heave_Ideal_vel'] = df_log['Platform_Heave_Ideal'].diff() / df_log[
    'Timestamp'].diff().dt.total_seconds()

df_log['Platform_Heave_CIMS_vel'] = df_log['Platform_Heave_CIMS'].diff() / df_log['Timestamp'].diff().dt.total_seconds()
df_log['Platform_Heave_MRU4_vel'] = df_log['Platform_Heave_MRU4'].diff() / df_log['Timestamp'].diff().dt.total_seconds()

df_log['Platform_Heave_Ideal_HG_vel'] = df_log['Platform_Heave_Ideal_vel'] * df_log['Heave_Gain']

df_log['Residual_Heave_Ideal_vel'] = df_log['MRU1_Heave_Velocity'] + df_log['Platform_Heave_Ideal_vel']
df_log['Residual_Heave_Ideal_HG_vel'] = df_log['MRU1_Heave_Velocity'] + df_log['Platform_Heave_Ideal_HG_vel']
df_log['Residual_Heave_CIMS_vel'] = df_log['MRU1_Heave_Velocity'] + df_log['Platform_Heave_CIMS_vel']
df_log['Residual_Heave_MRU4_vel'] = df_log['MRU1_Heave_Velocity'] + df_log['Platform_Heave_MRU4_vel']



moving_average=5
df_log['MRU1_Heave_Velocity_filtered'] = df_log['MRU1_Heave_Velocity'].rolling(moving_average).sum()/moving_average
df_log['Platform_Heave_Ideal_vel_filtered'] = df_log['Platform_Heave_Ideal_vel'].rolling(moving_average).sum()/moving_average
df_log['Platform_Heave_Ideal_HG_vel_filtered'] = df_log['Platform_Heave_Ideal_HG_vel'].rolling(moving_average).sum()/moving_average


df_log['Residual_Heave_Ideal_vel_filtered'] = df_log['MRU1_Heave_Velocity_filtered'] + df_log['Platform_Heave_Ideal_vel_filtered']
df_log['Residual_Heave_Ideal_HG_vel_filtered'] = df_log['MRU1_Heave_Velocity_filtered'] + df_log['Platform_Heave_Ideal_HG_vel_filtered']


# PLOTTING SECTION
if plot_RPH:
    figRPH, ax = plt.subplots(3, 2, sharex=True, sharey='row')

    # Share the Y axis between the roll and pitch values
    ax[0, 0].get_shared_y_axes().join(ax[0, 0], ax[1, 0])

    df_log.plot(ax=ax[0, 0], y=['MRU1_Roll'], x='Timestamp', kind='line')
    df_log.plot(ax=ax[0, 0], y=['Ideal_Platform_Roll'], x='Timestamp', kind='line')
    df_source.plot(ax=ax[0, 0], y=['ROLL'], x='Timestamp', kind='line')
    ax[0, 0].set_ylabel('Roll [deg]')

    df_log.plot(ax=ax[1, 0], y=['MRU1_Pitch'], x='Timestamp', kind='line')
    df_log.plot(ax=ax[1, 0], y=['Ideal_Platform_Pitch'], x='Timestamp', kind='line')
    df_source.plot(ax=ax[1, 0], y=['PITCH'], x='Timestamp', kind='line')
    ax[1, 0].set_ylabel('Pitch [deg]')

    df_log.plot(ax=ax[2, 0], y=['MRU1_Heave'], x='Timestamp', kind='line')
    df_log.plot(ax=ax[2, 0], y=['Ideal_Platform_Heave'], x='Timestamp', kind='line')
    df_source.plot(ax=ax[2, 0], y=['HEAVE'], x='Timestamp', kind='line')
    ax[2, 0].set_ylabel('Heave [mm]')

    # limit the heave values to 6 times the standard deviation to prevent unstable heave signal dominating the plot
    std = df_log['MRU1_Heave'].std()
    plt.ylim(-6 * std, 6 * std)

    # TODO: change Cylx_Pos_Ideal to Cylx_Pos_CIMS
    df_log.plot(ax=ax[0, 1], y=['Residual_Roll'], x='Timestamp', kind='line')
    ax[0, 1].set_ylabel('Roll [deg]')

    df_log.plot(ax=ax[1, 1], y=['Residual_Pitch'], x='Timestamp', kind='line')
    ax[1, 1].set_ylabel('Pitch [deg]')

    df_log.plot(ax=ax[2, 1], y=['Residual_Heave'], x='Timestamp', kind='line')
    ax[2, 1].set_ylabel('Heave [mm]')

    if plot_platform_residual:
        figresidual, ax = plt.subplots(2, 2, sharex=True, sharey='row')

    df_log.plot(ax=ax[0, 0], y=['MRU1_Heave_Velocity'], x='Timestamp', kind='line')
    df_log.plot(ax=ax[1, 0], y=['Ideal_Platform_Heave_Velocity'], x='Timestamp', kind='line')
    df_log.plot(ax=ax[0, 1], y=['Platform_Heave_Velocity_Inc_Heave_Gain'], x='Timestamp', kind='line')
    df_log.plot(ax=ax[1, 1], y=['Platform_Residual_Heave_Velocity_Inc_Heave_Gain'], x='Timestamp', kind='line')
    ax[0, 0].set_ylabel('Heave [mm]')

if plot_sync:
    figRPH, ax = plt.subplots(1, 1)
    df_log.plot(ax=ax, y=['MRU1_Heave'], x='Timestamp', kind='line')
    df_source.plot(ax=ax, y=['HEAVE'], x='Timestamp', kind='line')

if plot_orcaflex_MRU1:
    fig1, ax = plt.subplots(3, 1, sharex=True, sharey='row')
    # Share the Y axis between the roll and pitch values
    ax[0].get_shared_y_axes().join(ax[0], ax[1])

    df_log.plot(ax=ax[0], y=['MRU1_Roll'], x='Timestamp', kind='line')
    df_source.plot(ax=ax[0], y=['ROLL'], x='Timestamp', kind='line')
    ax[0].set_ylabel('Roll [deg]')

    df_log.plot(ax=ax[1], y=['MRU1_Pitch'], x='Timestamp', kind='line')
    df_source.plot(ax=ax[1], y=['PITCH'], x='Timestamp', kind='line')
    ax[1].set_ylabel('Pitch [deg]')

    df_log.plot(ax=ax[2], y=['MRU1_Heave'], x='Timestamp', kind='line')
    df_source.plot(ax=ax[2], y=['HEAVE'], x='Timestamp', kind='line')
    ax[2].set_ylabel('Heave [mm]')

if plot_ideal_pos:
    fig2, ax = plt.subplots(3, 2, sharex=True, sharey='row')
    # Share the Y axis between the roll and pitch values
    ax[0, 0].get_shared_y_axes().join(ax[0, 0], ax[1, 0])

    df_log.plot(ax=ax[0, 0], y=['MRU1_Roll'], x='Timestamp', kind='line')
    df_log.plot(ax=ax[0, 0], y=['Platform_Roll_Ideal'], x='Timestamp', kind='line')
    ax[0, 0].set_ylabel('Roll [deg]')

    df_log.plot(ax=ax[1, 0], y=['MRU1_Pitch'], x='Timestamp', kind='line')
    df_log.plot(ax=ax[1, 0], y=['Platform_Pitch_Ideal'], x='Timestamp', kind='line')
    ax[1, 0].set_ylabel('Pitch [deg]')

    df_log.plot(ax=ax[2, 0], y=['MRU1_Heave'], x='Timestamp', kind='line')
    df_log.plot(ax=ax[2, 0], y=['Platform_Heave_Ideal'], x='Timestamp', kind='line')
    df_log.plot(ax=ax[2, 0], y=['Platform_Heave_Ideal_HG'], x='Timestamp', kind='line')
    ax[2, 0].set_ylabel('Heave [mm]')

    df_log.plot(ax=ax[0, 1], y=['Residual_Roll_Ideal'], x='Timestamp', kind='line')
    ax[0, 1].set_ylabel('Roll [deg]')

    df_log.plot(ax=ax[1, 1], y=['Residual_Pitch_Ideal'], x='Timestamp', kind='line')
    ax[1, 1].set_ylabel('Pitch [deg]')

    df_log.plot(ax=ax[2, 1], y=['Residual_Heave_Ideal'], x='Timestamp', kind='line')
    df_log.plot(ax=ax[2, 1], y=['Residual_Heave_Ideal_HG'], x='Timestamp', kind='line')
    ax[2, 1].set_ylabel('Heave [mm]')

    if plot_platform_residual:
        figresidual, ax = plt.subplots(2, 2, sharex=True, sharey='row')

    df_log.plot(ax=ax[0, 0], y=['MRU1_Heave_Velocity'], x='Timestamp', kind='line')
    df_log.plot(ax=ax[1, 0], y=['Platform_Heave_Ideal_vel'], x='Timestamp', kind='line')
    df_log.plot(ax=ax[0, 1], y=['Platform_Heave_Velocity_Inc_Heave_Gain'], x='Timestamp', kind='line')
    df_log.plot(ax=ax[1, 1], y=['Platform_Residual_Heave_Velocity_Inc_Heave_Gain'], x='Timestamp', kind='line')
    ax[0, 0].set_ylabel('Heave [mm]')

if plot_heave:
    fig_heave, ax = plt.subplots(3, 2, sharex=True, sharey='col')
    # Share the Y axis between the roll and pitch values
    ax[0, 0].get_shared_y_axes().join(ax[0, 0], ax[1, 0])

    df_log.plot(ax=ax[0, 0], y=['MRU1_Heave'], x='Timestamp', kind='line')
    df_log.plot(ax=ax[0, 0], y=['Platform_Heave_Ideal'], x='Timestamp', kind='line')
    df_log.plot(ax=ax[0, 0], y=['Platform_Heave_Ideal_HG'], x='Timestamp', kind='line')
    ax[0, 0].set_ylabel('Heave [mm]')

    df_log.plot(ax=ax[1, 0], y=['MRU1_Heave'], x='Timestamp', kind='line')
    df_log.plot(ax=ax[1, 0], y=['Platform_Heave_CIMS'], x='Timestamp', kind='line')
    ax[1, 0].set_ylabel('Heave [mm]')

    df_log.plot(ax=ax[2, 0], y=['MRU1_Heave'], x='Timestamp', kind='line')
    df_log.plot(ax=ax[2, 0], y=['Platform_Heave_MRU4'], x='Timestamp', kind='line')
    ax[2, 0].set_ylabel('Heave [mm]')

    df_log.plot(ax=ax[0, 1], y=['Residual_Heave_Ideal'], x='Timestamp', kind='line')
    df_log.plot(ax=ax[0, 1], y=['Residual_Heave_Ideal_HG'], x='Timestamp', kind='line')
    ax[0, 1].set_ylabel('Heave [mm]')

    df_log.plot(ax=ax[1, 1], y=['Residual_Heave_CIMS'], x='Timestamp', kind='line')
    ax[1, 1].set_ylabel('Heave [mm]')

    df_log.plot(ax=ax[2, 1], y=['Residual_Heave_MRU4'], x='Timestamp', kind='line')
    ax[2, 1].set_ylabel('Heave [mm]')

if plot_heave_vel:
    fig_heave_vel, ax = plt.subplots(3, 2, sharex=True)
    # Share the Y axis between the roll and pitch values
    # ax[0, 0].get_shared_y_axes().join(ax[0, 0], ax[1, 0])

    df_log.plot(ax=ax[0, 0], y=['MRU1_Heave_Velocity'], x='Timestamp', kind='line')
    df_log.plot(ax=ax[0, 0], y=['Platform_Heave_Ideal_vel'], x='Timestamp', kind='line')
    df_log.plot(ax=ax[0, 0], y=['Platform_Heave_Ideal_HG_vel'], x='Timestamp', kind='line')
    ax[0, 0].set_ylabel('Heave Velocity [mm/s]')

    df_log.plot(ax=ax[1, 0], y=['MRU1_Heave_Velocity_filtered'], x='Timestamp', kind='line')
    df_log.plot(ax=ax[1, 0], y=['Platform_Heave_Ideal_vel_filtered'], x='Timestamp', kind='line')
    df_log.plot(ax=ax[1, 0], y=['Platform_Heave_Ideal_HG_vel_filtered'], x='Timestamp', kind='line')
    ax[1, 0].set_ylabel('Heave Velocity [mm/s]')

    # df_log.plot(ax=ax[1, 0], y=['MRU1_Heave_Velocity'], x='Timestamp', kind='line')
    # df_log.plot(ax=ax[1, 0], y=['Platform_Heave_CIMS_vel'], x='Timestamp', kind='line')
    # ax[1, 0].set_ylabel('Heave Velocity [mm/s]')

    df_log.plot(ax=ax[2, 0], y=['MRU1_Heave_Velocity'], x='Timestamp', kind='line')
    df_log.plot(ax=ax[2, 0], y=['Platform_Heave_MRU4_vel'], x='Timestamp', kind='line')
    ax[2, 0].set_ylabel('Heave Velocity [mm/s]')

    df_log.plot(ax=ax[0, 1], y=['Residual_Heave_Ideal_vel'], x='Timestamp', kind='line')
    df_log.plot(ax=ax[0, 1], y=['Residual_Heave_Ideal_HG_vel'], x='Timestamp', kind='line')
    ax[0, 1].set_ylabel('Heave Velocity [mm/s]')
    ax[0, 1].axhline(356)
    ax[0, 1].axhline(-356)


    df_log.plot(ax=ax[1, 1], y=['Residual_Heave_Ideal_vel_filtered'], x='Timestamp', kind='line')
    df_log.plot(ax=ax[1, 1], y=['Residual_Heave_Ideal_HG_vel_filtered'], x='Timestamp', kind='line')
    ax[1, 1].set_ylabel('Heave Velocity [mm/s]')
    ax[1, 1].axhline(356)
    ax[1, 1].axhline(-356)

    # df_log.plot(ax=ax[1, 1], y=['Residual_Heave_CIMS_vel'], x='Timestamp', kind='line')
    # ax[1, 1].set_ylabel('Heave Velocity [mm/s]')
    # ax[1, 1].axhline(356)
    # ax[1, 1].axhline(-356)

    df_log.plot(ax=ax[2, 1], y=['Residual_Heave_MRU4_vel'], x='Timestamp', kind='line')
    ax[2, 1].set_ylabel('Heave Velocity [mm/s]')
    ax[2, 1].axhline(356)
    ax[2, 1].axhline(-356)


fig,ax = plotters.plot_easy(df_log,[[['MRU1_Heave','Platform_Heave_Ideal_HG'],                                 ['Residual_Heave_Ideal_HG']],
                                    [['MRU1_Heave_Velocity_filtered','Platform_Heave_Ideal_vel_filtered'],     ['Residual_Heave_Ideal_HG_vel_filtered']]],

                                    [['Heave [mm]',                                                            ''], 
                                     ['Heave velocity [mm/s]',                                                 '']],
                                    
                                    sharex=True, sharey='row')
ax[1,1].axhline(356,color='red',ls='--')
ax[1,1].axhline(-356,color='red',ls='--')



# show the plots
if show_figures: plt.show()

# clear memory and close the figures
if plot_RPH: figRPH.clf()
if plot_platform_residual: figresidual.clf()

if plot_orcaflex_MRU1: fig1.clf()
