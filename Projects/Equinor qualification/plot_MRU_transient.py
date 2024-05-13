import helpers
import matplotlib.pyplot as plt
import os

# This script is setup to make the plots with the data that was collected in Rotterdam Port while playing the motion
# files for the Equinor TRL5 qualification on 27-09-2022. Four files were played, a selector is created to select which
# one is plotted.

# SECTION 1: SELECTING WHICH FILES TO LOAD

# output datafiles
initialdiroutput = "C:\\Users\\b.hoogendijk\\Desktop\\BM folder copies\\281 Equinor - Qualification process Equinor T700\\Engineering\\Simulations with hostsim\\autosave\\"

filenames_output = ['BM_AS10_221003T192519_Test_internal_nofilter_na.csv',
                    'BM_AS10_221003T194019_Test_internal_nofilter_na.csv']

filenames_output = []  # make empty to open file selection popup

# SECTION 2: SELECT THE PLOTS TO SHOW
save_figures = False  # save  the figures that are plotted NOT CONNECTED
show_figures = True  # show  the figures that are plotted

rotation = 270

# SECTION 3: LOADING THE FILES
# load output
pathname = []
for fn in filenames_output:
    pathname.append(os.path.join(initialdiroutput, fn))
df_log = helpers.load(pathname, save_to_feather=True, initialdir=initialdiroutput)
# df_log = helpers.load(save_to_feather=True, initialdir=initialdiroutput)

# CALCULATE ADDITIONAL INFORMATION ABOUT LOADED DATA
# calculate cylinder velocities and duty cycle
df_log = helpers.add_derivative_data(df_log, rotation=rotation)

df_log['Platform_Heave_MRU4'] *= -1

# # PLOTTING SECTION

# FIGURE 01; PLOT ROLL PITCH AND HEAVE MOTIONS. MRU MEASURED MOTION AND CIMS CALCULATED PLATFORM MOTION
fig, ax = plt.subplots()
df_log.plot(ax=ax, y=['MRU1_Heave'], x='Timestamp', kind='line')
df_log.plot(ax=ax, y=['MRU2_Heave'], x='Timestamp', kind='line')
df_log.plot(ax=ax, y=['MRU3_Heave'], x='Timestamp', kind='line')
df_log.plot(ax=ax, y=['Platform_Heave_MRU4'], x='Timestamp', kind='line')
ax.set_ylabel('Heave [mm]')
ax.legend(['Heave MRU 1 (24042)', 'Heave MRU 2 (22855)', 'Heave MRU 3 (24043)', 'Heave MRU 4 (24036)'])


# show the plots
if show_figures:
    plt.show()
