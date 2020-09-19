""" Peak detection algorithms for PPG signal."""
import pandas as pd
import numpy as np
import numpy.polynomial.polynomial as poly
import matplotlib.pyplot as plt

def simple_peaks(filtered_ppg):
	# simple peak-detection function
	ppg_data = filtered_ppg

	prev = 0
	peaks = []
	peak_times = []

	prev_time = 0

	direction = 1

	for index, row in ppg_data.iterrows():
		if direction == 1:
			if row.filtered < prev:
				# found peak
				peak_times.append(prev_time)
				peaks.append(prev)
				direction = 0 
		elif direction == 0:
			if row.filtered > prev:
				direction = 1
		
		prev_time = row.timestamp
		prev = row.filtered

	ppg_peaks = pd.DataFrame(np.column_stack([peaks, peak_times]), columns = ['peaks', 'peak_times'])

	ppg_data['is_peak'] = ppg_data['timestamp'].isin(ppg_peaks.peak_times) 

	return ppg_data

def simple_peaks_with_buffer(filtered_ppg):
	# simple peak-detection function with a buffer to prevent peaks too soon after each other
	ppg_data = filtered_ppg

	prev = 0
	peaks = []
	peak_times = [-20]

	prev_time = 0
	
	direction = 1

	for index, row in ppg_data.iterrows():
		if direction == 1:
			delta = row.timestamp - peak_times[-1]
			if delta <= 200: print("Delta rejected: ", delta)
			if row.filtered < prev and (delta > 200):
				# check peak is not too soon after the previous (200ms)
				# found peak
				peak_times.append(prev_time)
				peaks.append(prev)
				direction = 0 
		elif direction == 0:
			if row.filtered > prev:
				direction = 1
		
		prev_time = row.timestamp
		prev = row.filtered

	peak_times.pop(0)

	ppg_peaks = pd.DataFrame(np.column_stack([peaks, peak_times]), columns = ['peaks', 'peak_times'])

	ppg_data['is_peak'] = ppg_data['timestamp'].isin(ppg_peaks.peak_times) 

	return ppg_data

def peaks_with_interpolation(filtered_ppg, sampling_increase):
	""" Calculate the location of peaks using the same algorithm as previously; then interpolate using the 
	peak and data from either side of it for a (hopefully) more accurate timestamp for the true peak."""

	interpolated_peaks = []

	# use the same algorithm as previously for initial peak identification
	ppg_data = simple_peaks(filtered_ppg).reset_index()

	# indices of peaks
	idx_list = ppg_data.index[ppg_data['is_peak']].tolist()
	for i in idx_list:
		# interpolate between the values at the peak, and one on either side
		interpolated_peaks.append(Lagrange_peaks(ppg_data.loc[i-1:i+1]['timestamp'].values, ppg_data.loc[i-1:i+1]['filtered'].values, sampling_increase))

	return pd.DataFrame(interpolated_peaks, columns = ['timestamp', 'filtered'])
		
def Lagrange_peaks(x = [0, 4, 8], y = [2, 5, 4], sampling_increase=4, plot = False):
	""" Take data points and interpolate between them, returning the new peak timestamp and value. """

	Lagrange = (0, 0, 0) # polynomial representation

	for j in range(len(x)):
		# y_j*l_j(x)

		l_j = (1, 0, 0)
		# calculate Lagrange basis polynomial
		for m in range(len(x)):
			if m == j: continue
			# (x - x_m)/(x_j - x_m) represented as polynomial coefficients
			denom = x[j] - x[m]
			term = (-x[m]/denom, 1/denom, 0)
			l_j = poly.polymul(l_j, term)

		Lagrange = poly.polyadd(Lagrange, poly.polymul(y[j], l_j))

	# use the Lagrange polynomial to estimate the values along the range of timestamps at the original frequency
	xl = np.arange(x[0], x[-1], (x[1]-x[0])/sampling_increase)
	yl = poly.polyval(xl, Lagrange)

	# calculate the peak from the interpolated data
	peak_y = max(yl)
	peak_x = xl[yl.argmax()]

	# optional plot for testing/display
	if plot:
		plt.figure()
		lower_sample_data = plt.scatter(x, y, marker = 'o', color='blue')
		interpolation = plt.plot(xl, yl)
		true_peak = plt.scatter(peak_x, peak_y, marker = 'x', color = 'red')
		plt.title("Interpolating between data points from the lower sample rate.")
		plt.xlabel("Time")
		plt.ylabel("Signal Amplitude")
		plt.legend((lower_sample_data, true_peak), ("lower sample-rate data", "true peak"))
		plt.show()

	return(peak_x, peak_y)


