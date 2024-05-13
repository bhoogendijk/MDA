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

# # PLOTTING SECTION

# FIGURE 01; PLOT ROLL PITCH AND HEAVE MOTIONS. MRU MEASURED MOTION AND CIMS CALCULATED PLATFORM MOTION
fig, ax = plt.subplots(3, 1, sharex=True, sharey='row')
df_log.plot(ax=ax[0], y=['MRU1_Heave'], x='Timestamp', kind='line')
df_log.plot(ax=ax[0], y=['MRU2_Heave'], x='Timestamp', kind='line')
df_log.plot(ax=ax[0], y=['MRU3_Heave'], x='Timestamp', kind='line')
df_log.plot(ax=ax[1], y=['Cyl1_Pos_CIMS'], x='Timestamp', kind='line')
df_log.plot(ax=ax[1], y=['Cyl2_Pos_CIMS'], x='Timestamp', kind='line')
df_log.plot(ax=ax[1], y=['Cyl3_Pos_CIMS'], x='Timestamp', kind='line')
df_log.plot(ax=ax[2], y=['Active_Control_Loop'], x='Timestamp', kind='line')

# FIGURE 02; Cylinder pressures
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
ax[0].set_ylabel('Pressure [bar]')
ax[1].set_ylabel('Pressure [bar]')
ax[2].set_ylabel('Pressure [bar]')

# FIGURE 03; Compare ideal cylinder position and actual cylinder position (CIMS)
fig, ax = plt.subplots(3, 1, sharex=True, sharey='row')
df_log['Cyl1_Pos_Ideal'] = df_log['Cyl1_Pos_Ideal'] + 1250
df_log['Cyl2_Pos_Ideal'] = df_log['Cyl2_Pos_Ideal'] + 1250
df_log['Cyl3_Pos_Ideal'] = df_log['Cyl3_Pos_Ideal'] + 1250
df_log.plot(ax=ax[0], y=['Cyl1_Pos_CIMS'], x='Timestamp', kind='line')
df_log.plot(ax=ax[0], y=['Cyl1_Pos_Ideal'], x='Timestamp', kind='line')
df_log.plot(ax=ax[1], y=['Cyl2_Pos_CIMS'], x='Timestamp', kind='line')
df_log.plot(ax=ax[1], y=['Cyl2_Pos_Ideal'], x='Timestamp', kind='line')
df_log.plot(ax=ax[2], y=['Cyl3_Pos_CIMS'], x='Timestamp', kind='line')
df_log.plot(ax=ax[2], y=['Cyl3_Pos_Ideal'], x='Timestamp', kind='line')

# FIGURE 04; CIMS  cylinder velocities
fig, ax = plt.subplots(3, 1, sharex=True, sharey='row')
# df_log['Cyl1_Pos_Ideal'] = df_log['Cyl1_Pos_Ideal'] + 1250
# df_log['Cyl2_Pos_Ideal'] = df_log['Cyl2_Pos_Ideal'] + 1250
# df_log['Cyl3_Pos_Ideal'] = df_log['Cyl3_Pos_Ideal'] + 1250
df_log.plot(ax=ax[0], y=['Cyl1_Vel_CIMS'], x='Timestamp', kind='line')
df_log.plot(ax=ax[1], y=['Cyl2_Vel_CIMS'], x='Timestamp', kind='line')
df_log.plot(ax=ax[2], y=['Cyl3_Vel_CIMS'], x='Timestamp', kind='line')

# FIGURE 05; heave gains
fig, ax = plt.subplots(3, 1, sharex=True, sharey='row')
df_log.plot(ax=ax[0], y=['Heave_Gain_Stroke'], x='Timestamp', kind='line')
df_log.plot(ax=ax[0], y=['Heave_Gain_Speed'], x='Timestamp', kind='line')
df_log.plot(ax=ax[0], y=['Heave_Gain_DC'], x='Timestamp', kind='line')
df_log.plot(ax=ax[1], y=['Utilisation_Ratio'], x='Timestamp', kind='line')
df_log.plot(ax=ax[2], y=['Active_Control_Loop'], x='Timestamp', kind='line')

