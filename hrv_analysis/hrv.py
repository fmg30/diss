""" Calculating HRV values for ECG and PPG data """
import numpy as np

def peaks_to_nn(peak_times):
	# convert the peak times into the NN intervals
	nn_intervals = []
	for i in range(1, len(peak_times)):
		nn_intervals.append(peak_times[i]-peak_times[i-1])

	return nn_intervals

def successive_nn(nn_intervals):
	# convert NN intervals into differences between successive pairs
	successive_nn = []
	for i in range(1, len(nn_intervals)):
		successive_nn.append(nn_intervals[i] - nn_intervals[i-1])

	return successive_nn

def pNN50(peak_times):
	""" Return pNN50: number of pairs of successive NN intervals differing by more than 50ms, 
	expressed as a proportion of the total number of intervals."""

	# convert the peak times into the NN intervals
	nn_intervals = peaks_to_nn(peak_times)

	print("SD: ", np.std(nn_intervals))

	# similar process to find the number of pairs of NN intervals differing by more than 50ms
	NN50 = 0
	for j in range(1, len(nn_intervals)):
		if(nn_intervals[j] - nn_intervals[j-1] > 50):
			NN50 = NN50 + 1

	# express NN50 as a proportion of the total number of NN intervals
	pNN50 = NN50/len(nn_intervals) * 100

	return pNN50


def pNN20(peak_times):
	""" Return pNN20: number of pairs of successive NN intervals differing by more than 20ms, 
	expressed as a proportion of the total number of intervals."""

	# convert the peak times into the NN intervals
	nn_intervals = peaks_to_nn(peak_times)

	# similar process to find the number of pairs of NN intervals differing by more than 20ms
	NN20 = 0
	for j in range(1, len(nn_intervals)):
		if(nn_intervals[j] - nn_intervals[j-1] > 20):
			NN20 = NN20 + 1

	# express NN20 as a proportion of the total number of NN intervals
	pNN20 = NN20/len(nn_intervals) * 100

	return pNN20