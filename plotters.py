import matplotlib.pyplot as plt
import numpy as np
from itertools import chain

def UR_criteria(df, share_x_axes_with=False):
    fig, ax = plt.subplots(3, 2, sharex=True)

    if share_x_axes_with:
        ax.get_shared_x_axes().join(ax, share_x_axes_with)

    # Duty cycle
    df.plot(ax=ax[0, 0], y='Duty_Cycle', x='Timestamp', kind='line')
    ax[0, 0].set_ylabel('Cylinders abs vel. sum[mm/s]')
    dl = ax[0, 0].axhline(1260, color='black', ls='--')
    dl.set_label('Duty cycle limit')
    ax[0, 0].legend(loc='best')

    # Cylinder position
    df.plot(ax=ax[1, 0], y=['Cyl1_Pos_Ideal', 'Cyl2_Pos_Ideal', 'Cyl3_Pos_Ideal'], x='Timestamp',
            kind='line')
    ax[1, 0].set_ylabel('Cylinder pos. [mm]')
    dl = ax[1, 0].axhline(1100, color='black', ls='--')
    ax[1, 0].axhline(-1100, color='black', ls='--')
    dl.set_label('Position limit')
    ax[1, 0].legend(loc='best')

    # Cylinder velocity
    df.plot(ax=ax[2, 0], y=['Cyl1_Vel_Ideal', 'Cyl2_Vel_Ideal', 'Cyl3_Vel_Ideal'], x='Timestamp', kind='line')
    ax[2, 0].set_ylabel('Cylinder vel. [mm/s]')
    dl = ax[2, 0].axhline(736, color='black', ls='--')
    ax[2, 0].axhline(-736, color='black', ls='--')
    dl.set_label('Velocity limit')
    ax[2, 0].legend(loc='best')

    # system mode
    df.plot(ax=ax[0, 1], y='System_Mode', x='Timestamp', kind='line')
    ax[0, 1].set_ylabel('mode [-]')

    # UR
    df.plot(ax=ax[1, 1], y='Utilisation_Ratio', x='Timestamp', kind='line')
    ax[1, 1].set_ylabel('UR [%]')

    # HeaveGain
    df.plot(ax=ax[2, 1], y=['Heave_Gain_DC', 'Heave_Gain_Stroke', 'Heave_Gain_Speed'], x='Timestamp',
            kind='line')
    ax[2, 1].set_ylabel('gain [-]')

    return fig, ax


def RPH(df, share_x_axes_with=False):
    fig, ax = plt.subplots(3, 2, sharex=True, sharey='row')

    # Share the X axis with another plot
    if share_x_axes_with is not False:
        share_x_axes_with[0, 0].get_shared_x_axes().join(share_x_axes_with[0, 0], ax[0, 0])

    # Share the Y axis between the roll and pitch values
    ax[0, 0].get_shared_y_axes().join(ax[0, 0], ax[1, 0])

    df.plot(ax=ax[0, 0], y=['MRU1_Roll', 'MRU2_Roll', 'MRU3_Roll'], x='Timestamp', kind='line')
    df.plot(ax=ax[0, 1], y=['MRUp_Roll'], x='Timestamp', kind='line')
    ax[0, 0].set_ylabel('Roll [deg]')

    df.plot(ax=ax[1, 0], y=['MRU1_Pitch', 'MRU2_Pitch', 'MRU3_Pitch'], x='Timestamp', kind='line')
    df.plot(ax=ax[1, 1], y=['MRUp_Pitch'], x='Timestamp', kind='line')
    ax[1, 0].set_ylabel('Pitch [deg]')

    df.plot(ax=ax[2, 0], y=['MRU1_Heave', 'MRU2_Heave', 'MRU3_Heave'], x='Timestamp', kind='line')
    df.plot(ax=ax[2, 1], y=['MRUp_Heave'], x='Timestamp', kind='line')
    ax[2, 0].set_ylabel('Heave [mm]')

    # limit the heave values to 6 times the standard deviation to prevent unstable heave signal dominating the plot
    std = df['MRU1_Heave'].std()
    plt.ylim(-6 * std, 6 * std)
    return fig, ax

