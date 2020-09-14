import helpers, plotters
import matplotlib.pyplot as plt
from dateutil import parser
import numpy as np
import pandas as pd
import mplcursors
from tkinter import *
from tkinter import filedialog
import os

initialdiroutput = '../data/Hostsim/Logging data (output)/'  # data folder in which the data is searched for. default is '../data/'
initialdirinput = '../data/Hostsim/Time traces (input)/OrcaFlex time traces/'

plot_UR = False  # plot the UR figure
plot_RPH = True  # plot the RPH figure
plot_histogram = False  # plot the heave gain histogram figure
plot_heave_gain_roll = False
plot_power_consumption = True

save_figures = False  # save  the figures that are plotted
show_figures = True  # show  the figures that are plotted

# code execution

# LOAD THE LOGGING DATA (OUTPUT)
run_counter = 0
filenames_output = ["BM_AS10_200812T153942_Nokken_Hs2_7s_Perp_3sigma_nofilter.csv", "BM_AS10_200812T151056_Nokken_Hs2_7s_Perp_3sigma_nofilter.csv", "BM_AS10_200812T152442_Nokken_Hs2_7s_Perp_3sigma_nofilter.csv"]
pathname=[]
for fn in filenames_output:
    pathname.append(os.path.join(initialdiroutput, fn))


df_log = helpers.load(pathname, save_to_feather=False, initialdir=initialdiroutput)

# LOAD THE SOURCE DATA (INPUT)
# filename = filedialog.askopenfilename(initialdir=initialdirinput,
#                                       title="Select data files",
#                                       filetypes=(("xlsx files", "*.xlsx"), ("all files", "*.*")))

filename_input = "NORMAND_Tp070_Hs200_Hdg000_Perpendicular.xlsx"
pathname_input = os.path.join(initialdirinput, filename_input)

df_source = pd.read_excel(pathname_input)
timestamps = []
for i in range(df_source.shape[0]):
    timestamp = pd.Timestamp(df_log['Timestamp'].values[0] + pd.Timedelta(seconds=df_source['TIME'].values[i]+15.6))
    timestamps.append(timestamp)

df_source.insert(0, "Timestamp", timestamps, allow_duplicates=False)

# df_source['TIME'] = df_log['Timestamp'].values[0] + pd.Timedelta(seconds=df_source['TIME'].values)

df_source.set_index(df_source['Timestamp'], inplace=True)


# CHANGE THE SOURCE TO MATCH THE OUTPUT
factor = 1
df_source['HEAVE'] *= -1000 * factor
df_source['ROLL'] *= -1 * factor
df_source['PITCH'] *= 1 * factor

# CALCULATE ADDITIONAL INFORMATION ABOUT LOADED DATA

# calculate cylinder velocities and duty cycle
df_log = helpers.add_derivative_data(df_log)

df = pd.concat([df_source, df_log])

df = df.sort_values(['Timestamp'], ascending=[True])  # sorting values

# PLOTTING SECTION

if plot_RPH:
    fig, ax = plt.subplots(3, 2, sharex=True, sharey='row')

    # Share the Y axis between the roll and pitch values
    ax[0, 0].get_shared_y_axes().join(ax[0, 0], ax[1, 0])

    df_log.plot(ax=ax[0, 0], y=['MRU1_Roll'], x='Timestamp', kind='line')
    df_source.plot(ax=ax[0, 0], y=['ROLL'], x='Timestamp', kind='line')
    ax[0, 0].set_ylabel('Roll [deg]')

    df_log.plot(ax=ax[1, 0], y=['MRU1_Pitch'], x='Timestamp', kind='line')
    df_source.plot(ax=ax[1, 0], y=['PITCH'], x='Timestamp', kind='line')
    ax[1, 0].set_ylabel('Pitch [deg]')

    df_log.plot(ax=ax[2, 0], y=['MRU1_Heave'], x='Timestamp', kind='line')
    df_source.plot(ax=ax[2, 0], y=['HEAVE'], x='Timestamp', kind='line')
    ax[2, 0].set_ylabel('Heave [mm]')

    # limit the heave values to 6 times the standard deviation to prevent unstable heave signal dominating the plot
    std = df['MRU1_Heave'].std()
    plt.ylim(-6 * std, 6 * std)
    mplcursors.cursor()

# show the plots
if show_figures: plt.show()

# clear memory and close the figures
if plot_RPH: figRPH.clf()
