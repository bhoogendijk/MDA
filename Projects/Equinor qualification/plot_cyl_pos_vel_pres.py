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

filenames_output = [] # make empty to open file selection popup

# SECTION 2: SELECT THE PLOTS TO SHOW
save_figures = False  # save  the figures that are plotted NOT CONNECTED
show_figures = True  # show  the figures that are plotted

# SECTION 3: LOADING THE FILES

# load output
pathname = []
for fn in filenames_output:
    pathname.append(os.path.join(initialdiroutput, fn))
df_log = helpers.load(pathname, save_to_feather=True, initialdir=initialdiroutput)
# df_log = helpers.load(save_to_feather=True, initialdir=initialdiroutput)

# CALCULATE ADDITIONAL INFORMATION ABOUT LOADED DATA
# calculate cylinder velocities and duty cycle
df_log['MRU1_Heave'] *= -1  # BM003 uses heave moving down as positive, so we will adjust to our reference frame
df_log['MRU1_Pitch'] *= -1  # BM003 uses roll portside down down as positive, so we will adjust to our reference frame
df_log = helpers.add_derivative_data(df_log)


# # PLOTTING SECTION

# PLOT ROLL PITCH AND HEAVE MOTIONS. MRU MEASURED MOTION AND CIMS CALCULATED PLATFORM MOTION
fig, ax = plt.subplots(3, 1, sharex=True, sharey='row')
# Share the Y axis between the roll and pitch values
# ax[0, 0].get_shared_y_axes().join(ax[0], ax[1, 0])
df_log.plot(ax=ax[0], y=['MRU1_Heave'], x='Timestamp', kind='line')
df_log.plot(ax=ax[0], y=['MRU2_Heave'], x='Timestamp', kind='line')
df_log.plot(ax=ax[0], y=['MRU3_Heave'], x='Timestamp', kind='line')

df_log.plot(ax=ax[1], y=['Cyl1_Pos_CIMS'], x='Timestamp', kind='line')
df_log.plot(ax=ax[1], y=['Cyl2_Pos_CIMS'], x='Timestamp', kind='line')
df_log.plot(ax=ax[1], y=['Cyl3_Pos_CIMS'], x='Timestamp', kind='line')

df_log.plot(ax=ax[2], y=['Active_Control_Loop'], x='Timestamp', kind='line')

# Second figure
fig, ax = plt.subplots(3, 1, sharex=True, sharey='row')
df_log.plot(ax=ax[0], y=['HPU_Press'], x='Timestamp', kind='line')
df_log.plot(ax=ax[0], y=['Cyl1_Pres_Rod'], x='Timestamp', kind='line')
df_log.plot(ax=ax[0], y=['Cyl1_Pres_Bot'], x='Timestamp', kind='line')
df_log.plot(ax=ax[0], y=['Cyl1_Pres_Pas'], x='Timestamp', kind='line')
df_log.plot(ax=ax[0], y=['ActAccu1_Pres'], x='Timestamp', kind='line')


df_log.plot(ax=ax[1], y=['HPU_Press'], x='Timestamp', kind='line')
df_log.plot(ax=ax[1], y=['Cyl2_Pres_Rod'], x='Timestamp', kind='line')
df_log.plot(ax=ax[1], y=['Cyl2_Pres_Bot'], x='Timestamp', kind='line')
df_log.plot(ax=ax[1], y=['Cyl2_Pres_Pas'], x='Timestamp', kind='line')
df_log.plot(ax=ax[1], y=['ActAccu2_Pres'], x='Timestamp', kind='line')

df_log.plot(ax=ax[2], y=['HPU_Press'], x='Timestamp', kind='line')
df_log.plot(ax=ax[2], y=['Cyl3_Pres_Rod'], x='Timestamp', kind='line')
df_log.plot(ax=ax[2], y=['Cyl3_Pres_Bot'], x='Timestamp', kind='line')
df_log.plot(ax=ax[2], y=['Cyl3_Pres_Pas'], x='Timestamp', kind='line')
df_log.plot(ax=ax[2], y=['ActAccu3_Pres'], x='Timestamp', kind='line')

