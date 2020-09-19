""" Filters for pre-processing PPG data. """

from scipy.signal import butter, sosfilt, sosfiltfilt, sosfreqz

def butterworth_bandpass_coeffs(lowcut, highcut, fs, order=5):
	""" Butterworth bandpass filter design: returns filter coefficients. """

	# Nyquist frequency is half the sampling rate
	nyquist = 0.5 * fs

	# critical frequencies: the points at which the gain drops to 1/sqrt(2) that of the passband
	low = lowcut / nyquist
	high = highcut / nyquist

	filter_coeffs = butter(order, [low, high], analog=False, btype='band', output='sos')
	return filter_coeffs

def butterworth_bandpass_filter(data, lowcut, highcut, fs, order=5):
	""" Butterworth bandpass filter application to data: returns filtered data. """

	# filter design, returns filter coefficients
	filter_coeffs = butterworth_bandpass_coeffs(lowcut, highcut, fs, order=order)
	# apply the filter to the data
	filtered_data = sosfiltfilt(filter_coeffs, data)
	return filtered_data

def filter_ppg(ppg_data):
	""" Return dataframe with added column for filtered ppg data. """

	# sample rate and cutoff frequences (Hz) (based on min/max possible HR values)
	fs = 100 
	low = 0.4
	high = 4.0

	# filter between reasonable HR ranges
	ppg_data['filtered'] = butterworth_bandpass_filter(ppg_data['v0'].values, low, high, fs, order=5)

	return ppg_data
