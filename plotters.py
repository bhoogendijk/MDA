import matplotlib.pyplot as plt


def UR_criteria(df):
    fig, ax = plt.subplots(3, 2, sharex=True)

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
    dl = ax[1, 0].axhline(1250, color='black', ls='--')
    ax[1, 0].axhline(-1250, color='black', ls='--')
    dl.set_label('Position limit')
    ax[1, 0].legend(loc='best')

    # Cylinder velocity
    df.plot(ax=ax[2, 0], y=['Cyl1_Vel_Ideal', 'Cyl2_Vel_Ideal', 'Cyl3_Vel_Ideal'], x='Timestamp', kind='line')
    ax[2, 0].set_ylabel('Cylinder vel. [mm/s]')
    dl = ax[2, 0].axhline(740, color='black', ls='--')
    ax[2, 0].axhline(-740, color='black', ls='--')
    dl.set_label('Velocity limit')
    ax[2, 0].legend(loc='best')

    # system mode
    df.plot(ax=ax[0, 1], y='System_Mode', x='Timestamp', kind='line')
    ax[0, 1].set_ylabel('mode [-]')

    # UR
    df.plot(ax=ax[1, 1], y='Utilisation_Ratio', x='Timestamp', kind='line')
    ax[1, 1].set_ylabel('UR [%]')

    # Heave gain
    df.plot(ax=ax[2, 1], y=['Heave_Gain_DC', 'Heave_Gain_Stroke', 'Heave_Gain_Speed'], x='Timestamp',
            kind='line')
    ax[2, 1].set_ylabel('gain [-]')

    return fig, ax


def RPH(df):
    fig, ax = plt.subplots(3, 2, sharex=True, sharey='row')
    df.plot(ax=ax[0, 0], y=['MRU1_Roll', 'MRU2_Roll', 'MRU3_Roll'], x='Timestamp', kind='line')
    df.plot(ax=ax[0, 1], y=['MRUp_Roll'], x='Timestamp', kind='line')
    ax[0, 0].set_ylabel('Roll [deg]')

    df.plot(ax=ax[1, 0], y=['MRU1_Pitch', 'MRU2_Pitch', 'MRU3_Pitch'], x='Timestamp', kind='line')
    df.plot(ax=ax[1, 1], y=['MRUp_Roll'], x='Timestamp', kind='line')
    ax[1, 0].set_ylabel('Pitch [deg]')

    df.plot(ax=ax[2, 0], y=['MRU1_Heave', 'MRU2_Heave', 'MRU3_Heave'], x='Timestamp', kind='line')
    df.plot(ax=ax[2, 1], y=['MRUp_Heave'], x='Timestamp', kind='line')
    ax[2, 0].set_ylabel('Heave [mm]')
    return fig, ax