# Third plot
fig, ax = plt.subplots(3, 1, sharex=True, sharey='row')
# Share the Y axis between the roll and pitch values
# ax[0, 0].get_shared_y_axes().join(ax[0], ax[1, 0])
df_log['Cyl1_Pos_Ideal'] = df_log['Cyl1_Pos_Ideal'] +1250
df_log['Cyl2_Pos_Ideal'] = df_log['Cyl2_Pos_Ideal'] +1250
df_log['Cyl3_Pos_Ideal'] = df_log['Cyl3_Pos_Ideal'] +1250

df_log.plot(ax=ax[0], y=['Cyl1_Pos_CIMS'], x='Timestamp', kind='line')
df_log.plot(ax=ax[0], y=['Cyl1_Pos_Ideal'], x='Timestamp', kind='line')

df_log.plot(ax=ax[1], y=['Cyl2_Pos_CIMS'], x='Timestamp', kind='line')
df_log.plot(ax=ax[1], y=['Cyl2_Pos_Ideal'], x='Timestamp', kind='line')

df_log.plot(ax=ax[2], y=['Cyl3_Pos_CIMS'], x='Timestamp', kind='line')
df_log.plot(ax=ax[2], y=['Cyl3_Pos_Ideal'], x='Timestamp', kind='line')

# Fourth plot
fig, ax = plt.subplots(3, 1, sharex=True, sharey='row')
# Share the Y axis between the roll and pitch values
# ax[0, 0].get_shared_y_axes().join(ax[0], ax[1, 0])
df_log['Cyl1_Pos_Ideal'] = df_log['Cyl1_Pos_Ideal'] +1250
df_log['Cyl2_Pos_Ideal'] = df_log['Cyl2_Pos_Ideal'] +1250
df_log['Cyl3_Pos_Ideal'] = df_log['Cyl3_Pos_Ideal'] +1250

df_log.plot(ax=ax[0], y=['Cyl1_Vel_CIMS'], x='Timestamp', kind='line')
# df_log.plot(ax=ax[0], y=['Cyl1_Vel_Ideal'], x='Timestamp', kind='line')

df_log.plot(ax=ax[1], y=['Cyl2_Vel_CIMS'], x='Timestamp', kind='line')
# df_log.plot(ax=ax[1], y=['Cyl2_Vel_Ideal'], x='Timestamp', kind='line')

df_log.plot(ax=ax[2], y=['Cyl3_Vel_CIMS'], x='Timestamp', kind='line')
# df_log.plot(ax=ax[2], y=['Cyl3_Vel_Ideal'], x='Timestamp', kind='line')


#Fifth plot
fig, ax = plt.subplots(3, 1, sharex=True, sharey='row')
# Share the Y axis between the roll and pitch values
# ax[0, 0].get_shared_y_axes().join(ax[0], ax[1, 0])
df_log.plot(ax=ax[0], y=['Heave_Gain_Stroke'], x='Timestamp', kind='line')
df_log.plot(ax=ax[0], y=['Heave_Gain_Speed'], x='Timestamp', kind='line')
df_log.plot(ax=ax[0], y=['Heave_Gain_DC'], x='Timestamp', kind='line')

df_log.plot(ax=ax[1], y=['Utilisation_Ratio'], x='Timestamp', kind='line')

df_log.plot(ax=ax[2], y=['Active_Control_Loop'], x='Timestamp', kind='line')



# show the plots
if show_figures:
    plt.show()


df_log['MRU1_Roll_vel'] = df_log['MRU1_Roll'].diff() / df_log['Timestamp'].diff().dt.total_seconds()
df_log['MRU1_Pitch_vel'] = df_log['MRU1_Pitch'].diff() / df_log['Timestamp'].diff().dt.total_seconds()
df_log['MRU1_Heave_Velocity'] = df_log['MRU1_Heave'].diff() / df_log['Timestamp'].diff().dt.total_seconds()


print(df_log['MRU1_Roll'].std()*3.0/1.9*100)
print(df_log['MRU1_Pitch'].std()*3.0/2.25*100)
print(df_log['MRU1_Heave_Velocity'].std()*3.0/650*100)
