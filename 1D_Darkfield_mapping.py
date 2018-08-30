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
                                      DataType='.edf', Mute=True)

# Convert background images to numpy.array
BG_array = np.zeros((1,2,len(BG_filess)))
print(np.shape(BG_array))

# Load 1D data images.
# oneD_data_folder = os.path.join(master_folder, 'Mosa_chi_scan_RT')
# oneD_data_files, oneD_data_filenames = F.loadFolder(oneD_data_folder,
#                                       DataType='.edf', Mute=True)

# F.displayFiles(oneD_data_files, oneD_data_filenames,
#                fps=2, Mute=False)

F.closeFiles(Files=files)
# loadFolder()