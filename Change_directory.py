"""
Run this script to change current working directory to ESRF_ID06 folder. Modify the code to match your folder own case.

To run in terminal without closing python shell:
exec(open("\\\\home.ansatt.ntnu.no\\Magnussc\\Documents\\PhD\\Notes\\Python\\GitHub\\ESRF_ID06\\Change_directory.py").read(), globals())
"""
import os
# Modify for your own case.
my_path = os.path.normpath('\\\\home.ansatt.ntnu.no\\Magnussc\\Documents\\PhD\\Notes\\Python\\GitHub\\ESRF_ID06')
os.chdir(my_path)