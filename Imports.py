"""
Written for Python 3.6
Author: Magnus Christensen
To be run before ReadData.py
"""
import fabio, time
from os import listdir, path, makedirs
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import dates
from matplotlib import rc
from matplotlib import ticker
from PIL import Image, ImageTk
import png
import tkinter as tk
import calendar
from datetime import date
from datetime import datetime
from datetime import timedelta
import csv
from tkinter.filedialog import askdirectory
"""
To run in python shell and keep shell running:
exec(open("\\\\home.ansatt.ntnu.no/Magnussc/Documents/PhD/Notes/Python/Imports.py").read(), globals())
"""