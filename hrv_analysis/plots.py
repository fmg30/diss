""" File containing code for graphs. """

import matplotlib.pyplot as plt

import pandas as pd 

import numpy as np
from scipy.fftpack import rfft, irfft, fftfreq
from scipy.signal import detrend
import scipy

from matplotlib.patches import Ellipse

from matplotlib.lines import Line2D

def plot_acc(acc_watch, x_acc_df):
	""" Plot the acceleration signals (before/after syncing) from the watch and ECG together """
	fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
	plt.xlabel('Time (ms)')
	plt.ylabel('acc. value')
	ax1.set_title('Acceleration Data from ECG')
	ax2.set_title('Acceleration Data from Watch')

	# ecg data
	ax1.plot(x_acc_df['timestamp'], x_acc_df['x_acc'] )
	# ppg data
	ax2.plot(acc_watch['timestamp'], acc_watch['v0'])

	plt.show()

def plot_window_acc(acc_watch, x_acc_df, start, end):
	""" Plots graphs displaying window of interest (excluding high acceleration areas)."""
	fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
	plt.xlabel('Time (ms)')
	plt.ylabel('acc. value')
	ax1.set_title('Acceleration Data from ECG')
	ax2.set_title('Acceleration Data from Watch')

	# window of interest (without major acceleration changes)
	ax1.axvline(x=start, color='red')
	ax2.axvline(x=start, color='red')
	ax1.axvline(x=end, color='red')
	ax2.axvline(x=end, color='red')

	# ecg data
	ax1.plot(x_acc_df['timestamp'], x_acc_df['x_acc'] )
	# ppg data
	ax2.plot(acc_watch['timestamp'], acc_watch['v0'])

	plt.show()

def plot_window_ppg(ppg_data, ecg_df, start, end):
	""" Plots graphs displaying window of interest (excluding high acceleration areas)."""
	fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
	plt.xlabel('Time (ms)')
	# plt.ylabel('acc. value')
	ax1.set_title('ECG Data from ECG')
	ax2.set_title('PPG Data from Watch')

	# window of interest (without major acceleration changes)
	ax1.axvline(x=start, color='red')
	ax2.axvline(x=start, color='red')
	ax1.axvline(x=end, color='red')
	ax2.axvline(x=end, color='red')

	# ecg data
	ax1.plot(ecg_df['timestamp'], ecg_df['ecg'] )
	# ppg data
	ax2.plot(ppg_data['timestamp'], ppg_data['v0'])

	plt.show()

def plot_ECG_peaks(ecg_df, r_peaks):
	""" Plot the ECG annotated with identified R-peaks. """
	# peak_times = ecg_df.iloc[r_peaks]['timestamp']
	peak_times = r_peaks
	ecg_df['is_peak'] = ecg_df['timestamp'].isin(peak_times) 

	plt.figure()
	plt.plot(ecg_df['timestamp'], ecg_df['ecg'])
	plt.plot(ecg_df[ecg_df['is_peak']]['timestamp'], ecg_df[ecg_df['is_peak']]['ecg'], 'ro')
	plt.title('Detected R-peaks on ECG Data')
	plt.xlabel('Time (ms)')
	plt.ylabel('Voltage (mV)')
	plt.show()

def plot_power(ppg_data):
	# sampling frequency and data
	fs = 100
	signal = ppg_data['v0'].values

	# detrend the data since it is heavily biased positive 
	signal = detrend(signal, type='linear')

	# absolute values of fourier transform
	abs_f_transform = np.abs(np.fft.rfft(signal))

	# square components 
	ps = np.square(abs_f_transform)
	freq = np.linspace(0, fs/2, len(ps))

	plt.figure()
	plt.plot(freq, ps)
	plt.xlabel('Hz')
	plt.show()

def plot_filters(ppg_data):
	""" Plot the PPG data before and after it is filtered."""

	fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
	plt.xlabel('Time (ms)')
	plt.ylabel('PPG values')
	ax1.set_title('PPG Before Filtering')
	ax2.set_title('PPG After Filtering')

	# before filter
	ax1.plot(ppg_data['timestamp'], ppg_data['v0'] )
	# after filter
	ax2.plot(ppg_data['timestamp'], ppg_data['filtered'])

	plt.show()

