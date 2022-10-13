import matplotlib.pyplot as plt
import numpy as np


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


def heave_gain_motions(df):
    fig, ax = plt.subplots(3, 3, sharex=True)

    ax[0, 0].get_shared_y_axes().join(ax[0, 0], ax[0, 1])
    ax[0, 0].get_shared_y_axes().join(ax[0, 0], ax[0, 2])

    ax[1, 0].get_shared_y_axes().join(ax[1, 0], ax[2, 0])
    ax[1, 1].get_shared_y_axes().join(ax[1, 1], ax[2, 1])
    ax[1, 2].get_shared_y_axes().join(ax[1, 2], ax[2, 2])


    # HeaveGain stroke
    loc = (0, 0)
    df.plot(ax=ax[loc], y=['Heave_Gain_Stroke'], x='Timestamp', kind='line')
    ax[loc].set_ylabel('gain [-]')

    # HeaveGain velocity
    loc = (0, 1)
    df.plot(ax=ax[loc], y=['Heave_Gain_Speed'], x='Timestamp', kind='line')
    ax[loc].set_ylabel('gain [-]')

    # HeaveGain DC
    loc = (0, 2)
    df.plot(ax=ax[loc], y=['Heave_Gain_DC'], x='Timestamp',
            kind='line')
    ax[loc].set_ylabel('gain [-]')



    # Cylinder position
    loc = (1, 0)
    df.plot(ax=ax[loc], y=['Cyl1_Pos_Ideal', 'Cyl2_Pos_Ideal', 'Cyl3_Pos_Ideal'], x='Timestamp',
            kind='line')
    ax[loc].set_ylabel('Cylinder pos. [mm]')
    dl = ax[loc].axhline(1100, color='black', ls='--')
    ax[loc].axhline(-1100, color='black', ls='--')
    dl.set_label('Position limit')
    ax[loc].legend(loc='best')

    # Cylinder velocity
    loc = (1, 1)
    df.plot(ax=ax[loc], y=['Cyl1_Vel_Ideal', 'Cyl2_Vel_Ideal', 'Cyl3_Vel_Ideal'], x='Timestamp', kind='line')
    ax[loc].set_ylabel('Cylinder vel. [mm/s]')
    dl = ax[loc].axhline(736, color='black', ls='--')
    ax[loc].axhline(-736, color='black', ls='--')
    dl.set_label('Velocity limit')
    ax[loc].legend(loc='best')

    # Duty cycle stroke
    loc = (1, 2)
    df.plot(ax=ax[loc], y='Duty_Cycle', x='Timestamp', kind='line')
    ax[loc].set_ylabel('Cylinders abs vel. sum[mm/s]')
    dl = ax[loc].axhline(1260, color='black', ls='--')
    dl.set_label('Stroke duty cycle limit')
    ax[loc].legend(loc='best')

    # Cylinder position HG
    loc = (2, 0)
    df.plot(ax=ax[loc], y=['Cyl1_Pos_HG', 'Cyl2_Pos_HG', 'Cyl3_Pos_HG'], x='Timestamp',
            kind='line')
    ax[loc].set_ylabel('Cylinder pos. [mm]')
    dl = ax[loc].axhline(1100, color='black', ls='--')
    ax[loc].axhline(-1100, color='black', ls='--')
    dl.set_label('Position limit')
    ax[loc].legend(loc='best')

    # Cylinder velocity HG
    loc = (2, 1)
    df.plot(ax=ax[loc], y=['Cyl1_Vel_HG', 'Cyl2_Vel_HG', 'Cyl3_Vel_HG'], x='Timestamp', kind='line')
    ax[loc].set_ylabel('Cylinder vel. [mm/s]')
    dl = ax[loc].axhline(736, color='black', ls='--')
    ax[loc].axhline(-736, color='black', ls='--')
    dl.set_label('Velocity limit')
    ax[loc].legend(loc='best')

    # Duty cycle stroke HG
    loc = (2, 2)
    df.plot(ax=ax[loc], y='Duty_Cycle_HG', x='Timestamp', kind='line')
    ax[loc].set_ylabel('Cylinders abs vel. sum[mm/s]')
    dl = ax[loc].axhline(1260, color='black', ls='--')
    dl.set_label('Stroke duty cycle limit')
    ax[loc].legend(loc='best')

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
