import pandas as pd
from tkinter import *
from tkinter import filedialog
from os import listdir
import numpy as np
import os.path
from datetime import datetime, timedelta
from dateutil import parser


def read_csv(file, save_feather_folder='feather/', save_to_feather=True):
    df = pd.read_csv(file, index_col=None, header=0, skiprows=[1, 2])

    timestamps = []
    for i in range(df.shape[0]):
        timestamp = pd.Timestamp(year=df['S_Year'].values[0],
                                 month=df['S_Month'].values[0],
                                 day=df['S_Day'].values[0],
                                 hour=df['S_Hour'].values[0],
                                 minute=df['S_Minutes'].values[0],
                                 second=df['S_Seconds'].values[0]) + \
                    timedelta(seconds=df['Time_Msec_Current_010'].values[i])
        timestamps.append(timestamp)

    df.insert(175, "Timestamp", timestamps,
              allow_duplicates=False)  # Add a new 176th column with all the timestamps

    # Drop columns that have no information
    columns_to_drop = [
        'Time', 'S_Day', 'S_Hour', 'S_Minutes', 'S_Month', 'S_Seconds', 'S_Year', 'MTI_AccX', 'MTI_AccY', 'MTI_AccZ',
        'MTI_GyrX', 'MTI_GyrY', 'MTI_GyrZ', 'MTI_MagX', 'MTI_MagY', 'MTI_MagZ', 'MTI_pitch', 'MTI_roll',
        'MTI_TS', 'MTI_yaw', 'TimeStampSec', 'Time_Msec_Current_010', 'Time_Msec_Current_025',
        'Time_Msec_Current_050', 'Time_Msec_Current_100', 'Time_Msec_start_010', 'Time_Msec_start_025',
        'Time_Msec_start_050', 'Time_Msec_start_100', 'MY_DATE_TIME', 'BOX_BAT_PROC', 'BOX_BAT_TIME',
        'BOX_BAT_TIME_HOUR', 'YMD_HMS', '_TimeStampLow', 'MRU01_010', 'MRU02_063_DEG', 'MRU02_063_DEG_SHIP',
        'MRU02_064_DEG', 'MRU02_064_DEG_SHIP', 'MRU02_065_DEG', 'MRU02_065_DEG_SHIP', 'MRU02_336_SHIP',
        'Acc_Mp1_x', 'Acc_Mp1_y', 'Acc_Mp1_z', 'MRU01_011', 'MRU01_064_DEG', 'MRU01_065_DEG',
        'MRU01_065_DEG_SHIP', 'MRU01_132', 'MRU01_202', 'MRU01_336_SHIP', 'MRU02_010', 'MRU02_011', 'MRU02_060',
        'MRU02_061', 'MRU02_062', 'MRU02_063', 'MRU02_064', 'MRU02_065', 'MRU02_130', 'MRU02_131', 'MRU02_132',
        'MRU02_173', 'MRU02_300', 'MRU02_301', 'MRU02_302', 'MRU02_303', 'MRU02_304', 'MRU02_305', 'MRU02_314',
        'MRU02_324', 'MRU02_325', 'MRU02_326', 'MRU02_336', 'PLC04_Spare_2', 'PLC09_Spare_4', 'PLC14_Spare_6',
        'PLC15_Spare_7', 'PLC47_Spare_10', 'PLC54_Spare_11', 'PLC55_Spare_12', 'PLC67_Spare_13', 'PLC72_Time',
        'PLC74_Spare_14', 'PLC75_Spare_15', 'PLC31_Heartbeat']

    df = df.drop(columns=columns_to_drop)

    columns_to_bool = {'PLC24_EM1_Running': bool, 'PLC25_EM2_Running': bool, 'PLC26_EM3_Running': bool,
                       'PLC27_EM4_Running': bool, 'PLC28_EM5_Running': bool, 'PLC29_EM6_Running': bool,
                       'PLC30_EM7_Running': bool, 'PLC57_Freeze_Retract': bool, 'PLC60_Gen1_Running': bool,
                       'PLC61_Gen2_Running': bool, 'PLC62_Gen3_Running': bool, 'PLC64_MRU1_Stable': bool,
                       'PLC65_MRU2_Stable': bool, 'PLC66_MRU3_Stable': bool, 'PLC68_OBL_Mode': bool}

    float = np.float32
    columns_to_float = {'MRU01_060': float, 'MRU01_061': float, 'MRU01_062': float, 'MRU01_063': float,
                        'MRU01_063_DEG_SHIP': float, 'MRU01_064': float, 'MRU01_064_DEG_SHIP': float,
                        'MRU01_065': float, 'MRU01_130': float, 'MRU01_131': float, 'MRU01_300': float,
                        'MRU01_301': float, 'MRU01_302': float, 'MRU01_303': float, 'MRU01_304': float,
                        'MRU01_305': float, 'MRU01_314': float, 'MRU01_324': float, 'MRU01_325': float,
                        'MRU01_326': float, 'MRU01_336': float, 'PLC00_MRU1_Roll': float,
                        'PLC01_MRU1_Pitch': float, 'PLC02_MRU1_Heave': float, 'PLC03_Spare_1': float,
                        'PLC05_MRU2_Roll': float, 'PLC06_MRU2_Pitch': float, 'PLC07_MRU2_Heave': float,
                        'PLC08_Spare_3': float, 'PLC10_MRU3_Roll': float, 'PLC11_MRU3_Pitch': float,
                        'PLC12_MRU3_Heave': float, 'PLC13_Spare_5': float, 'PLC16_Heave_Gain_Stroke': float,
                        'PLC17_Heave_Gain_Speed': float, 'PLC18_Heave_Gain_DC': float,
                        'PLC19_Heave_Offset_Neutral': float, 'PLC20_HPU_Press': float,
                        'PLC21_HPU_Temp_Oil_1': float, 'PLC22_HPU_Temp_Oil_2': float,
                        'PLC23_HPU_Temp_Air': float, 'PLC35_Cyl1_Pos_Ideal': float,
                        'PLC36_Cyl2_Pos_Ideal': float, 'PLC37_Cyl3_Pos_Ideal': float,
                        'PLC38_Cyl1_Pres_Rod': float, 'PLC39_Cyl2_Pres_Rod': float,
                        'PLC40_Cyl3_Pres_Rod': float, 'PLC41_Cyl1_Pres_Bot': float,
                        'PLC42_Cyl2_Pres_Bot': float, 'PLC43_Cyl3_Pres_Bot': float,
                        'PLC44_Cyl1_Pres_Pas': float, 'PLC45_Cyl2_Pres_Pas': float,
                        'PLC46_Cyl3_Pres_Pas': float}

    dt_int = np.int16
    columns_to_int = {'PLC32_Cyl1_Pos_CIMS': dt_int, 'PLC33_Cyl2_Pos_CIMS': dt_int,
                      'PLC34_Cyl3_Pos_CIMS': dt_int, 'PLC48_PassAccu1_Pos': dt_int,
                      'PLC49_PassAccu2_Pos': dt_int, 'PLC50_PassAccu3_Pos': dt_int,
                      'PLC51_ActAccu1_Pres': dt_int, 'PLC52_ActAccu2_Pres': dt_int,
                      'PLC53_ActAccu3_Pres': dt_int, 'PLC56_Utilisation_Ratio': dt_int,
                      'PLC58_System_Mode': dt_int, 'PLC59_Active_Control_Loop': dt_int,
                      'PLC63_Gen_Fuel': dt_int, 'PLC71_OBL_Angle_Orientation': dt_int}

    dt_int_h = np.int32
    columns_to_int_h = {'MRU01_173': dt_int_h, 'PLC69_OBL_Distance_X': dt_int_h, 'PLC70_OBL_Distance_Y': dt_int_h,
                        'PLC73_Time_Compensation': dt_int_h}

    df = df.astype(columns_to_bool)
    df = df.astype(columns_to_float)
    df = df.astype(columns_to_int)
    df = df.astype(columns_to_int_h)

    # The csv that was loaded will be saved to feather by default. This allows (much) quicker loading times if the data
    # in this csv needs to be retrieved again.
    if save_to_feather:
        directory, filename = os.path.split(file)
        fullpath = os.path.join(directory, save_feather_folder, filename[:-3] + 'ftr')
        df.to_feather(fullpath)

    return df


