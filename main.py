import helpers, plotters
import matplotlib.pyplot as plt
from dateutil import parser
import numpy as np
import pandas as pd
import mplcursors

# define filters. These will be used to only load the data the are within the filters. Filters are applied by giving
# them as a variable to the loading function
def filter_heavelim(df):
    heavelim = 500  # mm
    df = df[(df['MRU1_Heave'] <= -heavelim) | (df['MRU1_Heave'] >= heavelim) | (
            df['MRU2_Heave'] <= -heavelim) | (df['MRU2_Heave'] >= heavelim) | (
                    df['MRU3_Heave'] <= -heavelim) | (df['MRU3_Heave'] >= heavelim)]
    return df


def filter_system_status(df):
    df = df[(df['System_Mode'] >= 4)]
    return df


# Define the timeframes. The script will loop through each timeframe seperately. It loads the data it finds that is
# within the timeframe (and the filter). Then code, such as plotting, is applied to the loaded data.
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

# timeframes = timeframes[0:2]

datafolder = '../data/'  # data folder in which the data is searched for. default is '../data/'

max_data_point_to_plot = 50000  # Removes data to for quick plotting at the cost of level of detail at high zoom levels
reduce_plot_datapoints = True  # True: data is reduced to max_data_points_to_plot. False: the data is not reduced

plot_UR = False  # plot the UR figure
plot_RPH = False  # plot the RPH figure
plot_histogram = False  # plot the heave gain histogram figure
plot_heave_gain_roll = True

save_figures = True  # save  the figures that are plotted
show_figures = False  # show  the figures that are plotted

save_key_values = False
filename_key_values = './key_values.csv'

key_values_list = []
# code execution
run_counter = 0
for timeframe in timeframes:
    run_counter += 1

    # LOADING THE DATA
    start = timeframe['start']
    end = timeframe['end']
    df = helpers.load_datarange(start, end, ff=filter_system_status, datafolder=datafolder)
    # df = helpers.load()
    print('loading data completed')

    # CALCULATE ADDITIONAL INFORMATION ABOUT LOADED DATA

    # calculate cylinder velocities and duty cycle
    df = helpers.add_derivative_data(df)

    # calculate active heave gain and UR, combine them in one key values dict
    key_values = {'Heave_Gain_Active': (df['Heave_Gain'][df['Heave_Gain'] < 1]).count() / float(len(df)) * 100.0}
    UR = helpers.calculate_UR(df)
    key_values.update(UR)
    key_values_list.append(key_values)
    print(f'The calculated UR of this sample is {key_values["UR"]:.0f} percent. '
          f'The average UR from the data is {key_values["UR_Data_Mean"]:.0f} percent. '
          f'The heave gain is active {key_values["Heave_Gain_Active"]:.2f} percent of the time')

    # PLOTTING SECTION
    if reduce_plot_datapoints:
        n = len(df.Timestamp)
        if n > max_data_point_to_plot:
            a = np.linspace(0, len(df.Timestamp) - 1, max_data_point_to_plot).astype(int)
            df = df.iloc[a]
            print('Reduced the number of datapoints in loaded dataset for plotting by a factor of {:.1f}'.format(
                n / max_data_point_to_plot))

    # Create filenames for the figures
    sf = parser.parse(start)
    ef = parser.parse(end)
    savename = f"run {run_counter} {sf.strftime('%Y-%m-%d %H%M')} till {ef.strftime('%Y-%m-%d %H%M')} "
    savenameUR = 'plots/' + savename + 'UR.png'
    savenameRPH = 'plots/' + savename + 'RPH.png'
    savenameHGR = 'plots/' + savename + 'HGR.png'

    # plot the data
    if plot_UR:
        figur, axur = plotters.UR_criteria(df)
        figur.set_size_inches(19, 12.8)
        mplcursors.cursor()
        if save_figures: plt.savefig(savenameUR, bbox_inches='tight', dpi=100)

    if plot_RPH:
        # the x axis will can shared between UR and RPH. This allows zooming in UR to reflect in RPH and vice versa.
        figRPH, axRPH = plotters.RPH(df, share_x_axes_with=axur)
        figRPH.set_size_inches(19, 12.8)
        if save_figures: plt.savefig(savenameRPH, bbox_inches='tight', dpi=100)

    if plot_histogram:
        figHist, axHist = plotters.heave_gain_histogram(df)

    if plot_heave_gain_roll:
        figHGR, axHGR = plotters.heave_gain_roll(df)
        figHGR.set_size_inches(19, 12.8)
        if save_figures: plt.savefig(savenameHGR, bbox_inches='tight', dpi=100)

    # show the plots
    if show_figures: plt.show()

    # clear memory and close the figures
    # Since the x-axis is shared between the figures, first both figures must be cleared before any one of them can be
    # closed
    if plot_RPH: figRPH.clf()
    if plot_UR: figur.clf()
    if plot_heave_gain_roll: figHGR.clf()
    if plot_UR: plt.close(figur)
    if plot_RPH: plt.close(figRPH)
    if plot_heave_gain_roll: plt.close(figHGR)
    if plot_histogram: figHist.clf();plt.close(figHist)

key_values = pd.DataFrame(key_values_list)
if save_key_values: key_values.to_csv(filename_key_values)