# FIGURE 06;  PLOT ROLL PITCH AND HEAVE MOTIONS CIMS CALCULATED PLATFORM MOTION AND THE RESIDUALS
figRPH, ax = plt.subplots(3, 2, sharex=True, sharey='row')
ax[0, 0].get_shared_y_axes().join(ax[0, 0], ax[1, 0]) # Share the Y axis between the roll and pitch values
df_log.plot(ax=ax[0, 0], y=['MRU1_Roll'], x='Timestamp', kind='line')
df_log.plot(ax=ax[0, 0], y=['Platform_Roll_CIMS'], x='Timestamp', kind='line')
ax[0, 0].set_ylabel('Roll [deg]')
ax[0, 0].legend(['Vessel Roll Amplitude', 'Platform Roll Amplitude'])
df_log.plot(ax=ax[1, 0], y=['MRU1_Pitch'], x='Timestamp', kind='line')
df_log.plot(ax=ax[1, 0], y=['Platform_Pitch_CIMS'], x='Timestamp', kind='line')
ax[1, 0].set_ylabel('Pitch [deg]')
ax[1, 0].legend(['Vessel Pitch Amplitude', 'Platform Pitch Amplitude'])
df_log.plot(ax=ax[2, 0], y=['MRU1_Heave'], x='Timestamp', kind='line')
df_log.plot(ax=ax[2, 0], y=['Platform_Heave_CIMS'], x='Timestamp', kind='line')
ax[2, 0].set_ylabel('Heave [mm]')
ax[2, 0].legend(['Vessel Heave Amplitude', 'Platform Heave Amplitude'])
df_log.plot(ax=ax[0, 1], y=['Residual_Roll_CIMS'], x='Timestamp', kind='line')
ax[0, 1].set_ylabel('Roll [deg]')
ax[0, 1].legend(['Residual Roll Amplitude'])
df_log.plot(ax=ax[1, 1], y=['Residual_Pitch_CIMS'], x='Timestamp', kind='line')
ax[1, 1].set_ylabel('Pitch [deg]')
ax[1, 1].legend(['Residual Pitch Amplitude'])
df_log.plot(ax=ax[2, 1], y=['Residual_Heave_CIMS'], x='Timestamp', kind='line')
ax[2, 1].set_ylabel('Heave [mm]')
ax[2, 1].legend(['Residual Heave Amplitude'])

