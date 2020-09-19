import read_data
import plots
import r_peaks_ecg
import filters
import peaks
import hrv

# read in ECG data from raw EDF file
raw_ecg_df, raw_x_acc_df = read_data.read_ECG()

# read in PPG data from smartwatch logfile
raw_ppg_data, raw_acc_watch = read_data.read_PPG()

# plot acceleration data from watch and ecg
# plots.plot_acc(raw_acc_watch, raw_x_acc_df)

# sync timestamps for watch with ecg using the difference from acceleration data
acc_watch = read_data.shift_timestamps(raw_acc_watch, 1525)
ppg_data = read_data.shift_timestamps(raw_ppg_data, 1525)

# plot again
# plots.plot_acc(acc_watch, raw_x_acc_df)

# define start and end times of the region of interest (area without acceleration changes, observed from plotting)
# this also greatly reduces the range of the values since the initial ECG data is a large outlier
w_start = 50000
w_end = 300000

# display window of interest on acceleration data
plots.plot_window_acc(acc_watch, raw_x_acc_df, 50000, 300000)

# display window of interest on heartbeat data
# plots.plot_window_ppg(ppg_data, raw_ecg_df, w_start, w_end)

# select window of interest from heartbeat data 
ppg_data = read_data.select_window(ppg_data, w_start, w_end).reset_index()
ecg_df = read_data.select_window(raw_ecg_df, w_start, w_end).reset_index()

# identify R-peaks on ECG data to establish ground truth
peak_times_ecg = r_peaks_ecg.find_peaks(ecg_df)

# plot the results
plots.plot_ECG_peaks(ecg_df, peak_times_ecg)

# plot power spectrum for ppg data
# plots.plot_power(ppg_data)

# add filtered ppg column 
ppg_data = ppg_data.drop_duplicates('timestamp')
ppg_data = filters.filter_ppg(ppg_data)
# plot result
plots.plot_filters(ppg_data)

# create artificially lower sample rate for PPG data (25, 50Hz down from 100Hz)
ppg_data_50 = ppg_data
ppg_data_50 = ppg_data_50.iloc[::2, :]
ppg_data_25 = ppg_data
ppg_data_25 = ppg_data_25.iloc[::4, :]
ppg_data_12 = ppg_data
ppg_data_12 = ppg_data_12.iloc[::8, :]

# simple peak detection algorithm for filtered ppg
ppg_data_simple_peaks = peaks.simple_peaks(ppg_data)
ppg_data_simple_peaks_50 = peaks.simple_peaks(ppg_data_50)
ppg_data_simple_peaks_25 = peaks.simple_peaks(ppg_data_25)
ppg_data_simple_peaks_12 = peaks.simple_peaks(ppg_data_12)

plots.plot_ppg_peaks_multiple(ppg_data_simple_peaks, ppg_data_simple_peaks_12, "Signals and identified peaks at 100 and 12.5 Hz.")

peaks.Lagrange_peaks(plot = True)
ppg_data_interpolated_12 = peaks.peaks_with_interpolation(ppg_data_12, 8)
# plot result
# plots.plot_ppg_peaks(ppg_data_simple_peaks, '100 Hz')
# plots.plot_ppg_peaks(ppg_data_simple_peaks_50, '50 Hz')
# plots.plot_ppg_peaks(ppg_data_simple_peaks_25, '25 Hz')

# plot the peaks calculated from the lower sample rate onto the full data to inspect the errors
# plots.plot_ppg_peaks_different_freqs(ppg_data_simple_peaks_25, '25 Hz', ppg_data_simple_peaks, '100 Hz')
# plots.plot_ppg_peaks_multiple_interpolated(ppg_data_simple_peaks, ppg_data_interpolated_12)

# dataframe containing only the peaks and their filtered values
peak_df = ppg_data_simple_peaks[ppg_data_simple_peaks["is_peak"]][['timestamp', 'filtered']]
peak_df_50 = ppg_data_simple_peaks_50[ppg_data_simple_peaks_50["is_peak"]][['timestamp', 'filtered']]
peak_df_25 = ppg_data_simple_peaks_25[ppg_data_simple_peaks_25["is_peak"]][['timestamp', 'filtered']]
peak_df_12 = ppg_data_simple_peaks_12[ppg_data_simple_peaks_12["is_peak"]][['timestamp', 'filtered']]

# extract time series of peaks (PPG)
peak_times_ppg = peak_df.timestamp.values
peak_times_ppg_50 = peak_df_50.timestamp.values
peak_times_ppg_25 = peak_df_25.timestamp.values
peak_times_ppg_12 = peak_df_12.timestamp.values
peak_times_ppg_interpolated_12 = ppg_data_interpolated_12.timestamp.values

