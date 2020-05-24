import plotly.graph_objects as go
from plotly.subplots import make_subplots
from helpers import *


# define a plotting function to plot the results
def plot_heave_gain(df):
    fig = make_subplots(rows=4, cols=1, shared_xaxes=True)

    fig.append_trace(
        go.Scattergl(x=list(df.Timestamp), y=list(df.PLC02_MRU1_Heave), name='MRU1_heave', yaxis="y"), row=1, col=1)
    fig.append_trace(
            go.Scattergl(x=list(df.Timestamp), y=list(df.PLC07_MRU2_Heave), name='MRU2_heave', yaxis="y"), row=1, col=1)
    fig.append_trace(
        go.Scattergl(x=list(df.Timestamp), y=list(df.PLC12_MRU3_Heave), name='MRU3_heave', yaxis="y"), row=1, col=1)

    fig.append_trace(
        go.Scattergl(x=list(df.Timestamp), y=list(df.PLC16_Heave_Gain_Stroke), name='Heave_Gain_Stroke', yaxis="y1"),
        row=2, col=1)
    fig.append_trace(
        go.Scattergl(x=list(df.Timestamp), y=list(df.PLC17_Heave_Gain_Speed), name='Heave_Gain_Speed', yaxis="y1"), row=2,
        col=1)
    fig.append_trace(
        go.Scattergl(x=list(df.Timestamp), y=list(df.PLC18_Heave_Gain_DC), name='Heave_Gain_DC', yaxis="y1"), row=2,
        col=1)

    fig.append_trace(
        go.Scattergl(x=list(df.Timestamp), y=list(df.PLC58_System_Mode), name='System_Mode', yaxis="y2"),
        row=3, col=1)

    fig.append_trace(
        go.Scattergl(x=list(df.Timestamp), y=list(df.PLC56_Utilisation_Ratio), name='Utilisation_Ratio', yaxis="y3"),
        row=4, col=1)

    # Set title
    fig.update_layout(
        title_text="Time series"
    )

    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="minute",
                         stepmode="backward"),
                    dict(count=15,
                         label="15min",
                         step="minute",
                         stepmode="backward"),
                    dict(count=1,
                         label="hour",
                         step="hour",
                         stepmode="backward"),
                    dict(count=1,
                         label="1d",
                         step="day",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            type="date"
        ), xaxis4_rangeslider_visible=True, xaxis4_rangeslider_thickness=0.1
    )

    fig.show()


# define the filter functions that filters the dataset.
def filter_heave_gain(df):
    df = df[(df['PLC16_Heave_Gain_Stroke'] < 1) |
            (df['PLC17_Heave_Gain_Speed'] < 1) |
            (df['PLC18_Heave_Gain_DC'] < 1)]
    return df


def filter_system_status(df):
    # 0 is off
    # 1 is HPU running
    # 2 is pressurized
    # 3 is position control
    # 4 is compensation

    # nofilter
    df = df[(df['PLC58_System_Mode'] >= 0)]
    return df


# In this case a specific timerange will be loaded from the csv available in the datafolder

# userinput
start = '2019-04-12 00:00:00'
end = '2019-04-14 00:00:00'
datafolder = '../data/'

# load the data
df = load_datarange(start, end, datafolder=datafolder, ff=filter_system_status)
print('Finished loading, now plotting')

# restrict the number of datapoints to plot, otherwise plotting will be too slow.
max_data_point_to_plot = 100000
n = len(df.Timestamp)
if n > max_data_point_to_plot:
    a = np.linspace(0, len(df.Timestamp) - 1, max_data_point_to_plot).astype(int)
    df = df.iloc[a]
    print('Reducing the loaded dataset for plotting by a factor of {:.1f}'.format(
        n / max_data_point_to_plot))


# plot the data
plot_heave_gain(df)