def load(filenames=False, initialdir="../data", save_feather_folder='feather/', save_to_feather=True,
         ff=lambda df: df):
    # if the user does not give any filenames, a file dialog will be shown in which the user can select the files
    # required
    if not filenames:
        Tk()
        filenames = filedialog.askopenfilenames(initialdir=initialdir,
                                                title="Select data files",
                                                filetypes=(("csv files", "*.csv"), ("all files", "*.*")))

    # at this point the filenames of the files that need to be loaded are known
    li = []
    for file in filenames:
        # first check if this csv is available in the feather folder, if not, load the csv
        directory, filename = os.path.split(file)
        fullpath = os.path.join(directory, save_feather_folder, filename[:-3] + 'ftr')
        if not os.path.exists(fullpath):
            # the feather file is not available, load the csv version
            frame = read_csv(file, save_feather_folder=save_feather_folder, save_to_feather=save_to_feather)
            print('Feather file not found, creating new feather file for', filename)
        else:
            # the feather file is available, it will be read to get the data quicker
            frame = pd.read_feather(fullpath)

        # set the Timestamp as the pandas index
        frame = frame.set_index(frame['Timestamp'])

        # apply the filter function to this pandas dataframe. If no filter is given, the default lambda function is just
        # a feed trough
        frame = ff(frame)

        # append the (filtered) frame to the list
        li.append(frame)

    # create one pandas frame from the list and sort the values according to timestamp
    df = pd.concat(li, axis=0, ignore_index=True)
    df = df.sort_values(['Timestamp'], ascending=[True])  # sorting values
    return df


