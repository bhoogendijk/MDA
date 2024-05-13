import pandas as pd
from tkinter import *
from tkinter import filedialog
from os import listdir
import numpy as np
import os.path
from datetime import datetime, timedelta
from dateutil import parser
from scipy.signal import savgol_filter


def read_csv(file):
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
        'MRU01_065_DEG_SHIP', 'MRU01_132', 'MRU01_336_SHIP', 'MRU02_010', 'MRU02_011', 'MRU02_060',
        'MRU02_061', 'MRU02_062', 'MRU02_063', 'MRU02_064', 'MRU02_065', 'MRU02_130', 'MRU02_131', 'MRU02_132',
        'MRU02_173', 'MRU02_300', 'MRU02_301', 'MRU02_302', 'MRU02_303', 'MRU02_304', 'MRU02_305', 'MRU02_314',
        'MRU02_324', 'MRU02_325', 'MRU02_326', 'MRU02_336', 'PLC04_Spare_2', 'PLC09_Spare_4', 'PLC14_Spare_6',
        'PLC15_Spare_7', 'PLC47_Spare_10', 'PLC54_Spare_11', 'PLC55_Spare_12', 'PLC67_Spare_13', 'PLC72_Time',
        'PLC74_Spare_14', 'PLC75_Spare_15']

    if 'PLC31_Heartbeat' in df: columns_to_drop.append('PLC31_Heartbeat')  # this only exist in data from limetree
    if 'PLC31_Spare_9' in df: columns_to_drop.append("PLC31_Spare_9")  # this only exist in data before limetree

    df = df.drop(columns=columns_to_drop)

    columns_to_bool = {'PLC24_EM1_Running': bool, 'PLC25_EM2_Running': bool, 'PLC26_EM3_Running': bool,
                       'PLC27_EM4_Running': bool, 'PLC28_EM5_Running': bool, 'PLC29_EM6_Running': bool,
                       'PLC30_EM7_Running': bool, 'PLC57_Freeze_Retract': bool, 'PLC60_Gen1_Running': bool,
                       'PLC61_Gen2_Running': bool, 'PLC62_Gen3_Running': bool, 'PLC64_MRU1_Stable': bool,
                       'PLC65_MRU2_Stable': bool, 'PLC66_MRU3_Stable': bool, 'PLC68_OBL_Mode': bool}

    dt_float = np.float32
    columns_to_float = {'MRU01_060': dt_float, 'MRU01_061': dt_float, 'MRU01_062': dt_float, 'MRU01_063': dt_float,
                        'MRU01_063_DEG_SHIP': dt_float, 'MRU01_064': dt_float, 'MRU01_064_DEG_SHIP': dt_float,
                        'MRU01_065': dt_float, 'MRU01_130': dt_float, 'MRU01_131': dt_float, 'MRU01_300': dt_float,
                        'MRU01_301': dt_float, 'MRU01_302': dt_float, 'MRU01_303': dt_float, 'MRU01_304': dt_float,
                        'MRU01_305': dt_float, 'MRU01_314': dt_float, 'MRU01_324': dt_float, 'MRU01_325': dt_float,
                        'MRU01_326': dt_float, 'MRU01_336': dt_float, 'PLC00_MRU1_Roll': dt_float,
                        'PLC01_MRU1_Pitch': dt_float, 'PLC02_MRU1_Heave': dt_float, 'PLC03_Spare_1': dt_float,
                        'PLC05_MRU2_Roll': dt_float, 'PLC06_MRU2_Pitch': dt_float, 'PLC07_MRU2_Heave': dt_float,
                        'PLC08_Spare_3': dt_float, 'PLC10_MRU3_Roll': dt_float, 'PLC11_MRU3_Pitch': dt_float,
                        'PLC12_MRU3_Heave': dt_float, 'PLC13_Spare_5': dt_float, 'PLC16_Heave_Gain_Stroke': dt_float,
                        'PLC17_Heave_Gain_Speed': dt_float, 'PLC18_Heave_Gain_DC': dt_float,
                        'PLC19_Heave_Offset_Neutral': dt_float, 'PLC20_HPU_Press': dt_float,
                        'PLC21_HPU_Temp_Oil_1': dt_float, 'PLC22_HPU_Temp_Oil_2': dt_float,
                        'PLC23_HPU_Temp_Air': dt_float, 'PLC35_Cyl1_Pos_Ideal': dt_float,
                        'PLC36_Cyl2_Pos_Ideal': dt_float, 'PLC37_Cyl3_Pos_Ideal': dt_float,
                        'PLC38_Cyl1_Pres_Rod': dt_float, 'PLC39_Cyl2_Pres_Rod': dt_float,
                        'PLC40_Cyl3_Pres_Rod': dt_float, 'PLC41_Cyl1_Pres_Bot': dt_float,
                        'PLC42_Cyl2_Pres_Bot': dt_float, 'PLC43_Cyl3_Pres_Bot': dt_float,
                        'PLC44_Cyl1_Pres_Pas': dt_float, 'PLC45_Cyl2_Pres_Pas': dt_float,
                        'PLC46_Cyl3_Pres_Pas': dt_float}

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

    # Change the 'units'
    df['MRU01_130'] *= 1000  # Platform heave in meters to heave in mm
    df['MRU01_314'] *= 1000  # Platform heave velocity in m/s to mm/s
    df['MRU01_131'] *= 1000  # Platform heave velocity in MP2 in m/s to mm/s
    # MAP to new better understandable names
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
        'MRU01_131': 'Platform_Heave_MRU4MP2_vel',  # likely incorrect, it is unknown what signal is MP2 and MP1
        'MRU01_300': '300',
        'MRU01_301': '301',
        'MRU01_302': '302',
        'MRU01_303': '303',
        'MRU01_304': '304',
        'MRU01_305': '305',
        'MRU01_314': 'Platform_Heave_MRU4_vel',  # likely incorrect, it is unknown what signal is MP2 and MP1
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


