"""
Working directory in python shell must be 'ESRF_ID06'.

To run in terminal without closing python shell:
exec(open("1D_Darkfield_mapping.py").read(), globals())

"""

# import Functions
import importlib
import os
import Functions as F # Separate script in the 'ESRF_ID06' folder.
importlib.reload(F)

master_folder = os.getcwd()
print(master_folder)

background_folder = os.path.join(master_folder, 'Backgrounds')
files, filenames = F.loadFolder(background_folder, DataType='.edf')

F.displayFiles(files, filenames, fps=2, Mute=False)

F.closeFiles(Files=files)
# loadFolder()