def load_datarange(startdate, enddate, datafolder='../data/', save_feather_folder='feather/', save_to_feather=True,
                   ff=lambda df: df):
    # This function loads a specific datarange. It looks in the datafolder for all the files that fall within this data
    # range. It applies a datarange filter on top of any other filter that the user gives.

    # get the filenames that are in the datafolder and fall within the datarange +-15m
    filenames = get_AS10_filenames_datarange(startdate, enddate, datafolder)

    # combine the datarange filter and the user filter
    combined_filter_function = lambda df: ff(df.loc[startdate:enddate])

    # give the loading task to the loading function with the correct filenames and adjusted datarange filter
    return load(filenames=filenames, save_feather_folder=save_feather_folder, save_to_feather=save_to_feather,
                ff=combined_filter_function)


def create_timeframe_filter(start, end):
    return lambda df: df.loc[start:end]


def get_AS10_filenames_datarange(start, end, folder='../data/'):
    # this functions looks at all the AS10 type files in the specified folder and checks if it falls within a
    # certain timeframe. It returns a list will all filenames that do.

    # list all filenames
    filenames_all = listdir(folder)

    # check how the start and end time is given, if it is a string (so not a date object), parse it
    if isinstance(start, str):
        start = parser.parse(start)
    if isinstance(end, str):
        end = parser.parse(end)

    # A single A10 file takes 10 minutus, also load the files around that time to ensure we load all required files
    start = start - timedelta(minutes=16)
    end = end + timedelta(minutes=16)

    li = []
    # for each filename, check its date and if it is within the start and end range, if so, append to list.
    for filename in filenames_all:
        if filename.startswith('BM_AS10_') and filename.endswith('.csv'):
            filedate = datetime.strptime(filename[8:14] + filename[15:19], '%y%m%d%H%M')
            if start < filedate < end:
                pathname = os.path.join(folder, filename)
                li.append(pathname)
    return li