def read_csv_bm001(file):
    # TODO: work in progress. Needs to be adjusted to read BM001 data types and convert to same format as BM003
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
        'MRU01_065_DEG_SHIP', 'MRU01_132', 'MRU01_336_SHIP', 'MRU02_010', 'MRU02_011', 'MRU02_060',
        'MRU02_061', 'MRU02_062', 'MRU02_063', 'MRU02_064', 'MRU02_065', 'MRU02_130', 'MRU02_131', 'MRU02_132',
        'MRU02_173', 'MRU02_300', 'MRU02_301', 'MRU02_302', 'MRU02_303', 'MRU02_304', 'MRU02_305', 'MRU02_314',
        'MRU02_324', 'MRU02_325', 'MRU02_326', 'MRU02_336', 'PLC04_Spare_2', 'PLC09_Spare_4', 'PLC14_Spare_6',
        'PLC15_Spare_7', 'PLC47_Spare_10', 'PLC54_Spare_11', 'PLC55_Spare_12', 'PLC67_Spare_13', 'PLC72_Time',
        'PLC74_Spare_14', 'PLC75_Spare_15']

    if 'PLC31_Heartbeat' in df: columns_to_drop.append('PLC31_Heartbeat')  # this only exist in data from limetree
    if 'PLC31_Spare_9' in df: columns_to_drop.append("PLC31_Spare_9")  # this only exist in data before limetree

    df = df.drop(columns=columns_to_drop)

    columns_to_bool = {'PLC24_EM1_Running': bool, 'PLC25_EM2_Running': bool, 'PLC26_EM3_Running': bool,
                       'PLC27_EM4_Running': bool, 'PLC28_EM5_Running': bool, 'PLC29_EM6_Running': bool,
                       'PLC30_EM7_Running': bool, 'PLC57_Freeze_Retract': bool, 'PLC60_Gen1_Running': bool,
                       'PLC61_Gen2_Running': bool, 'PLC62_Gen3_Running': bool, 'PLC64_MRU1_Stable': bool,
                       'PLC65_MRU2_Stable': bool, 'PLC66_MRU3_Stable': bool, 'PLC68_OBL_Mode': bool}

    dt_float = np.float32
    columns_to_float = {'MRU01_060': dt_float, 'MRU01_061': dt_float, 'MRU01_062': dt_float, 'MRU01_063': dt_float,
                        'MRU01_063_DEG_SHIP': dt_float, 'MRU01_064': dt_float, 'MRU01_064_DEG_SHIP': dt_float,
                        'MRU01_065': dt_float, 'MRU01_130': dt_float, 'MRU01_131': dt_float, 'MRU01_300': dt_float,
                        'MRU01_301': dt_float, 'MRU01_302': dt_float, 'MRU01_303': dt_float, 'MRU01_304': dt_float,
                        'MRU01_305': dt_float, 'MRU01_314': dt_float, 'MRU01_324': dt_float, 'MRU01_325': dt_float,
                        'MRU01_326': dt_float, 'MRU01_336': dt_float, 'PLC00_MRU1_Roll': dt_float,
                        'PLC01_MRU1_Pitch': dt_float, 'PLC02_MRU1_Heave': dt_float, 'PLC03_Spare_1': dt_float,
                        'PLC05_MRU2_Roll': dt_float, 'PLC06_MRU2_Pitch': dt_float, 'PLC07_MRU2_Heave': dt_float,
                        'PLC08_Spare_3': dt_float, 'PLC10_MRU3_Roll': dt_float, 'PLC11_MRU3_Pitch': dt_float,
                        'PLC12_MRU3_Heave': dt_float, 'PLC13_Spare_5': dt_float, 'PLC16_Heave_Gain_Stroke': dt_float,
                        'PLC17_Heave_Gain_Speed': dt_float, 'PLC18_Heave_Gain_DC': dt_float,
                        'PLC19_Heave_Offset_Neutral': dt_float, 'PLC20_HPU_Press': dt_float,
                        'PLC21_HPU_Temp_Oil_1': dt_float, 'PLC22_HPU_Temp_Oil_2': dt_float,
                        'PLC23_HPU_Temp_Air': dt_float, 'PLC35_Cyl1_Pos_Ideal': dt_float,
                        'PLC36_Cyl2_Pos_Ideal': dt_float, 'PLC37_Cyl3_Pos_Ideal': dt_float,
                        'PLC38_Cyl1_Pres_Rod': dt_float, 'PLC39_Cyl2_Pres_Rod': dt_float,
                        'PLC40_Cyl3_Pres_Rod': dt_float, 'PLC41_Cyl1_Pres_Bot': dt_float,
                        'PLC42_Cyl2_Pres_Bot': dt_float, 'PLC43_Cyl3_Pres_Bot': dt_float,
                        'PLC44_Cyl1_Pres_Pas': dt_float, 'PLC45_Cyl2_Pres_Pas': dt_float,
                        'PLC46_Cyl3_Pres_Pas': dt_float}

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

    # Change the 'units'
    df['MRU01_130'] *= 1000  # Platform heave in meters to heave in mm
    df['MRU01_314'] *= 1000  # Platform heave velocity in m/s to mm/s

    # MAP to new better understandable names
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
        'MRU01_314': 'Platform_Heave_MRU4_vel',
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