def heave_gain_roll(df, share_x_axes_with=False):
    fig, ax = plt.subplots(3, 2, sharex=True)

    if share_x_axes_with:
        ax.get_shared_x_axes().join(ax, share_x_axes_with)

    # Duty cycle
    df.plot(ax=ax[0, 0], y='Duty_Cycle', x='Timestamp', kind='line')
    ax[0, 0].set_ylabel('Cylinders abs vel. sum[mm/s]')
    dl = ax[0, 0].axhline(1260, color='black', ls='--')
    dl.set_label('Duty cycle limit')
    ax[0, 0].legend(loc='best')

    # Cylinder position
    df.plot(ax=ax[1, 0], y=['Cyl1_Pos_Ideal', 'Cyl2_Pos_Ideal', 'Cyl3_Pos_Ideal'], x='Timestamp',
            kind='line')
    ax[1, 0].set_ylabel('Cylinder pos. [mm]')
    dl = ax[1, 0].axhline(1100, color='black', ls='--')
    ax[1, 0].axhline(-1100, color='black', ls='--')
    dl.set_label('Position limit')
    ax[1, 0].legend(loc='best')

    # Cylinder velocity
    df.plot(ax=ax[2, 0], y=['Cyl1_Vel_Ideal', 'Cyl2_Vel_Ideal', 'Cyl3_Vel_Ideal'], x='Timestamp', kind='line')
    ax[2, 0].set_ylabel('Cylinder vel. [mm/s]')
    dl = ax[2, 0].axhline(736, color='black', ls='--')
    ax[2, 0].axhline(-736, color='black', ls='--')
    dl.set_label('Velocity limit')
    ax[2, 0].legend(loc='best')

    # UR
    df.plot(ax=ax[0, 1], y='Utilisation_Ratio', x='Timestamp', kind='line')
    ax[0, 1].set_ylabel('UR [%]')

    df.plot(ax=ax[1, 1], y=['MRU1_Roll', 'MRU2_Roll', 'MRU3_Roll'], x='Timestamp', kind='line')
    ax[1, 1].set_ylabel('Roll [deg]')

    # HeaveGain
    df.plot(ax=ax[2, 1], y=['Heave_Gain_DC', 'Heave_Gain_Stroke', 'Heave_Gain_Speed'], x='Timestamp',
            kind='line')
    ax[2, 1].set_ylabel('gain [-]')

    return fig, ax

def heave_gain(df, share_x_axes_with=False):
    fig, ax = plt.subplots(4, 2, sharex=True)

    if share_x_axes_with:
        ax.get_shared_x_axes().join(ax, share_x_axes_with)

    # Duty cycle
    df.plot(ax=ax[0, 0], y='Duty_Cycle', x='Timestamp', kind='line')
    ax[0, 0].set_ylabel('Cylinders abs vel. sum[mm/s]')
    dl = ax[0, 0].axhline(1260, color='black', ls='--')
    dl.set_label('Duty cycle limit')
    ax[0, 0].legend(loc='best')

    # Cylinder position
    df.plot(ax=ax[1, 0], y=['Cyl1_Pos_Ideal', 'Cyl2_Pos_Ideal', 'Cyl3_Pos_Ideal'], x='Timestamp',
            kind='line')
    ax[1, 0].set_ylabel('Cylinder pos. [mm]')
    dl = ax[1, 0].axhline(1100, color='black', ls='--')
    ax[1, 0].axhline(-1100, color='black', ls='--')
    dl.set_label('Position limit')
    ax[1, 0].legend(loc='best')

    # Cylinder velocity
    df.plot(ax=ax[2, 0], y=['Cyl1_Vel_Ideal', 'Cyl2_Vel_Ideal', 'Cyl3_Vel_Ideal'], x='Timestamp', kind='line')
    ax[2, 0].set_ylabel('Cylinder vel. [mm/s]')
    dl = ax[2, 0].axhline(736, color='black', ls='--')
    ax[2, 0].axhline(-736, color='black', ls='--')
    dl.set_label('Velocity limit')
    ax[2, 0].legend(loc='best')

    # Heave
    df.plot(ax=ax[0, 1], y=['MRU1_Heave', 'MRU2_Heave', 'MRU3_Heave'], x='Timestamp', kind='line')
    ax[1, 1].set_ylabel('Heave [deg]')

    # roll
    df.plot(ax=ax[1, 1], y=['MRU1_Roll', 'MRU2_Roll', 'MRU3_Roll'], x='Timestamp', kind='line')
    ax[1, 1].set_ylabel('Roll [deg]')

    # pitch
    df.plot(ax=ax[2, 1], y=['MRU1_Pitch', 'MRU2_Pitch', 'MRU3_Pitch'], x='Timestamp', kind='line')
    ax[1, 1].set_ylabel('Pitch [deg]')

    # HeaveGain
    df.plot(ax=ax[3, 1], y=['Heave_Gain_DC', 'Heave_Gain_Stroke', 'Heave_Gain_Speed'], x='Timestamp',
            kind='line')
    ax[2, 1].set_ylabel('gain [-]')

    # HeaveGain
    df.plot(ax=ax[3, 0], y=['Heave_Gain_DC', 'Heave_Gain_Stroke', 'Heave_Gain_Speed'], x='Timestamp',
            kind='line')
    ax[2, 1].set_ylabel('gain [-]')

    return fig, ax

