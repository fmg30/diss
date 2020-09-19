""" Return array of R-peaks identified using library containing the engzee detector. """

from ecgdetectors import Detectors

def find_peaks(ecg_df):
	unfiltered_ecg = ecg_df['ecg'].values
	fs = 500 # sampling freq. in Hz

	detectors = Detectors(fs)

	# r_peaks = detectors.two_average_detector(unfiltered_ecg)
	# r_peaks = detectors.matched_filter_detector(unfiltered_ecg,"templates/template_250hz.csv")
	# r_peaks = detectors.swt_detector(unfiltered_ecg)
	r_peaks = detectors.engzee_detector(unfiltered_ecg)
	# r_peaks = detectors.christov_detector(unfiltered_ecg)
	# r_peaks = detectors.hamilton_detector(unfiltered_ecg)
	# r_peaks = detectors.pan_tompkins_detector(unfiltered_ecg)

	r_peaks = ecg_df['timestamp'][r_peaks].values

	return r_peaks

	