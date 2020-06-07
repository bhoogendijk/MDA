import helpers, plotters
import matplotlib.pyplot as plt
from dateutil import parser
import numpy as np


def filter_heavelim(df):
    heavelim = 500  # mm
    df = df[(df['MRU1_Heave'] <= -heavelim) | (df['MRU1_Heave'] >= heavelim) | (
            df['MRU2_Heave'] <= -heavelim) | (df['MRU2_Heave'] >= heavelim) | (
                    df['MRU3_Heave'] <= -heavelim) | (df['MRU3_Heave'] >= heavelim)]
    return df


def filter_system_status(df):
    df = df[(df['System_Mode'] >= 4)]
    return df


timeframes = [
    {'start': '2016-09-21 02:00', 'end': '2016-09-21 15:00'},
    {'start': '2016-10-23 21:00', 'end': '2016-10-24 18:00'},
    {'start': '2016-10-25 03:00', 'end': '2016-10-25 14:00'},
    {'start': '2016-11-23 18:00', 'end': '2016-11-25 12:00'},
    {'start': '2016-12-03 22:00', 'end': '2016-12-04 09:00'},
    {'start': '4-9-19 10:00', 'end': '4-10-19 0:00'},
    {'start': '4-11-19 10:00', 'end': '4-11-19 20:00'},
    {'start': '4-12-19 21:00', 'end': '4-13-19 1:26'},
    {'start': '4-13-19 1:50', 'end': '4-13-19 5:10'},
    {'start': '4-16-19 2:45', 'end': '4-20-19 11:00'},
    {'start': '4-20-19 20:50', 'end': '4-23-19 0:24'},
    {'start': '5-2-19 18:40', 'end': '5-2-19 23:00'},
    {'start': '5-3-19 3:00', 'end': '5-4-19 1:00'},
    {'start': '5-4-19 23:53', 'end': '5-6-19 5:35'},
    {'start': '5-6-19 14:30', 'end': '5-8-19 12:45'},
    {'start': '5-11-19 0:00', 'end': '5-12-19 5:18'},
    {'start': '5-13-19 1:22', 'end': '5-14-19 1:22'},
    {'start': '5-14-19 6:20', 'end': '5-15-19 4:15'},
    {'start': '5-15-19 20:30', 'end': '5-17-19 20:30'},
    {'start': '2019-05-18 04:30', 'end': '2019-05-18 08:30'},
    {'start': '2019-05-19 04:00', 'end': '2019-05-19 14:00'},
    {'start': '2019-05-19 16:00', 'end': '2019-05-21 08:00'},
    {'start': '2019-05-25 00:00', 'end': '2019-05-27 06:00'},
    {'start': '2019-05-28 00:00', 'end': '2019-05-31 12:00'},
    {'start': '2019-06-01 10:00', 'end': '2019-06-01 18:00'},
    {'start': '2019-06-01 22:00', 'end': '2019-06-02 04:00'},
    {'start': '2019-06-02 05:00', 'end': '2019-06-03 03:00'},
    {'start': '2019-06-03 06:00', 'end': '2019-06-03 13:00'},
    {'start': '2019-06-03 14:00', 'end': '2019-06-04 07:00'},
    {'start': '2019-06-07 00:00', 'end': '2019-06-10 00:00'},
    {'start': '2019-06-10 08:00', 'end': '2019-06-11 12:00'},
    {'start': '2019-06-13 12:00', 'end': '2019-06-17 02:00'},

]

run = 0
save = True
for timeframe in timeframes:
    run += 1
    start = timeframe['start']
    end = timeframe['end']

    # load the data
    df = helpers.load_datarange(start, end, ff=filter_system_status)
    print('loading data completed')

    # calculate cylinder velocities and duty cycle
    df = helpers.add_derivative_data(df)

    # print UR
    helpers.calculate_UR(df, print_to_cli=True)

    max_data_point_to_plot = 100000
    n = len(df.Timestamp)
    if n > max_data_point_to_plot:
        a = np.linspace(0, len(df.Timestamp) - 1, max_data_point_to_plot).astype(int)
        df_for_plot = df.iloc[a]
        df = None
        print('Reduced the number of datapoints in loaded dataset for plotting by a factor of {:.1f}'.format(
            n / max_data_point_to_plot))
    else:
        df_for_plot = df

    sf = parser.parse(start)
    ef = parser.parse(end)
    savename = f"run {run} {sf.strftime('%Y-%m-%d %H%M')} till {ef.strftime('%Y-%m-%d %H%M')} "
    savenameUR = 'plots/' + savename + 'UR.png'
    savenameRPH = 'plots/' + savename + 'RPH.png'

    # plot the data
    figur, axur = plotters.UR_criteria(df_for_plot)
    figur.set_size_inches(19, 12.8)

    if save: plt.savefig(savenameUR, bbox_inches='tight', dpi=100)

    figRPH, axRPH = plotters.RPH(df_for_plot, axur)
    figRPH.set_size_inches(19, 12.8)
    if save: plt.savefig(savenameRPH, bbox_inches='tight', dpi=100);

    # plotters.heave_gain_histogram(df)

    # plt.show()

    figur.clf()
    plt.close(figur)
    figRPH.clf()
    plt.close(figRPH)