# FIGURE 07; PLOT ROLL PITCH AND HEAVE VELOCITIES. MRU MEASURED MOTION AND CIMS CALCULATED PLATFORM MOTION
figRPHvel, ax = plt.subplots(3, 2, sharex=True, sharey='row')
ax[0, 0].get_shared_y_axes().join(ax[0, 0], ax[1, 0]) # Share the Y axis between the roll and pitch values
df_log.plot(ax=ax[0, 0], y=['MRU1_Roll_vel'], x='Timestamp', kind='line')
df_log.plot(ax=ax[0, 0], y=['Platform_Roll_CIMS_vel'], x='Timestamp', kind='line')
ax[0, 0].set_ylabel('Roll Velocity [deg/s]')
ax[0, 0].legend(['Vessel Roll Velocity', 'Platform Roll Velocity'])
df_log.plot(ax=ax[1, 0], y=['MRU1_Pitch_vel'], x='Timestamp', kind='line')
df_log.plot(ax=ax[1, 0], y=['Platform_Pitch_CIMS_vel'], x='Timestamp', kind='line')
ax[1, 0].set_ylabel('Pitch Velocity [deg/s]')
ax[1, 0].legend(['Vessel Pitch Velocity', 'Platform Pitch Velocity'])
df_log.plot(ax=ax[2, 0], y=['MRU1_Heave_Velocity'], x='Timestamp', kind='line')
df_log.plot(ax=ax[2, 0], y=['Platform_Heave_CIMS_vel'], x='Timestamp', kind='line')
ax[2, 0].set_ylabel('Heave Velocity [mm/s]')
ax[2, 0].legend(['Vessel Heave Velocity', 'Platform Heave Velocity'])
df_log.plot(ax=ax[0, 1], y=['Residual_Roll_CIMS_vel'], x='Timestamp', kind='line')
ax[0, 1].set_ylabel('Roll Velocity [deg/s]')
ax[0, 1].legend(['Residual Roll Velocity'])
df_log.plot(ax=ax[1, 1], y=['Residual_Pitch_CIMS_vel'], x='Timestamp', kind='line')
ax[1, 1].set_ylabel('Pitch Velocity [deg/s]')
ax[1, 1].legend(['Residual Pitch Velocity'])
df_log.plot(ax=ax[2, 1], y=['Residual_Heave_CIMS_vel'], x='Timestamp', kind='line')
ax[2, 1].axhline(356, color='k')
ax[2, 1].axhline(-356, color='k')
ax[2, 1].set_ylabel('Heave Velocity [mm]')
ax[2, 1].legend(['Residual Heave Velocity'])

# FIGURE 08; PLOT HEAVE VELOCITIES. MRU MEASURED MOTION AND CIMS CALCULATED PLATFORM MOTION
figRPHvel, ax = plt.subplots(2, 1, sharex=True, sharey='row')
df_log.plot(ax=ax[0], y=['Residual_Heave_CIMS_vel'], x='Timestamp', kind='line')
ax[0].axhline(356, color='k')
ax[0].axhline(-356, color='k')
ax[0].set_ylabel('Heave Velocity [mm/s]')
ax[0].legend(['Residual Heave Velocity (CIMS)'])
df_log.plot(ax=ax[1], y=['Utilisation_Ratio'], x='Timestamp', kind='line')
ax[1].set_ylabel('Utilisation ratio [-]')

# FIGURE 09; PLOT HEAVE VELOCITIES. MRU MEASURED MOTION AND CIMS CALCULATED PLATFORM MOTION
figRPHvel, ax = plt.subplots(2, 1, sharex=True, sharey='row')
df_log.plot(ax=ax[0], y=['Platform_Heave_MRU4_vel'], x='Timestamp', kind='line')
ax[0].axhline(356, color='k')
ax[0].axhline(-356, color='k')
ax[0].set_ylabel('Heave Velocity [mm/s]')
ax[0].legend(['Residual Heave Velocity (MRU)'])
df_log.plot(ax=ax[1], y=['Utilisation_Ratio'], x='Timestamp', kind='line')
ax[1].set_ylabel('Utilisation ratio [-]')
# TODO: use the reel velocity instead of platform center velocity

# FIGURE 10; PLOT HEAVE VELOCITIES. MRU MEASURED MOTION AND CIMS CALCULATED PLATFORM MOTION
figHvel, ax = plt.subplots(2, 1, sharex=True, sharey='row')
df_log.plot(ax=ax[0], y=['Residual_Heave_Ideal_vel'], x='Timestamp', kind='line')
ax[0].axhline(356, color='k')
ax[0].axhline(-356, color='k')
ax[0].set_ylabel('Heave Velocity [mm/s]')
ax[0].legend(['Residual Heave Velocity (Ideal)'])
df_log.plot(ax=ax[1], y=['Utilisation_Ratio'], x='Timestamp', kind='line')
ax[1].set_ylabel('Utilisation ratio [-]')

# show the plots
if show_figures:
    plt.show()

print(df_log['MRU1_Heave_Velocity'].std() * 3.3 / 796 * 100)
print(df_log['Utilisation_Ratio'].mean())