def plot_ppg_peaks(ppg_data, freq):
	""" Plot PPG peaks on the data."""
	# dataframe containing only the peaks and their filtered values
	peak_df = ppg_data[ppg_data["is_peak"]][['timestamp', 'filtered']]

	""" Plotting on filtered data using the dataframe containing only peaks."""
	plt.figure()
	plt.plot(ppg_data['timestamp'], ppg_data['filtered'])
	plt.plot(peak_df['timestamp'], peak_df['filtered'], 'ro')
	plt.title('Detected R-peaks on PPG Data (filtered) at ' + freq)
	plt.xlabel('Time (ms)')
	plt.ylabel('PPG values (filtered)')
	plt.show()

	peak_df_unfilt = ppg_data[ppg_data["is_peak"]][['timestamp', 'v0']]
	""" Plotting on unfiltered data. """
	plt.figure()
	plt.plot(ppg_data['timestamp'], ppg_data['v0'])
	plt.plot(peak_df_unfilt['timestamp'], peak_df_unfilt['v0'], 'ro')
	plt.title('Detected R-peaks on PPG Data (unfiltered) at ' + freq)
	plt.xlabel('Time (ms)')
	plt.ylabel('PPG values (unfiltered)')
	plt.show()

def plot_ppg_peaks_different_freqs(ppg_data, freq, original_data, original_freq):
	""" Plot PPG peaks calculated from lower sampling rate on the original data."""

	# dataframe containing only the peaks and their filtered values
	peak_df = ppg_data[ppg_data["is_peak"]][['timestamp', 'filtered']]

	""" Plotting on filtered data using the dataframe containing only peaks."""
	plt.figure()
	plt.plot(original_data['timestamp'], original_data['filtered'])
	plt.plot(peak_df['timestamp'], peak_df['filtered'], 'ro')
	plt.title('Detected R-peaks calculated at ' + freq + ' plotted on the filtered data sampled at ' + original_freq)
	plt.xlabel('Time (ms)')
	plt.ylabel('PPG values (filtered)')
	plt.show()

	peak_df_unfilt = ppg_data[ppg_data["is_peak"]][['timestamp', 'v0']]

	""" Plotting on unfiltered data. """
	plt.figure()
	plt.plot(original_data['timestamp'], original_data['v0'])
	plt.plot(peak_df_unfilt['timestamp'], peak_df_unfilt['v0'], 'ro')
	plt.title('Detected R-peaks calculated at ' + freq + ' plotted on the unfiltered data sampled at ' + original_freq)
	plt.xlabel('Time (ms)')
	plt.ylabel('PPG values (unfiltered)')
	plt.show()

def plot_ppg_peaks_multiple(ppg_data1, ppg_data2, title):

	# dataframe containing only the peaks and their filtered values
	peak_df1 = ppg_data1[ppg_data1["is_peak"]][['timestamp', 'filtered']]
	peak_df2 = ppg_data2[ppg_data2["is_peak"]][['timestamp', 'filtered']]

	""" Plotting on filtered data using the dataframe containing only peaks."""
	plt.figure()
	plt.plot(ppg_data1['timestamp'], ppg_data1['filtered'])
	plt.plot(ppg_data2['timestamp'], ppg_data2['filtered'])
	p1 = plt.scatter(peak_df1['timestamp'], peak_df1['filtered'], marker = 'o', color = 'blue')
	p2 = plt.scatter(peak_df2['timestamp'], peak_df2['filtered'], marker = 'x', color = 'red')
	plt.legend((p1, p2), ("Peak at higher sampling rate", "Peak at lower sampling rate"))	
	plt.title(title + " (filtered)")
	plt.xlabel('Time (ms)')
	plt.ylabel('PPG values (filtered)')

	plt.show()

	peak_df_unfilt1 = ppg_data1[ppg_data1["is_peak"]][['timestamp', 'v0']]
	peak_df_unfilt2 = ppg_data2[ppg_data2["is_peak"]][['timestamp', 'v0']]

	""" Plotting on unfiltered data. """
	plt.figure()
	plt.plot(ppg_data1['timestamp'], ppg_data1['v0'])
	plt.plot(ppg_data2['timestamp'], ppg_data2['v0'])
	plt.plot(peak_df_unfilt1['timestamp'], peak_df_unfilt1['v0'], 'ro')
	plt.plot(peak_df_unfilt2['timestamp'], peak_df_unfilt2['v0'], 'x')
	plt.title(title + " (unfiltered)")
	plt.xlabel('Time (ms)')
	plt.ylabel('PPG values (unfiltered)')
	plt.show()

