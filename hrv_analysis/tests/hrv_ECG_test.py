""" R-peak identification using library: used to test the different detectors available.

Used for testing/exploring library originally.
"""


import numpy as np
import matplotlib.pyplot as plt
import pathlib
from ecgdetectors import Detectors

# engzee detector identifies 100% of the R peaks from the ECG data (manually checked)

current_dir = pathlib.Path(__file__).resolve()
example_dir = current_dir.parent/'ECG'/'20200221'/'08-38-21.tsv'
unfiltered_ecg_dat = np.loadtxt(example_dir) 
unfiltered_ecg = unfiltered_ecg_dat[:]
fs = 500

detectors = Detectors(fs)

# r_peaks = detectors.two_average_detector(unfiltered_ecg)
# r_peaks = detectors.matched_filter_detector(unfiltered_ecg,"templates/template_250hz.csv")
# r_peaks = detectors.swt_detector(unfiltered_ecg)
r_peaks = detectors.engzee_detector(unfiltered_ecg)
# r_peaks = detectors.christov_detector(unfiltered_ecg)
# r_peaks = detectors.hamilton_detector(unfiltered_ecg)
# r_peaks = detectors.pan_tompkins_detector(unfiltered_ecg)

plt.figure()
plt.plot(unfiltered_ecg)
plt.plot(r_peaks, unfiltered_ecg[r_peaks], 'ro')
plt.title('Detected R-peaks')

plt.show()
