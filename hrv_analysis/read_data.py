""" Functions for reading raw data from various file types. """

import os
import numpy as np
import pandas as pd
import pathlib
# library for reading EDF file format
import pyedflib

import matplotlib.pyplot as plt

def read_ECG():
	""" Open and read EDF (European Data Format) file 

	Adds timestamps and returns ecg data, and acceleration data for x axis. 

	Sampling frequencies: 500Hz (ECG), 100Hz for X, Y, Z Acceleration.
	"""
	file_name = os.path.join('', './ECG/20200221/08-38-21.EDF')
	file = pyedflib.EdfReader(file_name)

	# 20200221/08-38-21 FILE			
	# 340 seconds
	# sampling frequencies: 500Hz (ECG), 100Hz for X, Y, Z Accel
	# final two columns are Marker and HRV, ignore for now

	# create time datapoints in milliseconds (avoids accuracy issues with floats)
	# ecg samples at 500Hz, acceleration at 100Hz

	# range in steps of 2ms (500Hz)
	ecg_time = np.arange(0, 340000, 2)

	# range in steps of 10ms (100Hz)
	acc_time = np.arange(0, 340000, 10)

	# read signals from file (currently only using x_axis acceleration)
	ecg_data = file.readSignal(0)
	x_acc_data = file.readSignal(1)
	y_acc_data = file.readSignal(2)
	z_acc_data = file.readSignal(3)

	# join timestamps into the array for both ecg and acceleration data
	ecg_data = np.concatenate((ecg_time.reshape(-1, 1), ecg_data.reshape(-1, 1)), axis=1)
	x_acc_data = np.concatenate((acc_time.reshape(-1, 1), x_acc_data.reshape(-1, 1)), axis=1)
	
	# create dataframe and column names 
	ecg_df = pd.DataFrame(data = ecg_data, columns=['timestamp', 'ecg'])
	x_acc_df = pd.DataFrame(data = x_acc_data, columns=['timestamp', 'x_acc'])

	return(ecg_df, x_acc_df)

def read_PPG():
	""" Read in PPG file
	Returns dataframe of acceleration data, and df of ppg data from smartwatch.
	"""
	current_dir = pathlib.Path(__file__).resolve()
	logfile = current_dir.parent/'Raw'/'feb21wground'
	logfile = pd.read_csv(logfile)

	# separate into two dataframes (one for each sensor) based on the name of the sensor
	accdf = logfile[:][logfile.sensor == 'BMI120 Accelerometer Non-wakeup']
	ppgdf = logfile[:][logfile.sensor == 'pah8011_ppg PPG Sensor Non-wakeup']

	# start timestamp at 0, convert to ms
	accdf['timestamp'] = (accdf['timestamp'] - accdf['timestamp'].iloc[0]) * 1000
	ppgdf['timestamp'] = (ppgdf['timestamp'] - ppgdf['timestamp'].iloc[0]) * 1000

	# drop the columns not currently used
	ppgdf = ppgdf.drop(['v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9', 'v10', 'v11', 'v12', 'v13', 'v14', 'v15', 'v16', 'v17'], axis=1)

	return(ppgdf, accdf)

def shift_timestamps(df, shift):
	""" Shift the timestamps on a dataframe by given amount for syncing."""

	sync_df = df
	sync_df['timestamp'] = (sync_df['timestamp'] - shift)

	return sync_df

def select_window(df, start, end):
	""" Returns the dataframe with only the rows between start to end. """
	mask = (df['timestamp'] > start) & (df['timestamp'] <= end)

	df = df.loc[mask]

	return df