def plot_ppg_peaks_multiple_interpolated(ppg_data1, ppg_data2):

	# dataframe containing only the peaks and their filtered values
	peak_df1 = ppg_data1[ppg_data1["is_peak"]][['timestamp', 'filtered']]
	peak_df2 = ppg_data2

	""" Plotting on filtered data using the dataframe containing only peaks."""
	plt.figure()
	plt.plot(ppg_data1['timestamp'], ppg_data1['filtered'])
	plt.plot(ppg_data2['timestamp'], ppg_data2['filtered'])
	plt.plot(peak_df1['timestamp'], peak_df1['filtered'], 'ro')
	plt.plot(peak_df2['timestamp'], peak_df2['filtered'], 'x')
	plt.title('Detected R-peaks on PPG Data (filtered) at ')
	plt.xlabel('Time (ms)')
	plt.ylabel('PPG values (filtered)')
	plt.show()

def plot_scatter(data1, data1label, data2, data2label, xlabel, ylabel, title, lines = []):
	plt.figure()
	p1 = plt.scatter(np.linspace(1, len(data1), len(data1)), y=data1, marker = 'x', color = 'r')
	p2 = plt.scatter(np.linspace(1, len(data2), len(data2)), y=data2, marker = 'x')
	plt.legend((p1, p2), (data1label, data2label))
	plt.title(title)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)

	for line in lines:
		plt.axhline(y=line, color='g', linestyle = '-')

	plt.show()

def poincare(data, title):
	# plot a Poincare/return map of the data; (x_t, x_t+1) etc. 
	x = np.array(data[:-1]) # x_0 to x__n-1)
	y = np.array(data[1:]) # x_1 to x_n

	x_1 = (1/np.sqrt(2))*(x-y)
	x_2 = (1/np.sqrt(2))*(x+y)
	SD1 = np.sqrt(np.var(x_1))
	SD2 = np.sqrt(np.var(x_2))

	print("SD1: ", SD1)
	print("SD2: ", SD2)

	center = (np.mean(x), np.mean(y))
	SD2end = (SD2*np.cos(np.deg2rad(45)), SD2*np.cos(np.deg2rad(45)))

	fig, ax = plt.subplots(1, 1)
	NNs = plt.scatter(x, y, s = 2)
	plt.xlim(500, 1500)
	plt.xlabel('NN interval [i] (ms)')
	plt.ylabel('NN interval [i+1] (ms)')
	plt.ylim(500, 1500)
	loi = plt.plot(range(600, 1400, 1), range(600, 1400, 1), linestyle = '--', color='grey', label = 'identity line')
	ell_patch = Ellipse(center, 2*SD1, 2*SD2, -45, edgecolor='black', facecolor='none')
	ax.add_patch(ell_patch)
	line = Line2D([0,1],[0,1],linestyle='-', color='black')
	line2 = Line2D([0,1], [0, 1], linestyle = '--', color = 'grey')
	ax.legend([line, line2, NNs], ['fitted ellipse', 'identity line', 'NN interval'])
	print(title)
	plt.show()

def plot_pNN_against_freq(frequency, pNN50, pNN20):
	# plot the change in HRV calculations as the sampling rate is changed

	plt.figure()
	nn50 = plt.scatter(frequency, pNN50, marker = 'x', color='blue')
	nn20 = plt.scatter(frequency, pNN20, marker = 'x', color= 'red')
	plt.plot(frequency, pNN50)
	plt.plot(frequency, pNN20)
	plt.xlim(0, 100)
	plt.ylim(0, 50)
	plt.xlabel('Decreasing Sampling Rate (Hz)', fontsize=14)
	plt.xticks(fontsize=14)
	plt.ylabel('%', fontsize=14)
	plt.yticks(fontsize=14)
	plt.gca().invert_xaxis()
	plt.legend((nn20, nn50), ('pNN20 result', 'pNN50 result'), fontsize=12)
	plt.show()
