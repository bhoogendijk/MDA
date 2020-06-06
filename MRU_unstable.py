from helpers import *
import matplotlib.pyplot as plt
import plotters


def filter_heavelim(df):
    heavelim = 500  # mm
    df = df[(df['PLC02_MRU1_Heave'] <= -heavelim) | (df['PLC02_MRU1_Heave'] >= heavelim) | (
            df['PLC07_MRU2_Heave'] <= -heavelim) | (df['PLC07_MRU2_Heave'] >= heavelim) | (
                    df['PLC12_MRU3_Heave'] <= -heavelim) | (df['PLC12_MRU3_Heave'] >= heavelim)]
    return df


def filter_system_status(df):
    df = df[(df['PLC58_System_Mode'] >= 4)]
    return df


start = '2019-05-16 06:00:00'
end = '2019-05-16 12:00:00'

# load the data
df = load_datarange(start, end, ff=filter_system_status)
df = post_process(df)
print('loading data completed')

# plot_heave_and_mru_status(df_for_plot)

df['Heave_Gain'] = df[['Heave_Gain_DC', 'Heave_Gain_Stroke', 'Heave_Gain_Speed']].min(axis=1)

df['Cyl1_Vel_Ideal'] = df['Cyl1_Pos_Ideal'].diff() / df['Timestamp'].diff().dt.total_seconds()
df['Cyl2_Vel_Ideal'] = df['Cyl2_Pos_Ideal'].diff() / df['Timestamp'].diff().dt.total_seconds()
df['Cyl3_Vel_Ideal'] = df['Cyl3_Pos_Ideal'].diff() / df['Timestamp'].diff().dt.total_seconds()

df['Duty_Cycle'] = df['Cyl1_Vel_Ideal'].abs() + df['Cyl2_Vel_Ideal'].abs() + df['Cyl3_Vel_Ideal'].abs()
df['Duty_Cycle_Heave'] = 3 * df['MRU1_Heave'].diff() / df['Timestamp'].diff().dt.total_seconds()
UR_Duty_Cycle = 100 * 3 * df['Duty_Cycle'].std() / 1260
UR_Cyl1_Vel = 100 * 3 * df['Cyl1_Vel_Ideal'].std() / 740
UR_Cyl2_Vel = 100 * 3 * df['Cyl2_Vel_Ideal'].std() / 740
UR_Cyl3_Vel = 100 * 3 * df['Cyl3_Vel_Ideal'].std() / 740

UR_Cyl1_Amp = 100 * 3 * df['Cyl1_Pos_Ideal'].std() / 1250
UR_Cyl2_Amp = 100 * 3 * df['Cyl2_Pos_Ideal'].std() / 1250
UR_Cyl3_Amp = 100 * 3 * df['Cyl3_Pos_Ideal'].std() / 1250

UR_duty_approx = 100 * 3 * df['Duty_Cycle'].std() / 1260

UR = max(UR_Duty_Cycle, UR_Cyl1_Amp, UR_Cyl2_Amp, UR_Cyl3_Amp, UR_Cyl1_Vel, UR_Cyl2_Vel, UR_Cyl3_Vel)

print('UR is {:.0f} procent'.format(UR))
print('UR_Duty_Cycle is {:.0f} procent'.format(UR_Duty_Cycle))
print('UR_Cyl1_Amp is {:.0f} procent'.format(UR_Cyl1_Amp))
print('UR_Cyl2_Amp is {:.0f} procent'.format(UR_Cyl2_Amp))
print('UR_Cyl3_Amp is {:.0f} procent'.format(UR_Cyl3_Amp))
print('UR_Cyl1_Vel is {:.0f} procent'.format(UR_Cyl1_Vel))
print('UR_Cyl2_Vel is {:.0f} procent'.format(UR_Cyl2_Vel))
print('UR_Cyl3_Vel is {:.0f} procent'.format(UR_Cyl3_Vel))

fig_UR, ax_UR = plotters.UR_criteria(df)
fig_RPH, ax_RPH = plotters.RPH(df)
plt.show()


# # plot histogram
# hist, bins = np.histogram(df['PLC18_Heave_Gain_DC'], bins=np.arange(0.3, 1 + 0.15, 0.05))
# fig, ax = plt.subplots(1, 1, figsize=(10, 4))
# ax.bar(bins[:-1], hist.astype(np.float32) / hist.sum(), width=(bins[1] - bins[0]), color='grey')
# ax.set_title('Normalized histogram of heave gain DC')
# ax.set_ylabel('number of datapoints, normalized')
# ax.set_xlabel('heave gain DC')
#
# # COMPARING IDEAL AND CIMS TO ENSURE IT MATCHES
# df.plot(y=['PLC32_Cyl1_Pos_CIMS', 'PLC35_Cyl1_Pos_Ideal'], x='Timestamp')
#
# # PLC32_Cyl1_Pos_CIMS	PLC33_Cyl2_Pos_CIMS	PLC34_Cyl3_Pos_CIMS
#
# # Comparison with different methods of obtaining velocity and a filter attempt
# cyl1_np_vel = np.gradient(df['PLC35_Cyl1_Pos_Ideal'])
# cyl2_np_vel = np.gradient(df['PLC36_Cyl2_Pos_Ideal'])
# cyl3_np_vel = np.gradient(df['PLC37_Cyl3_Pos_Ideal'])
#
# fig, ax = plt.subplots()
# plt.plot(cyl1_np_vel * 10 + cyl2_np_vel * 10 + cyl3_np_vel * 10)
# plt.plot(df['sum_cyl_vel'])
# y = df['sum_cyl_vel'].values
# yhat = savgol_filter(y, 21, 2)  # window size 51, polynomial order 3
# plt.plot(yhat)
#
# UR_duty_savgol = 100 * 3 * np.nanstd(yhat) / 1260
#
# print('UR SAVGOL for this sample is {:.0f} procent'.format(UR_duty_savgol))