# calculate NN intervals for PPG
nn_intervals_ppg = hrv.peaks_to_nn(peak_times_ppg)
nn_intervals_ppg_50 = hrv.peaks_to_nn(peak_times_ppg_50)
nn_intervals_ppg_25 = hrv.peaks_to_nn(peak_times_ppg_25)
nn_intervals_ppg_12 = hrv.peaks_to_nn(peak_times_ppg_12)
nn_intervals_ppg_interpolated_12 = hrv.peaks_to_nn(peak_times_ppg_interpolated_12)

# calculate differences between successive NN
nn_diff_ppg = hrv.successive_nn(nn_intervals_ppg)
nn_diff_ppg_50 = hrv.successive_nn(nn_intervals_ppg_50)
nn_diff_ppg_25 = hrv.successive_nn(nn_intervals_ppg_25)
nn_diff_ppg_12 = hrv.successive_nn(nn_intervals_ppg_12)
nn_diff_ppg_interpolated_12 = hrv.successive_nn(nn_intervals_ppg_interpolated_12)

# calculate NN intervals for ECG
nn_intervals_ecg = hrv.peaks_to_nn(peak_times_ecg)
# calculate differences between successive NN
nn_diff_ecg = hrv.successive_nn(nn_intervals_ecg)

# def plot_scatter(data1, data1label, data2, data2label, xlabel, ylabel, title):
# plots.plot_scatter(nn_intervals_ppg, "PPG", nn_intervals_ecg, "ECG", "Index of NN interval", "Length of NN Interval (ms)", "The Length of NN intervals from both PPG and ECG sources using the simple peaks algorithm.")
# plots.plot_scatter(nn_diff_ppg, "PPG", nn_diff_ecg, "ECG", "Index of NN difference", "Difference between successive NN (ms)", "The Difference between successive NN intervals from PPG and ECG sources.")

def calculate_and_print_results():
	# calculate ground truth HRV from ECG data
	pNN50_ECG = hrv.pNN50(peak_times_ecg)
	pNN20_ECG = hrv.pNN20(peak_times_ecg)
	print("pNN50, ECG: ", pNN50_ECG)
	print("pNN20, ECG: ", pNN20_ECG)

	# calculate HRV from PPG data
	pNN50_PPG = hrv.pNN50(peak_times_ppg)
	pNN20_PPG = hrv.pNN20(peak_times_ppg)
	print("pNN50, PPG: ", pNN50_PPG)
	print("pNN20, PPG: ", pNN20_PPG)

	# calculate HRV from PPG data (50Hz sample rate)
	pNN50_PPG_50 = hrv.pNN50(peak_times_ppg_50)
	pNN20_PPG_50 = hrv.pNN20(peak_times_ppg_50)
	print("pNN50, PPG at 50Hz: ", pNN50_PPG_50)
	print("pNN20, PPG at 50Hz: ", pNN20_PPG_50)

	# calculate HRV from PPG data (25Hz sample rate)
	pNN50_PPG_25 = hrv.pNN50(peak_times_ppg_25)
	pNN20_PPG_25 = hrv.pNN20(peak_times_ppg_25)
	print("pNN50, PPG at 25Hz: ", pNN50_PPG_25)
	print("pNN20, PPG at 25Hz: ", pNN20_PPG_25)

	# calculate HRV from PPG data (12.5Hz sample rate)
	pNN50_PPG_12 = hrv.pNN50(peak_times_ppg_12)
	pNN20_PPG_12 = hrv.pNN20(peak_times_ppg_12)
	print("pNN50, PPG at 12.5Hz: ", pNN50_PPG_12)
	print("pNN20, PPG at 12.5Hz: ", pNN20_PPG_12)

	pNN50_list = [pNN50_PPG, pNN50_PPG_50, pNN50_PPG_25, pNN50_PPG_12]
	pNN20_list = [pNN20_PPG, pNN20_PPG_50, pNN20_PPG_25, pNN20_PPG_12]
	# plots.plot_pNN_against_freq([100, 50, 25, 12.5], pNN50_list, pNN20_list)

	# calculate HRV from PPG data (interpolated 12.5Hz sample rate)
	print("pNN50, PPG interpolated from 12.5Hz: ", hrv.pNN50(peak_times_ppg_interpolated_12))
	print("pNN20, PPG interpolated from 12.5Hz: ", hrv.pNN20(peak_times_ppg_interpolated_12))

calculate_and_print_results()

plots.poincare(nn_intervals_ecg, "Poincar" + u'é' + " plot of NN intervals from ECG.")
plots.poincare(nn_intervals_ppg, "Poincar" + u'é' + " plot of NN intervals from PPG.")
# plots.poincare(nn_intervals_ppg_50, "Poincar" + u'é' + " plot of NN intervals from PPG at 50Hz.")
# plots.poincare(nn_intervals_ppg_25, "Poincar" + u'é' + " plot of NN intervals from PPG at 25Hz.")
plots.poincare(nn_intervals_ppg_12, "Poincar" + u'é' + " plot of NN intervals from PPG at 12.5Hz.")
plots.poincare(nn_intervals_ppg_interpolated_12, "Poincar" + u'é' + " plot of NN intervals, interpolated from PPG at 12.5Hz.")