def heave_gain_histogram(df):
    # plot histogram
    hist, bins = np.histogram(df['Heave_Gain_DC'], bins=np.arange(0.3, 1 + 0.15, 0.05))
    fig, ax = plt.subplots(1, 1, figsize=(10, 4))
    ax.bar(bins[:-1], hist.astype(np.float32) / hist.sum(), width=(bins[1] - bins[0]), color='grey')
    ax.set_title('Normalized histogram of heave gain DC')
    ax.set_ylabel('number of datapoints, normalized')
    ax.set_xlabel('heave gain DC')
    return fig, ax

def power_consumption(df):
    fig, ax = plt.subplots(1, 1, sharex=True)

    ax = [ax]
    # Power Consumption
    df.plot(ax=ax[0], y='Power_Consumption', x='Timestamp', kind='line')
    # df.plot(ax=ax[0], y='Power_Consumption_unaltered', x='Timestamp', kind='line', ls='--')
    ax[0].set_ylabel('Power consumption [kW]')
    dl = ax[0].axhline(df['Power_Consumption'].mean(), color='blue', ls='--')
    dl.set_label(f'Average power ({df["Power_Consumption"].mean():.0f} kW)')
    d2 = ax[0].axhline(1511, color='black', ls='--')
    d2.set_label('Power limit')
    ax[0].legend(loc='best')
    #
    # # Duty cycle
    # df.plot(ax=ax[1], y='Duty_Cycle', x='Timestamp', kind='line')
    # ax[1].set_ylabel('Cylinders abs vel. sum[mm/s]')
    # dl = ax[1].axhline(1260, color='black', ls='--')
    # dl.set_label('Duty cycle limit')
    # ax[1].legend(loc='best')
    #
    # # Pressure
    # df.plot(ax=ax[2], y='HPU_Press', x='Timestamp', kind='line')
    # ax[2].set_ylabel('HPU_Pressure')
    #
    # # UR
    # df.plot(ax=ax[3], y='Utilisation_Ratio', x='Timestamp', kind='line')
    # ax[3].set_ylabel('UR [%]')


    return fig, ax

def plot_easy(df,variables,ylabels,sharex=True,sharey=False):
    
    nrow,ncol = len(variables),len(variables[0])
    fig, ax = plt.subplots(nrow, ncol, sharex=sharex,sharey=sharey)

    for i, row in enumerate(variables):
        for j, elem in enumerate(row):
            df.plot(ax=ax[i,j], y=elem, x='Timestamp', kind='line')
            ax[i,j].set_ylabel(ylabels[i][j])



    return fig, ax

