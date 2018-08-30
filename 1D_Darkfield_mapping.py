"""
Working directory in python shell must be 'ESRF_ID06'.

To run in terminal without closing python shell:
exec(open("1D_Darkfield_mapping.py").read(), globals())

"""

# import Functions
import importlib
import numpy as np
import os
import Functions as F # Separate script in the 'ESRF_ID06' folder.
importlib.reload(F)

master_folder = os.getcwd()

# Load background images.
background_folder = os.path.join(master_folder, 'Backgrounds')
BG_files, BG_filenames = F.loadFolder(background_folder,
                                      DataType='0000.edf', Mute=True)
# Load 1D data images.
oneD_data_folder = os.path.join(master_folder, 'Mosa_chi_scan_RT')
oneD_data_files, oneD_data_filenames = F.loadFolder(oneD_data_folder,
                                                    DataType='2258.edf',
                                                    Mute=True)

# Convert background images to numpy.array
BG_array = F.make_data_array(BG_files)
# Convert 1D data images to numpy.array
oneD_data_array = F.make_data_array(oneD_data_files)

# For each pixel, find median value through all images.
BG_median = np.median(BG_array, axis=2)

# Get some values.
ffz = F.getMotorValue(BG_files[0].header, 'ffz')
ffx = 5000.0
two_theta = np.arctan(ffz/ffx)*180/np.pi
obpitch = F.getMotorValue(BG_files[0].header, 'obpitch')


# Subtract background median from data images.
# oneD_BG_sub = oneD_data_array - BG_median

print(ffz, ffx, two_theta, obpitch)
# for name in sorted(BG_files[0].header['motor_mne'].split()):
#     print(name)


# F.displayFiles(oneD_data_files, oneD_data_filenames,
#                fps=2, Mute=False)

F.closeFiles(Files=BG_files, Mute=True)
F.closeFiles(Files=oneD_data_files, Mute=True)
# loadFolder()