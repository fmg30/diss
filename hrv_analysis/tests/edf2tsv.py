"""Utility file; convert edf file to tsv format for peak detection library. (No longer required)."""

import os
import pyedflib
import numpy

import matplotlib.pyplot as plt

# read and open EDF file
file_name = os.path.join('', './ECG/20200221/08-38-21.EDF')
file = pyedflib.EdfReader(file_name)

# read signals from file
ecg_data = file.readSignal(0)
acc_data = file.readSignal(1)


print(len(ecg_data)) #170000
print(len(acc_data)) #34000

test = numpy.column_stack((ecg_data, acc_data))

print(test)

numpy.savetxt('./ECG/20200221/08-38-21.tsv', test, delimiter="")