def post_process(df):
    df['MRU01_130'] *= 1000

    mapping = {
        'PLC24_EM1_Running': 'EM1_Running',
        'PLC25_EM2_Running': 'EM2_Running',
        'PLC26_EM3_Running': 'EM3_Running',
        'PLC27_EM4_Running': 'EM4_Running',
        'PLC28_EM5_Running': 'EM5_Running',
        'PLC29_EM6_Running': 'EM6_Running',
        'PLC30_EM7_Running': 'EM7_Running',
        'PLC57_Freeze_Retract': 'Freeze_Retract',
        'PLC60_Gen1_Running': 'Gen1_Running',
        'PLC61_Gen2_Running': 'Gen2_Running',
        'PLC62_Gen3_Running': 'Gen3_Running',
        'PLC64_MRU1_Stable': 'MRU1_Stable',
        'PLC65_MRU2_Stable': 'MRU2_Stable',
        'PLC66_MRU3_Stable': 'MRU3_Stable',
        'PLC68_OBL_Mode': 'OBL_Mode',
        'MRU01_060': '060',
        'MRU01_061': '061',
        'MRU01_062': '062',
        'MRU01_063': '063',
        'MRU01_063_DEG_SHIP': 'MRUp_Roll',
        'MRU01_064': '064',
        'MRU01_064_DEG_SHIP': 'MRUp_Pitch',
        'MRU01_065': '065',
        'MRU01_130': 'MRUp_Heave',
        'MRU01_131': '131',
        'MRU01_300': '300',
        'MRU01_301': '301',
        'MRU01_302': '302',
        'MRU01_303': '303',
        'MRU01_304': '304',
        'MRU01_305': '305',
        'MRU01_314': '314',
        'MRU01_324': '324',
        'MRU01_325': '325',
        'MRU01_326': '326',
        'MRU01_336': '336',
        'PLC00_MRU1_Roll': 'MRU1_Roll',
        'PLC01_MRU1_Pitch': 'MRU1_Pitch',
        'PLC02_MRU1_Heave': 'MRU1_Heave',
        'PLC03_Spare_1': 'Spare_1',
        'PLC05_MRU2_Roll': 'MRU2_Roll',
        'PLC06_MRU2_Pitch': 'MRU2_Pitch',
        'PLC07_MRU2_Heave': 'MRU2_Heave',
        'PLC08_Spare_3': 'Spare_3',
        'PLC10_MRU3_Roll': 'MRU3_Roll',
        'PLC11_MRU3_Pitch': 'MRU3_Pitch',
        'PLC12_MRU3_Heave': 'MRU3_Heave',
        'PLC13_Spare_5': 'Spare_5',
        'PLC16_Heave_Gain_Stroke': 'Heave_Gain_Stroke',
        'PLC17_Heave_Gain_Speed': 'Heave_Gain_Speed',
        'PLC18_Heave_Gain_DC': 'Heave_Gain_DC',
        'PLC19_Heave_Offset_Neutral': 'Heave_Offset_Neutral',
        'PLC20_HPU_Press': 'HPU_Press',
        'PLC21_HPU_Temp_Oil_1': 'HPU_Temp_Oil_1',
        'PLC22_HPU_Temp_Oil_2': 'HPU_Temp_Oil_2',
        'PLC23_HPU_Temp_Air': 'HPU_Temp_Air',
        'PLC35_Cyl1_Pos_Ideal': 'Cyl1_Pos_Ideal',
        'PLC36_Cyl2_Pos_Ideal': 'Cyl2_Pos_Ideal',
        'PLC37_Cyl3_Pos_Ideal': 'Cyl3_Pos_Ideal',
        'PLC38_Cyl1_Pres_Rod': 'Cyl1_Pres_Rod',
        'PLC39_Cyl2_Pres_Rod': 'Cyl2_Pres_Rod',
        'PLC40_Cyl3_Pres_Rod': 'Cyl3_Pres_Rod',
        'PLC41_Cyl1_Pres_Bot': 'Cyl1_Pres_Bot',
        'PLC42_Cyl2_Pres_Bot': 'Cyl2_Pres_Bot',
        'PLC43_Cyl3_Pres_Bot': 'Cyl3_Pres_Bot',
        'PLC44_Cyl1_Pres_Pas': 'Cyl1_Pres_Pas',
        'PLC45_Cyl2_Pres_Pas': 'Cyl2_Pres_Pas',
        'PLC46_Cyl3_Pres_Pas': 'Cyl3_Pres_Pas',
        'PLC32_Cyl1_Pos_CIMS': 'Cyl1_Pos_CIMS',
        'PLC33_Cyl2_Pos_CIMS': 'Cyl2_Pos_CIMS',
        'PLC34_Cyl3_Pos_CIMS': 'Cyl3_Pos_CIMS',
        'PLC48_PassAccu1_Pos': 'PassAccu1_Pos',
        'PLC49_PassAccu2_Pos': 'PassAccu2_Pos',
        'PLC50_PassAccu3_Pos': 'PassAccu3_Pos',
        'PLC51_ActAccu1_Pres': 'ActAccu1_Pres',
        'PLC52_ActAccu2_Pres': 'ActAccu2_Pres',
        'PLC53_ActAccu3_Pres': 'ActAccu3_Pres',
        'PLC56_Utilisation_Ratio': 'Utilisation_Ratio',
        'PLC58_System_Mode': 'System_Mode',
        'PLC59_Active_Control_Loop': 'Active_Control_Loop',
        'PLC63_Gen_Fuel': 'Gen_Fuel',
        'PLC71_OBL_Angle_Orientation': 'OBL_Angle_Orientation'
    }
    df = df.rename(columns=mapping)
    return df
