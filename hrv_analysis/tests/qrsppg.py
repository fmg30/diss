""" Initial testing file for exploring the gathered PPG data. (No longer used). """

import pandas as pd 
import pathlib
import numpy as np
import matplotlib.pyplot as plt

from scipy.signal import butter, sosfilt, sosfiltfilt, sosfreqz

def load_data(logfile_path, logfile_name):
	print(logfile_path)
	csv_path = os.path.join(logfile_path, logfile_name)
	return pd.read_csv(csv_path)

def ppg_dataset_test():
	# plot the example ppg dataset instead of gathered data

	current_dir = pathlib.Path(__file__).resolve()
	test_ppg = current_dir.parent/'example_data'/'bidmc_07_Signals.csv'

	test_data = pd.read_csv(test_ppg)

	x = test_data['Time [s]']
	y = test_data[' PLETH']

	plt.plot(x, y)
	plt.show()

def butter_bandpass(lowcut, highcut, fs, order=5):
	# nyquist frequency is half the sampling rate
	nyq = 0.5 * fs

	low = lowcut / nyq
	high = highcut / nyq

	sos = butter(order, [low, high], analog=False, btype='band', output='sos')
	return sos

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
	sos = butter_bandpass(lowcut, highcut, fs, order=order)
	y = sosfiltfilt(sos, data)
	return y

current_dir = pathlib.Path(__file__).resolve()
logfile = current_dir.parent/'Raw'/'feb21wground'
logfile = pd.read_csv(logfile)

# remove first _s of data to avoid initial spikes and changes
logfile.drop(logfile.index[:1000], inplace=True)

# separate into two dataframes (one for each sensor) based on the name of the sensor
accdf = logfile[:][logfile.sensor == 'BMI120 Accelerometer Non-wakeup']
ppgdf = logfile[:][logfile.sensor == 'pah8011_ppg PPG Sensor Non-wakeup']

# drop the columns not currently used
ppgdf = ppgdf.drop(['v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9', 'v10', 'v11', 'v12', 'v13', 'v14', 'v15', 'v16', 'v17'], axis=1)

# sample rate and cutoff frequences (Hz) (based on min/max possibly HR values)
fs = 100 
low = 0.4
high = 4.0

# filter between reasonable HR ranges
ppgdf['filtered'] = butter_bandpass_filter(ppgdf['v0'].values, low, high, fs, order=5)
# ppgdf['filtered'] = ppgdf['v0']

def simple_peaks(filtered_ppg):
	# simple peak-detection function
	# some noise and extra peaks identified but reasonable otherwise
	ppgdf = filtered_ppg

	prev = 0
	peaks = []
	peak_times = []

	direction = 1

	for index, row in ppgdf.iterrows():
		if direction == 1:
			if row.filtered < prev:
				# found peak
				peak_times.append(row.timestamp)
				peaks.append(row.filtered)

				direction = 0 
		elif direction == 0:
			if row.filtered > prev:
				direction = 1
		
		prev = row.filtered

	return peaks, peak_times

peaks, peak_times = simple_peaks(ppgdf)

ppg_peaks = pd.DataFrame(np.column_stack([peaks, peak_times]), columns = ['peaks', 'peak_times'])

# plot peaks on filtered data
plt.figure()
plt.plot(ppgdf['timestamp'], ppgdf['filtered'])
# plt.plot(ppg_peaks['peak_times'], ppg_peaks['peaks'], 'ro')
plt.show()

# plot peaks on unfiltered data
# plt.figure()
# plt.plot(ppg_peaks['timestamp'], ppg_peaks['v0'])
# plt.show()



# plt.figure()
# plt.plot(unfiltered_ecg)
# plt.plot(r_peaks, unfiltered_ecg[r_peaks], 'ro')
# plt.title('Detected R-peaks')
# plt.show()