def load(filenames=False, initialdir="../data", save_feather_folder='feather', save_to_feather=True,
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
            print('Feather file not found, loading CSV version')
            frame = read_csv(file)
            if save_to_feather:
                # The csv that was loaded will be saved to feather by default.
                # This allows (much) quicker loading times if the data in this csv needs to be retrieved again.
                print('Creating new feather file for', filename)
                directory, filename = os.path.split(file)
                fullpath = os.path.join(directory, save_feather_folder, filename[:-3] + 'ftr')
                frame.to_feather(fullpath)
        else:
            # the feather file is available, it will be read to get the data quicker
            frame = pd.read_feather(fullpath)

        # Index is not saved by feather, hence it is always set after loading the frame
        frame.set_index(frame['Timestamp'], inplace=True)

        # apply the filter function to this pandas dataframe. If no filter is given, the default lambda function is just
        # a feedtrough

        frame = ff(frame)
        # append the (filtered) frame to the list
        li.append(frame)

    # set the Timestamp as the pandas index

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

    # A single A10 file takes 15 minutus, also load the files around that time to ensure we load all required files
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


# below function is written to handle reading BM001 files which have a different naming structure. It is not yet in use.
def get_BM10_filenames_datarange(start, end, folder='../data/'):
    # this functions looks at all the AS10 type files in the specified folder and checks if it falls within a
    # certain timeframe. It returns a list will all filenames that do.

    # list all filenames
    filenames_all = listdir(folder)

    # check how the start and end time is given, if it is a string (so not a date object), parse it
    if isinstance(start, str):
        start = parser.parse(start)
    if isinstance(end, str):
        end = parser.parse(end)

    # A single BM10 file takes 30 minutus, also load the files around that time to ensure we load all required files
    start = start - timedelta(minutes=31)
    end = end + timedelta(minutes=31)

    li = []
    # for each filename, check its date and if it is within the start and end range, if so, append to list.
    for filename in filenames_all:
        if filename.startswith('BM10_') and filename.endswith('.csv'):
            filedate = datetime.strptime(filename[5:11] + filename[12:16], '%y%m%d%H%M')
            if start < filedate < end:
                pathname = os.path.join(folder, filename)
                li.append(pathname)
    return li


def add_derivative_data(df, rotation=270):
    # minimum of heave gain
    # df['Heave_Gain_DC'] = df['Heave_Gain_DC'] * 3 / 2  # TODO: only multiply by 3/2 if all motors are off
    df['Heave_Gain'] = df[['Heave_Gain_DC', 'Heave_Gain_Stroke', 'Heave_Gain_Speed']].min(axis=1)

    df['MRU1_Heave'] *= -1  # BM003 uses heave moving down as positive, so we will adjust to our reference frame
    df['MRU2_Heave'] *= -1  # BM003 uses heave moving down as positive, so we will adjust to our reference frame
    df['MRU3_Heave'] *= -1  # BM003 uses heave moving down as positive, so we will adjust to our reference frame
    df['MRU1_Pitch'] *= -1  # BM003 uses roll portside down down as positive, so we will adjust to our reference frame

    window_size = 13
    polyorder = 2

    # Add cylinder velocities and duty cycles
    y = df['Cyl1_Pos_Ideal'].diff() / df['Timestamp'].diff().dt.total_seconds()
    df['Cyl1_Vel_Ideal'] = savgol_filter(y, window_size, polyorder)
    y = df['Cyl2_Pos_Ideal'].diff() / df['Timestamp'].diff().dt.total_seconds()
    df['Cyl2_Vel_Ideal'] = savgol_filter(y, window_size, polyorder)
    y = df['Cyl3_Pos_Ideal'].diff() / df['Timestamp'].diff().dt.total_seconds()
    df['Cyl3_Vel_Ideal'] = savgol_filter(y, window_size, polyorder)
    y = 3 * df['MRU1_Heave'].diff() / df['Timestamp'].diff().dt.total_seconds()
    df['Duty_Cycle_Heave'] = savgol_filter(y, window_size, polyorder)

    df['Duty_Cycle'] = df['Cyl1_Vel_Ideal'].abs() + df['Cyl2_Vel_Ideal'].abs() + df['Cyl3_Vel_Ideal'].abs()

    area_active = 0.053  # m2
    inefficiency = 0.9
    idle_power = 450  # kW

    P_pump_max = 1511  # kW

    df['Power_Consumption'] = df['Cyl1_Vel_Ideal'].abs() + df['Cyl2_Vel_Ideal'].abs() + df['Cyl3_Vel_Ideal'].abs() * \
                              df['HPU_Press'] * 3 / 10 * area_active / inefficiency

    df['Power_Consumption_unaltered'] = df['Cyl1_Vel_Ideal'].abs() + df['Cyl2_Vel_Ideal'].abs() + df[
        'Cyl3_Vel_Ideal'].abs() * \
                                        df['HPU_Press'] * 3 / 10 * area_active / inefficiency

    df.loc[df.Power_Consumption <= idle_power, 'Power_Consumption'] = idle_power
    df.loc[df.Power_Consumption >= P_pump_max, 'Power_Consumption'] = P_pump_max
    df.loc[df.HPU_Press <= 308, 'Power_Consumption'] = P_pump_max

    # Calculate the platform motions based on the CIMS values

    if rotation == 270:
        df['Platform_Roll_CIMS'] = np.arctan((1 / 2 * df['Cyl1_Pos_CIMS'] + 1 / 2 * df['Cyl2_Pos_CIMS'] - df[
            'Cyl3_Pos_CIMS']) / 11951.1) * 180 / np.pi  # for 270 degree rotation
        df['Platform_Pitch_CIMS'] = np.arctan(
            (df['Cyl1_Pos_CIMS'] - df['Cyl2_Pos_CIMS']) / 13800.0) * 180 / np.pi  # for 270 degree rotation
        df['Platform_Heave_CIMS'] = (df['Cyl1_Pos_CIMS'] + df['Cyl2_Pos_CIMS'] + df['Cyl3_Pos_CIMS']) / 3 - 1250

        df['Platform_Roll_Ideal'] = np.arctan((1 / 2 * df['Cyl1_Pos_Ideal'] + 1 / 2 * df['Cyl2_Pos_Ideal'] - df[
            'Cyl3_Pos_Ideal']) / 11951.1) * 180 / np.pi  # for 270 degree rotation
        df['Platform_Pitch_Ideal'] = np.arctan(
            (df['Cyl1_Pos_Ideal'] - df['Cyl2_Pos_Ideal']) / 13800.0) * 180 / np.pi  # for 270 degree rotation
        df['Platform_Heave_Ideal'] = df['Heave_Gain'] * (
                    (df['Cyl1_Pos_Ideal'] + df['Cyl2_Pos_Ideal'] + df['Cyl3_Pos_Ideal']) / 3)

    elif rotation == 0:
        df['Platform_Pitch_CIMS'] = np.arctan((1 / 2 * df['Cyl1_Pos_CIMS'] + 1 / 2 * df['Cyl2_Pos_CIMS'] - df[
            'Cyl3_Pos_CIMS']) / 11951.1) * 180 / np.pi  # for 0 degree rotation
        df['Platform_Roll_CIMS'] = -np.arctan(
            (df['Cyl1_Pos_CIMS'] - df['Cyl2_Pos_CIMS']) / 13800.0) * 180 / np.pi  # for 270 degree rotation
        df['Platform_Heave_CIMS'] = (df['Cyl1_Pos_CIMS'] + df['Cyl2_Pos_CIMS'] + df['Cyl3_Pos_CIMS']) / 3 - 1250
    #     TODO: add rotation 180 and 90
    else:
        raise ("platform rotation not defined")

    # Rename for clarity
    df['Platform_Roll_MRU4'] = df['MRUp_Roll']
    df['Platform_Pitch_MRU4'] = df['MRUp_Pitch']
    df['Platform_Heave_MRU4'] = df['MRUp_Heave']

    # Calculate the residual platform motions based on vessel motion and Ideal motions (Only works with cylinders
    # actually moving but regardless whether on Hostsim or on skid MRU's.
    df['Residual_Roll_Ideal'] = df['MRU1_Roll'] + df['Platform_Roll_Ideal']
    df['Residual_Pitch_Ideal'] = df['MRU1_Pitch'] + df['Platform_Pitch_Ideal']
    df['Residual_Heave_Ideal'] = df['MRU1_Heave'] + df['Platform_Heave_Ideal']

    # Calculate the residual platform motions based on vessel motion and CIMS motions (Only works with cylinders
    # actually moving but regardless whether on Hostsim or on skid MRU's.
    df['Residual_Roll_CIMS'] = df['MRU1_Roll'] + df['Platform_Roll_CIMS']
    df['Residual_Pitch_CIMS'] = df['MRU1_Pitch'] + df['Platform_Pitch_CIMS']
    df['Residual_Heave_CIMS'] = df['MRU1_Heave'] + df['Platform_Heave_CIMS']

    # Calculate the residual platform motions based on vessel motion and CIMS motions (works in simulations with
    # cylinders actually moving, but only on Hostsim. When on skid MRU's, use the Platform_xxx_MRU4 value directly
    df['Residual_Roll_MRU4'] = df['MRU1_Roll'] + df['Platform_Roll_MRU4']
    df['Residual_Pitch_MRU4'] = df['MRU1_Pitch'] + df['Platform_Pitch_MRU4']
    df['Residual_Heave_MRU4'] = df['MRU1_Heave'] + df['Platform_Heave_MRU4']

    # calculate velocity derivatives
    df['MRU1_Roll_vel_unfiltered'] = df['MRU1_Roll'].diff() / df['Timestamp'].diff().dt.total_seconds()
    df['Platform_Roll_Ideal_vel_unfiltered'] = df['Platform_Roll_Ideal'].diff() / df[
        'Timestamp'].diff().dt.total_seconds()
    df['Platform_Roll_CIMS_vel_unfiltered'] = df['Platform_Roll_CIMS'].diff() / df[
        'Timestamp'].diff().dt.total_seconds()
    df['Platform_Roll_MRU4_vel_unfiltered'] = df['Platform_Roll_MRU4'].diff() / df[
        'Timestamp'].diff().dt.total_seconds()

    df['MRU1_Pitch_vel_unfiltered'] = df['MRU1_Pitch'].diff() / df['Timestamp'].diff().dt.total_seconds()
    df['Platform_Pitch_Ideal_vel_unfiltered'] = df['Platform_Pitch_Ideal'].diff() / df[
        'Timestamp'].diff().dt.total_seconds()
    df['Platform_Pitch_CIMS_vel_unfiltered'] = df['Platform_Pitch_CIMS'].diff() / df[
        'Timestamp'].diff().dt.total_seconds()
    df['Platform_Pitch_MRU4_vel_unfiltered'] = df['Platform_Pitch_MRU4'].diff() / df[
        'Timestamp'].diff().dt.total_seconds()

    df['MRU1_Heave_Velocity_unfiltered'] = df['MRU1_Heave'].diff() / df['Timestamp'].diff().dt.total_seconds()
    df['MRU2_Heave_Velocity_unfiltered'] = df['MRU2_Heave'].diff() / df['Timestamp'].diff().dt.total_seconds()
    df['MRU3_Heave_Velocity_unfiltered'] = df['MRU3_Heave'].diff() / df['Timestamp'].diff().dt.total_seconds()
    df['Platform_Heave_Ideal_vel_unfiltered'] = df['Platform_Heave_Ideal'].diff() / df[
        'Timestamp'].diff().dt.total_seconds()
    df['Platform_Heave_CIMS_vel_unfiltered'] = df['Platform_Heave_CIMS'].diff() / df[
        'Timestamp'].diff().dt.total_seconds()
    # df['Platform_Heave_MRU4_vel'] velocity already exists, no need to differentiate platform MRU heave signal

    # calculate the residuals
    df['Residual_Heave_Ideal_vel_unfiltered'] = df['MRU1_Heave_Velocity_unfiltered'] + df[
        'Platform_Heave_Ideal_vel_unfiltered']
    df['Residual_Heave_CIMS_vel_unfiltered'] = df['MRU1_Heave_Velocity_unfiltered'] + df[
        'Platform_Heave_CIMS_vel_unfiltered']
    df['Residual_Heave_MRU4_vel_unfiltered'] = df['MRU1_Heave_Velocity_unfiltered'] - df['Platform_Heave_MRU4_vel']

    # Filter the signals
    moving_average = 5
    df['MRU1_Roll_vel'] = df['MRU1_Roll_vel_unfiltered'].rolling(moving_average).sum() / moving_average
    df['Platform_Roll_Ideal_vel'] = df['Platform_Roll_Ideal_vel_unfiltered'].rolling(
        moving_average).sum() / moving_average
    df['Platform_Roll_CIMS_vel'] = df['Platform_Roll_CIMS_vel_unfiltered'].rolling(
        moving_average).sum() / moving_average
    df['Platform_Roll_MRU4_vel'] = df['Platform_Roll_MRU4_vel_unfiltered'].rolling(
        moving_average).sum() / moving_average

    df['MRU1_Pitch_vel'] = df['MRU1_Pitch_vel_unfiltered'].rolling(moving_average).sum() / moving_average
    df['Platform_Pitch_Ideal_vel'] = df['Platform_Pitch_Ideal_vel_unfiltered'].rolling(
        moving_average).sum() / moving_average
    df['Platform_Pitch_CIMS_vel'] = df['Platform_Pitch_CIMS_vel_unfiltered'].rolling(
        moving_average).sum() / moving_average
    df['Platform_Pitch_MRU4_vel'] = df['Platform_Pitch_MRU4_vel_unfiltered'].rolling(
        moving_average).sum() / moving_average

    df['MRU1_Heave_Velocity'] = df['MRU1_Heave_Velocity_unfiltered'].rolling(moving_average).sum() / moving_average
    df['MRU2_Heave_Velocity'] = df['MRU2_Heave_Velocity_unfiltered'].rolling(moving_average).sum() / moving_average
    df['MRU3_Heave_Velocity'] = df['MRU3_Heave_Velocity_unfiltered'].rolling(moving_average).sum() / moving_average
    df['Platform_Heave_Ideal_vel'] = df['Platform_Heave_Ideal_vel_unfiltered'].rolling(
        moving_average).sum() / moving_average
    df['Platform_Heave_CIMS_vel'] = df['Platform_Heave_CIMS_vel_unfiltered'].rolling(
        moving_average).sum() / moving_average

    # Calculate the filtered residuals
    df['Residual_Roll_Ideal_vel'] = df['MRU1_Roll_vel'] + df['Platform_Roll_Ideal_vel']
    df['Residual_Roll_CIMS_vel'] = df['MRU1_Roll_vel'] + df['Platform_Roll_CIMS_vel']
    df['Residual_Roll_MRU4_vel'] = df['MRU1_Roll_vel'] + df['Platform_Roll_MRU4_vel']

    df['Residual_Pitch_Ideal_vel'] = df['MRU1_Pitch_vel'] + df['Platform_Pitch_Ideal_vel']
    df['Residual_Pitch_CIMS_vel'] = df['MRU1_Pitch_vel'] + df['Platform_Pitch_CIMS_vel']
    df['Residual_Pitch_MRU4_vel'] = df['MRU1_Pitch_vel'] + df['Platform_Pitch_MRU4_vel']

    df['Residual_Heave_Ideal_vel'] = df['MRU1_Heave_Velocity'] + df['Platform_Heave_Ideal_vel']
    df['Residual_Heave_CIMS_vel'] = df['MRU1_Heave_Velocity'] + df['Platform_Heave_CIMS_vel']
    df['Residual_Heave_MRU4_vel'] = df['MRU1_Heave_Velocity'] - df['Platform_Heave_MRU4_vel']

    # calculate velocity derivatives
    df['Cyl1_Vel_CIMS_unfiltered'] = df['Cyl1_Pos_CIMS'].diff() / df['Timestamp'].diff().dt.total_seconds()
    df['Cyl2_Vel_CIMS_unfiltered'] = df['Cyl2_Pos_CIMS'].diff() / df['Timestamp'].diff().dt.total_seconds()
    df['Cyl3_Vel_CIMS_unfiltered'] = df['Cyl3_Pos_CIMS'].diff() / df['Timestamp'].diff().dt.total_seconds()

    df['Cyl1_Vel_Ideal_unfiltered'] = df['Cyl1_Pos_Ideal'].diff() / df['Timestamp'].diff().dt.total_seconds()
    df['Cyl2_Vel_Ideal_unfiltered'] = df['Cyl2_Pos_Ideal'].diff() / df['Timestamp'].diff().dt.total_seconds()
    df['Cyl3_Vel_Ideal_unfiltered'] = df['Cyl3_Pos_Ideal'].diff() / df['Timestamp'].diff().dt.total_seconds()

    moving_average = 5
    df['Cyl1_Vel_CIMS'] = df['Cyl1_Vel_CIMS_unfiltered'].rolling(moving_average).sum() / moving_average
    df['Cyl2_Vel_CIMS'] = df['Cyl2_Vel_CIMS_unfiltered'].rolling(moving_average).sum() / moving_average
    df['Cyl3_Vel_CIMS'] = df['Cyl3_Vel_CIMS_unfiltered'].rolling(moving_average).sum() / moving_average

    df['Cyl1_Vel_Ideal'] = df['Cyl1_Vel_Ideal_unfiltered'].rolling(moving_average).sum() / moving_average
    df['Cyl2_Vel_Ideal'] = df['Cyl2_Vel_Ideal_unfiltered'].rolling(moving_average).sum() / moving_average
    df['Cyl3_Vel_Ideal'] = df['Cyl3_Vel_Ideal_unfiltered'].rolling(moving_average).sum() / moving_average

    return df


def calculate_UR(df, print_to_cli=False):
    # calculated UR's are only applicable with the following assumptions:
    # - No pump failure or pump turned off (or HPU turned off)
    # - Reduction in heave stroke due to offset in neutral point of compensation not accounted for
    UR_Duty_Cycle = 100 * 3 * np.sqrt(np.mean(df['Duty_Cycle'].pow(2))) / 1260

    UR_Cyl1_Vel = 100 * 3 * df['Cyl1_Vel_Ideal'].std() / 736
    UR_Cyl2_Vel = 100 * 3 * df['Cyl2_Vel_Ideal'].std() / 736
    UR_Cyl3_Vel = 100 * 3 * df['Cyl3_Vel_Ideal'].std() / 736

    UR_Cyl1_Amp = 100 * 3 * (df['Cyl1_Pos_Ideal'] - df['Heave_Offset_Neutral']).std() / 1100
    UR_Cyl2_Amp = 100 * 3 * (df['Cyl2_Pos_Ideal'] - df['Heave_Offset_Neutral']).std() / 1100
    UR_Cyl3_Amp = 100 * 3 * (df['Cyl3_Pos_Ideal'] - df['Heave_Offset_Neutral']).std() / 1100

    UR_Duty_Cycle_Heave = 100 * 3 * df['Duty_Cycle_Heave'].std() / 1260

    UR_Data_Mean = df['Utilisation_Ratio'].mean()

    UR = max(UR_Duty_Cycle, UR_Cyl1_Amp, UR_Cyl2_Amp, UR_Cyl3_Amp, UR_Cyl1_Vel, UR_Cyl2_Vel, UR_Cyl3_Vel)

    UR_lib = {
        'UR': UR,
        'UR_Duty_Cycle': UR_Duty_Cycle,
        'UR_Cyl1_Vel': UR_Cyl1_Vel,
        'UR_Cyl2_Vel': UR_Cyl2_Vel,
        'UR_Cyl3_Vel': UR_Cyl3_Vel,
        'UR_Cyl1_Amp': UR_Cyl1_Amp,
        'UR_Cyl2_Amp': UR_Cyl2_Amp,
        'UR_Cyl3_Amp': UR_Cyl3_Amp,
        'UR_Duty_Cycle_Heave': UR_Duty_Cycle_Heave,
        'UR_Data_Mean': UR_Data_Mean
    }

    if print_to_cli:
        print('UR is {:.0f} percent'.format(UR))
        print('UR_Duty_Cycle is {:.0f} percent'.format(UR_Duty_Cycle))
        print('UR_Duty_Cycle_Heave is {:.0f} percent'.format(UR_Duty_Cycle_Heave))
        print('UR_Cyl1_Amp is {:.0f} percent'.format(UR_Cyl1_Amp))
        print('UR_Cyl2_Amp is {:.0f} percent'.format(UR_Cyl2_Amp))
        print('UR_Cyl3_Amp is {:.0f} percent'.format(UR_Cyl3_Amp))
        print('UR_Cyl1_Vel is {:.0f} percent'.format(UR_Cyl1_Vel))
        print('UR_Cyl2_Vel is {:.0f} percent'.format(UR_Cyl2_Vel))
        print('UR_Cyl3_Vel is {:.0f} percent'.format(UR_Cyl3_Vel))
        print('UR_Data_Mean is {:.0f} percent'.format(UR_Data_Mean))

    return UR_lib
