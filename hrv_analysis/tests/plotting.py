""" Initial testing file for viewing the PPG data. (No longer used). """

import pandas as pd 
import matplotlib.pyplot as plt
import os
import sys
from scipy import signal

# method for splitting the ppg data out of the logfile
# initial test for plotting w/ R-peaks


def load_data(logfile_path, logfile_name):
	print(logfile_path)
	csv_path = os.path.join(logfile_path, logfile_name)
	return pd.read_csv(csv_path)

def plot_only_ppg(logfile):
	# old method for reading data that doesn't have the sensor name column
	x = logfile['timestamp']
	y = logfile['v0']

	plt.xlabel('Time (s)')
	plt.ylabel('PPG values')
	plt.plot(x, y)
	plt.show()


def plot_sensor(logfile):
	# separate into two dataframes (one for each sensor) based on the name of the sensor
	accdf = logfile[:][logfile.sensor == 'BMI120 Accelerometer Non-wakeup']
	ppgdf = logfile[:][logfile.sensor == 'pah8011_ppg PPG Sensor Non-wakeup']
	# pah8011_ppg PPG Sensor Non-wakeup
	# get x and y for the acceleration data
	xacc = accdf['timestamp']
	yacc = accdf['v0']

	# get x and y for the ppg data
	xppg = ppgdf['timestamp']
	yppg = ppgdf['v0']

	fig, (ax1, ax2) = plt.subplots(2, 1, sharex=False)
	plt.xlabel('Time (s)')
	plt.ylabel('PPG values')
	ax1.set_title('Raw Data')
	ax2.set_title('Acc Data')

	ax1.plot(xppg, yppg)
	ax2.plot(xacc, yacc)

	plt.show()

logfile_name = sys.argv[1]
logfile_raw = load_data("./Raw/", logfile_name)

if(len(sys.argv) > 2 and sys.argv[2] == 'old'):
	plot_only_ppg(logfile_raw)
else:
	plot_sensor(logfile_raw)


def print_sensor_names():
	# print unique sensor names labelled in logfile
	uniques = logfile.sensor.unique()
	print(uniques)
