""" Initial test for plotting ECG data."""

import pandas as pd 
import matplotlib.pyplot as plt
plt.style.use('seaborn-deep')
import os
import sys
import numpy as np
import pathlib
from scipy import signal
# library for reading EDF file format
import pyedflib


# 20200221/08-38-21 FILE
# 340 seconds
# sampling frequencies: 500Hz (ECG), 100Hz for X, Y, Z Accel
# final two columns are Marker and HRV, ignore for now

# read and open EDF file
file_name = os.path.join('', './ECG/20200221/08-38-21.EDF')
file = pyedflib.EdfReader(file_name)

# create time datapoints in milliseconds (avoids accuracy issues with floats)
# ecg samples at 500Hz, acceleration at 100Hz

# range in steps of 2ms (500Hz)
ecg_time = np.arange(0, 340000, 2).reshape(-1, 1)

# range in steps of 10ms (100Hz)
acc_time = np.arange(0, 340000, 10).reshape(-1, 1)

# read signals from file
ecg_data = file.readSignal(0)
x_acc_data = file.readSignal(1)
y_acc_data = file.readSignal(2)
z_acc_data = file.readSignal(3)


# read in ppg file
current_dir = pathlib.Path(__file__).resolve()
logfile = current_dir.parent/'Raw'/'feb21wground'
logfile = pd.read_csv(logfile)

# separate into two dataframes (one for each sensor) based on the name of the sensor
accdf = logfile[:][logfile.sensor == 'BMI120 Accelerometer Non-wakeup']
ppgdf = logfile[:][logfile.sensor == 'pah8011_ppg PPG Sensor Non-wakeup']

# start timestamp at 0, convert to ms
accdf['timestamp'] = (accdf['timestamp'] - accdf['timestamp'][0]) * 1000

# drop the columns not currently used
ppgdf = ppgdf.drop(['v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9', 'v10', 'v11', 'v12', 'v13', 'v14', 'v15', 'v16', 'v17'], axis=1)

# shift PPG data to synchronise with the ECG
sync_accdf = accdf
sync_ppgdf = ppgdf

sync_accdf['timestamp'] = (sync_accdf['timestamp'] - 1525)
sync_ppgdf['timestamp'] = (sync_ppgdf['timestamp'] - 1525)


def plot_acc_pre_sync():
	# plot signals before syncing acceleration
	fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
	plt.xlabel('Time (ms)')
	plt.ylabel('acc. value')
	ax1.set_title('Acceleration Data from ECG')
	ax2.set_title('Acceleration Data from Watch')

	ax1.plot(acc_time, x_acc_data)
	ax2.plot(accdf['timestamp'], accdf['v0'])

	plt.show()

def plot_acc_post_sync():
	# plot signals before syncing acceleration
	fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
	plt.xlabel('Time (ms)')
	plt.ylabel('acc. value')

	# window of interest (without major acceleration changes)
	ax1.axvline(x=50000, color='red')
	ax2.axvline(x=50000, color='red')
	ax1.axvline(x=300000, color='red')
	ax2.axvline(x=300000, color='red')

	ax1.set_title('Acceleration Data from ECG')
	ax2.set_title('Acceleration Data from Watch')

	ax1.plot(acc_time, x_acc_data)
	ax2.plot(sync_accdf['timestamp'], sync_accdf['v0'])

	plt.show()

def plot_acc_and_cross():
	# plot signals and their cross-correlation
	fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)
	plt.xlabel('Time (ms)')
	plt.ylabel('acc. value')
	ax1.set_title('Acceleration Data from ECG')
	ax2.set_title('Acceleration Data from Watch')
	ax3.set_title('cross-correlation')

	cc = np.correlate(x_acc_data, accdf['v0'])

	ax1.plot(acc_time, x_acc_data)
	ax2.plot(accdf['timestamp'], accdf['v0'])
	ax3.plot(cc)

	print(cc)
	plt.show()
