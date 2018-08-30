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
Written for Python 3.6
Author: Magnus Christensen
Run Imports.py first (separated for speedier consequtive runs of this script from terminal)
"""

"""Exception class: """
class MyException(Exception):
    """
    This is an exception class intended to allow throwing and catching of exeptions without unintentionally catching library exception types.
    """

    def __init__(self, *args, **kwargs):

        Exception.__init__(self, *args, **kwargs)

"""Load functions:"""
def namesFromFolder(FolderPath, DataType=None):
    """
    This function returns a list of filenames in a specified folder.

    FolderPath:
        String/path. Folder/directory in which to search for files
    DataType:
        String. If specified (not None), only files with names ending with <DataType> are included, otherwise all files are included.
    FileNames:
        List of strings. Contains the filenames (without directories) of the files found in <FolderPath>.
    """

    """Sort filenames alphabetically"""
    FileNames = sorted(listdir(FolderPath))
    if DataType != None:
        """Make new list only of filenames ending with <DataType>"""
        NewNameList = list()
        for FileName in FileNames:
            if FileName.endswith(DataType):
                NewNameList.append(FileName)
        FileNames = NewNameList
    return FileNames
def loadFolder(FolderPath, DataType=None, Mute=False):
    """
    This function returns a list of image files and a list of corresponding filenames.

    FolderPath:
        String/path. Folder/directory in which to search for images to open
    DataType:
        String. If specified (not None), only files with names ending with <DataType> are included, otherwise all files are included. edf-files are opened with fabio, png with PIL. To allow other data types to be opened, modify the endswith()-expressions and check that fabio or PIL supports the format, or add another module.
    Mute:
        bool. If true, skip print operations (except for unexpected behavior).
    Files:
        List of images (fabio-image or PIL.Image-image)
    FileNames:
        List of strings. Contains the filenames (without directories) of the files in Files (in the same order).
    """

    Files = []  # Fill in later

    FileNames = namesFromFolder(FolderPath, DataType=DataType)

    if len(FileNames) > 0:
        """File(s) found"""
        if FileNames[0].endswith('edf'):  # Test the first file
            if not Mute:
                print('\nLoading files with fabio...')
            for index in range(len(FileNames)):
                FilePath = path.join(FolderPath, FileNames[index])
                Files.append(fabio.open(FilePath))
                if not Mute:
                    print('File loaded with fabio: ' + FilePath)
        elif FileNames[0].endswith('png'):
            if not Mute:
                print('\nLoading files with PIL...')
            for index in range(len(FileNames)):
                FilePath = path.join(FolderPath, FileNames[index])
                Files.append(Image.open(FilePath))
                if not Mute:
                    print('File loaded with PIL: ' + FilePath)
        else:
            """DataType not expected"""
            print('No files loaded')
            return None, None
        return Files, FileNames
    else:
        """No files found"""
        return None, None
def loadFile(FolderPath, Index=0, DataType=None, Mute=False):
    """
    This function returns an image file and a corresponding filename.

    FolderPath:
        String/path. Folder/directory in which to search for images to open
    Index:
        int. Of all files found in <FolderPath>, the returned File is nbr <Index> (alphabetically and zero-indexed).
    DataType:
        String. If specified (not None), only files with names ending with <DataType> are included, otherwise all files are included. edf-files are opened with fabio, png with PIL. To allow other data types to be opened, modify the endswith()-expressions and check that fabio or PIL supports the format, or add another module.
    Mute:
        bool. If true, skip print operations(except for unexpected behavior).
    File:
        image(fabio-image or PIL.Image-image)
    FileName:
        string. Contains the filename(without directory) of the file in File.
    """

    FileNames = namesFromFolder(FolderPath, DataType=DataType)
    if len(FileNames) > 0 and len(FileNames) > Index:
        """File(s) found"""
        FileName = FileNames[Index]
        FilePath = path.join(FolderPath, FileName)
        if FileNames[0].endswith('edf'):  # Test the first file
            File = fabio.open(FilePath)
            if not Mute:
                print('File loaded with fabio: ' + FilePath)
        elif FileNames[0].endswith('png'):
            File = Image.open(FilePath)
            if not Mute:
                print('File loaded with PIL: ' + FilePath)
        else:
            """DataType not expected"""
            print('No file loaded')
            return None, None
        return File, FileNames[Index]
    else:
        """No files found"""
        return None, None
def closeFiles(Files, Mute=False):
    """
    This function closes a list of files.

    Files:
        List of objects with a close() method
    Mute:
        bool. If true, skip print operations.
    """

    for index in range(len(Files)):
        Files[index].close()
    if not Mute:
        print('\nFiles closed with fabio/PIL/etc. ...')

"""Plot/display functions:"""
def displayFile(File, FileName, Duration, Mute=False):
    """
    This function displays a fabio image file with matplotlib.pyplot. The image must be grayscale (single channel). The display normalizes the grayscale range to the data range of the image.

    File:
        fabio.image. File to display
    FileName:
        String. Filename of the image (only needed to print info)
    Duration:
        Float. Nbr. of seconds to display the image
    Mute:
        bool. If true, skip print operations.
    """

    fig = plt.figure()
    ax = fig.gca()
    imgplot = ax.imshow(File.data,
                        cmap='gray',
                        clim=(File.getmin(), File.getmax()))
    if not Mute:
        print('Showing file %s' % FileName)
    plt.pause(Duration)
    plt.close(fig)
def displayFiles(Files, FileNames, fps=1000.0, Mute=False):
    """
    This function displays consecutively images from a list of fabio image files with matplotlib.pyplot. The images must be grayscale (single channel). The display normalizes the grayscale range to the data range of each image.

    Files:
        List of fabio.image. Files to display
    FileNames:
        List of strings. Filenames of the image (only needed to print info)
    fps:
        Float. Nbr. of images to display per second
    Mute:
        bool. If true, skip print operations.
    """

    fig = plt.figure()
    ax = fig.gca()
    imgplot = ax.imshow(Files[0].data, cmap='gray', clim=(
        Files[0].getmin(), Files[0].getmax()))
    if not Mute:
        print('Showing file %s' % FileNames[0])
    plt.pause(1/fps)
    for index in range(len(Files)-1):
        imgplot.set_data(Files[index].data)
        imgplot.set_clim(Files[index].getmin(), Files[index].getmax())
        if not Mute:
            print('Showing file %s' % FileNames[index])
        plt.pause(1/fps)
    plt.close(fig)
    closeFiles(Files)

"""Get metadata from edf-files:"""
def getScanType(Header):
    """
    This function searches through a file header of a fabio.image object - which is a dictionary - for the 'scan' entry, and based on it classifies the scan as a ScanType. The classification is based on the various types used during the June 2018 ESRF beamtime of Magnus Christensen. Strain and rocking scans are both classified as strain by this script due to the 'scan' command at ESRF ID06 being the same for the two cases - only rocking scans are aborted before obpitch changes.
    
    Header:
        Dictionary. Contains the header of an edf-file from ESRF ID06.
    ScanType:
        String. The scan type identified. If no scan type is found, None is returned.
    """

    try:
        scan = Header['scan'].split()
        if 'mesh' in scan and 'diffry' in scan and 'chi' in scan:
            ScanType = 'mosaicity'
        elif 'diffry' in scan and 'ascan' in scan:
            ScanType = 'strain'
        elif 'timescan' in scan:
            ScanType = 'timescan'
        elif 'zapline' in scan and 'diffry' in scan:
            ScanType = 'zapline-diffry'
        elif 'obx' in scan or 'oby' in scan or 'obz' in scan:
            ScanType = 'obfoc'
        elif '(none)' in scan:
            ScanType = 'none'
        elif 'loopscan' in scan:
            ScanType = 'loopscan'
        elif 'diffty' in scan and 'ascan' in scan:
            ScanType = 'diffty'
        elif 'zapimage' in scan and 'diffry' in scan and 'chi' in scan:
            ScanType = 'zapimage-mosaicity'
        else:
            raise MyException('ScanType not recognized')
    except MyException as e:
        print(e)
        return None
    else:
        return ScanType
def getScanParameters(Header):
    """
    This function gets ScanType from getScanType() using a file header of an edf file from ESRF. It returns the parameters of the scan. Different parameters are returned for differet <ScanType> (see the below commented assignments and subsequent return statements). Not all parameters are returned, only included with an assignment for easier modification of the function if necessary.

    Header:
        Dictionary. Contains the header of an edf-file from ESRF ID06.
    """

    try:
        ScanType = getScanType(Header)
        if ScanType not in ['mosaicity', 'strain', 'timescan',
                            'zapline-diffry', 'obfoc', 'none',
                            'loopscan', 'diffty',
                            'zapimage-mosaicity']:
            raise MyException('Invalid ScanType')
    except MyException as e:
        print(e)
        return None
    else:
        scan = Header['scan'].split()
        if ScanType == 'mosaicity':
            diffryMin = scan[2]     # diffry motor lower limit
            diffryMax = scan[3]     # diffry motor upper limit
            diffryN = scan[4]       # number of steps for diffry motor
            chiMin = scan[6]        # chi motor lower limit
            chiMax = scan[7]        # chi motor upper limit
            chiN = scan[8]          # number of steps for chi motor
            ShutterTime = scan[9]   # Shutter time (s)
            return int(diffryN), int(chiN)
        elif ScanType == 'strain':
            diffryMin = scan[2]     # diffry motor lower limit
            diffryMax = scan[3]     # diffry motor upper limit
            diffryN = scan[4]       # number of steps for diffry motor
            return int(diffryN)
        elif ScanType == 'timescan':
            ShutterTime = scan[1]   # Shutter time (s)
            Unknown = scan[2]       # Unknown parameter
            return float(ShutterTime)
        elif ScanType == 'zapline-diffry':
            diffryMin = scan[2]     # diffry motor lower limit
            diffryMax = scan[3]     # diffry motor upper limit
            diffryN = scan[4]       # number of steps for diffry motor
            # exposure time of one zapline image (ms)
            ZapTime = scan[5]
            return int(diffryN)
        elif ScanType == 'obfoc':
            obxPresent = 'obx' in scan  # True if obx moves with scan
            obyPresent = 'oby' in scan  # True if oby moves with scan
            obzPresent = 'obz' in scan  # True if obz moves with scan
            # number of steps for obx/oby/obz to take (in total)
            obxyzN = scan[1 + 3*(obxPresent+obyPresent+obzPresent)]
            return obxyzN
        elif ScanType == 'none':
            return None
        elif ScanType == 'loopscan':
            timeN = scan[1]         # number of time steps
            ShutterTime = scan[2]   # Shutter time (s)
            Unknown = scan[3]       # Unknown parameter
            return timeN
        elif ScanType == 'diffty':
            difftyMin = scan[2]     # diffty motor lower limit
            difftyMax = scan[3]     # diffty motor upper limit
            difftyN = scan[4]       # number of steps for diffty motor
            return difftyN
        elif ScanType == 'zapimage-mosaicity':
            diffryMin = scan[2]     # diffry motor lower limit
            diffryMax = scan[3]     # diffry motor upper limit
            diffryN = scan[4]       # number of steps for diffry motor
            """exposure time of one zap image along diffry(ms) (0 means no zap/temporal integration)"""
            diffryZapTime = scan[5]
            chiMin = scan[7]            # chi motor lower limit
            chiMax = scan[8]            # chi motor upper limit
            chiN = scan[9]              # number of steps for chi motor
            """exposure time of one zap image along chi(ms) (0 means no zap/temporal integration)"""
            chiZapTime = scan[10]
            return int(diffryN), int(chiN)
def getScanLocation(Header, FileName=None):
    """
    This function gets ScanType from getScanType() and corresponding scan parameters from getScanParameters(), and returns the zero-indexed integer representing the current step number of the scan that this particular file (whose header is given) is at. ScanType 'zapline-diffry' and 'zapimage-mosaicity' assumes <TimeStep> a certain place in <FileName>, information not contained in the header, so for these ScanTypes FileName must be given. The FileName must have the timeStep ('zapline-diffry') or chiStep ('zapimage-mosaicity'), one-indexed, at FileName[-18:-14]. The returned values are either explained below or in getScanParameters().
    Header:
        Dictionary. Contains the header of an edf-file from ESRF ID06.
    FileName:
        String. Filename of the edf-file whose header is <Header>
    """
    
    try:
        ScanType = getScanType(Header)
        if ScanType not in ['mosaicity', 'strain', 'timescan',
                            'zapline-diffry', 'obfoc', 'none',
                            'loopscan', 'diffty',
                            'zapimage-mosaicity']:
            raise MyException('Invalid ScanType')
    except MyException as e:
        print(e)
        return None
    else:
        if ScanType == 'mosaicity':
            diffryN, chiN = getScanParameters(Header)
            imageNbr = int(Header['run'])
            #  Current diffry motor position
            diffryStep = ((imageNbr) % (diffryN+1))
            chiStep = (imageNbr//(diffryN+1))
            diffry = getMotorValue(Header, 'diffry')
            #  Current chi motor position
            chi = getMotorValue(Header, 'chi')
            return diffry, chi, diffryStep, chiStep
        elif ScanType == 'strain':
            diffryN = getScanParameters(Header)
            imageNbr = int(Header['run'])
            obpitchN = int(10)  # Assume 11 obpitch-values per diffry
            obpitchStep = imageNbr // (diffryN+1)
            diffryStep = ((imageNbr) % (diffryN+1))
            #  Current diffry motor position
            diffry = getMotorValue(Header, 'diffry')
            #  Current obpitch motor position
            obpitch = getMotorValue(Header, 'obpitch')
            return diffry, obpitch, diffryStep, obpitchStep
        elif ScanType == 'timescan':
            timescanStep = int(Header['run'])
            return timescanStep
        elif ScanType == 'zapline-diffry':
            diffryStep = int(Header['acq_frame_nb'])
            timeStep = int(FileName[-18:-14])-1
            return diffryStep, timeStep
        elif ScanType == 'obfoc':
            obxyzStep = int(Header['run'])
            return obxyzStep
        elif ScanType == 'none':
            return None
        elif ScanType == 'loopscan':
            loopscanStep = int(Header['run'])
            return loopscanStep
        elif ScanType == 'diffty':
            difftyStep = int(Header['run'])
            return difftyStep
        elif ScanType == 'zapimage-mosaicity':
            chiStep = int(FileName[-18:-14])-1
            diffryStep = int(Header['acq_frame_nb'])
            return diffryStep, chiStep
def getNewFileName(FileName, Header):
    """This function returns a new filename which contains the scan step(s) of the current file (whose filename is passed in FileName). Default behavior at ESRF ID06 appends numbers to each file. These numbers (and the '.edf' suffix) are here replaced with a string of the form 'AaBb' or 'Aa', where A is a letter denoting the type of movement scanned over through the scan, and a is the zero-indexed step number the current file is at (and similarly for B and b). If there is a part of <FileName> that is not removed with the removed numbers, this part will be separated from 'Aa' by '-'. If a file contains '.' (apart from '.edf' at the end), it is replaced with '-'. If a file contains '.' (apart from the file type suffix) this is / these are replaced with 'point'.

    The possible A, B combinations are:
        D: diffry motor (y-rotation of sample)
        C: chi motor (sample rotation)
        O: obpitch motor (bjective rotation)
        T: time
        Y: diffty (y-translation of sample)
        Oxyz/Oxy/Ox (and z,y,z permutations thereof): obx, oby and obz motors (x/y/z translation of objective lens)

    FileName
        String. Filename of the edf-file whose header is <Header>
    Header:
        Dictionary. Contains the header of an edf-file from ESRF ID06 named <FileName>.
    newFileName
        String. New filename of the edf-file whose header is <Header>. No data type suffix is added.
    """
    try:
        ScanType = getScanType(Header)
        if ScanType not in ['mosaicity', 'strain', 'timescan',
                            'zapline-diffry', 'obfoc', 'none',
                            'loopscan', 'diffty',
                            'zapimage-mosaicity']:
            raise MyException('Invalid ScanType')
    except MyException as e:
        print(e)
        return None
    else:
        if ScanType == 'mosaicity':
            diffry, chi, diffryStep, chiStep = getScanLocation(Header)
            newFileName = FileName[0:-9]+'-D%iC%i' % (diffryStep,
                                                      chiStep)
        elif ScanType == 'strain':
            diffry, obpitch, diffryStep, obpitchStep = getScanLocation(
                Header)
            newFileName = FileName[0:-9]+'-D%iO%i' % (diffryStep,
                                                      obpitchStep)
        elif ScanType in ['timescan', 'loopscan']:
            timescanStep = getScanLocation(Header)
            newFileName = FileName[0:-9]+'-T%i' % (timescanStep)
        elif ScanType == 'zapline-diffry':
            diffryStep, timeStep = getScanLocation(Header,
                                                   FileName=FileName)
            newFileName = FileName[0:-19]+'-D%iT%i' % (diffryStep,
                                                       timeStep)
        elif ScanType == 'obfoc':
            obxyzStep = getScanLocation(Header)
            newFileName = FileName[0:-9]+'-O'
            scan = Header['scan'].split()
            if 'obx' in scan:
                newFileName += 'x'
            if 'oby' in scan:
                newFileName += 'y'
            if 'obz' in scan:
                newFileName += 'z'
            newFileName += '%i' % (obxyzStep)
        elif ScanType == 'none':
            newFileName = FileName[0:-9]
        elif ScanType == 'diffty':
            difftyStep = getScanLocation(Header)
            newFileName = FileName[0:-9]+'-Y%i' % (difftyStep)
        elif ScanType == 'zapimage-mosaicity':
            diffryStep, chiStep = getScanLocation(Header,
                                                  FileName=FileName)
            newFileName = FileName[0:-19]+'-D%iC%i' % (diffryStep,
                                                       chiStep)

        if newFileName[0] == '-':
            """Guard against names starting with '-', which occurs if the filename has no stem (non-numerical part) originally.
            """
            return newFileName[1:].replace('.', 'point')
        else:
            return newFileName.replace('.', 'point')
def getMotorValue(Header, Name):
    """
    This function returns the motor value in Header whose name is <Name>. The function is based on the syntax of headers from edf files from ESRF ID06, in that there is an entry with motor names in the header, and an entry with the corresponding motor positions in the same order. No failsafe is implemented.

    Header:
        Dictionary. Contains the header of an edf-file from ESRF ID06..
    Name:
        String. Motor name to search for.
    """
    motor_pos = Header['motor_pos'].split()  # Motor positions
    motor_mne = Header['motor_mne'].split()  # Motor Names
    index = motor_mne.index(Name)  # Find <name> entry
    return float(motor_pos[index])
def motorPosArray(Header):
    """
    This function returns a 1D numpy array of the motor position entries in <Header>.

    Header:
        Dictionary. Contains the header of an edf-file from ESRF ID06.
    """
    return np.array(Header['motor_pos'].split()).astype(float)
def getMovedMotors(Header1, Header2):
    """
    This functions returns a list all of motors that have moved between the acquisition of the datafile whose header is Header1, and that whose header is Header2. Each list entry is a tuple with the name of the moved motor as the first entry and the motor value change (from Header1 to Header2) as the second entry. To find the motor positions, motorPosArray() is used.

    Header1 and Header2:
        Dictionary. Contains the header of an edf-file from ESRF
    MovedMotors:
        List of (numerical, string) tuples. Contains all moved motors from Header1 to Header2.
    """
    MotorPosDifference = motorPosArray(Header2) -\
        motorPosArray(Header1)
    NonZeroIndices = np.flatnonzero(MotorPosDifference).tolist()
    MotorNames1 = Header1['motor_mne'].split()
    MovedMotors = []  # Fill in later
    for index in NonZeroIndices:
        MovedMotors.append(
            (MotorNames1[index], str(MotorPosDifference[index])))
    return MovedMotors
def testNbrScanInFoldersJune2018(Mute=False, DataType='edf'):
    """
    This function returns a string that tells if any of the folders returned by getAllFoldersJune2018() contains files with different values (within the same folder) for the 'scan' parameter in the file headers. This function is meant for files from Magnus ESRF ID06 beamtime June 2018, where each folder ideally contains only one scan, but in practice does not. The instances where it does not must be found in order to handle the fact that some functions used in data analysis might expect only one scan per folder.

    Mute:
        If True, skip print operations, otherwise print the folders searched and the findings afterwards.
    DataType:
        String. Data type (suffix) of files whose headers to check.
    Results:
        String. Meant for the print() function. Contains number of file (within folder) whose 'scan' is not the same as the previous file. Results also contains the folder the file is in.

    Returned Results (trimmed) of running this function (with default parameters) is shown below:

    File nbr. 1200  in 10_1_3\diff\cooling_from_590
    File nbr. 59    in 10_1_3\diff\heating_from_540
    File nbr. 100   in 10_1_3\nf\casting_2
    File nbr. 213   in 10_1_3\nf\mosa_saturday_548
    File nbr. 61    in 10_1_3\nf\obfoc1
    File nbr. 37    in 10_1_3\nf\rocking_grain1_551C
    File nbr. 81    in 10_1_3\nf\rocking_saturday_540
    File nbr. 51    in 10_1_3\nf\rocking_saturday_radiography_552_up
    File nbr. 21    in 10_1_5\ff\obfoc3_530C
    File nbr. 10    in 10_1_5\nf\ramp_from_530
    File nbr. 30    in 10_1_5\nf\ramp_from_530
    File nbr. 120   in 10_1_5\nf\ramp_from_530
    File nbr. 148   in 10_1_5\nf\ramp_from_530
    File nbr. 176   in 10_1_5\nf\ramp_from_530
    File nbr. 232   in 10_1_5\nf\ramp_from_530
    File nbr. 260   in 10_1_5\nf\ramp_from_530
    File nbr. 484   in 10_1_5\nf\ramp_from_530
    File nbr. 494   in 10_1_5\nf\ramp_from_530
    File nbr. 994   in 10_1_5\nf\ramp_from_530
    File nbr. 50    in 10_1_5\nf\ramp_from_554to555C
    File nbr. 6     in cooling_10_1_5\ff\mosa_zap_590C
    File nbr. 2     in ooling_10_1_5\ff\test
    File nbr. 1     in cooling_10_1_5\nf\direct_575
    File nbr. 1     in cooling_10_1_5\nf\direct_605
    File nbr. 51    in cooling_10_1_5\nf\direct_610
    """
    Directories = getAllFoldersJune2018()
    Results = ''  # Add contents later
    for Directory in Directories:
        if not Mute:
            print('Searching in: %s\n' % Directory)
        FileNames = namesFromFolder(Directory, DataType=DataType)
        for FileIndex in range(len(FileNames)):
            File, FileName = loadFile(Directory, Index=FileIndex,
                                      DataType=DataType, Mute=True)
            if FileIndex == 0:
                PreviousScan = File.header['scan']
            CurrentScan = File.header['scan']
            if PreviousScan != CurrentScan:
                # Current scan is different from previous
                Results += 'File nbr. %i has different scan from \
                            previous file in %s\n' % (FileIndex,
                                                      Directory)
            PreviousScan = CurrentScan
            File.close()
    if len(Results) == 0:
        Results += 'No folders found with multiple scan inputs'
    if not Mute:
        print(Results)
    return Results
def printAllFolderDates(DriveLetter='D'):
    directories = getAllFoldersJune2018(DriveLetter=DriveLetter)
    PathToRemove = 'D:\\ESRF June 2018\\hxrm_2018-06-20_magnus\\'
    DatedFolders = []
    for directory in directories:
        Folder = path.normpath(directory)
        FileIndices = [0, -1]
        OrderedDate = []
        for FileIndex in FileIndices:
            File, FileName = loadFile(Folder, DataType='edf',
                                      Mute=True, Index=FileIndex)
            if 'time' in File.header:
                HeaderDate = File.header['time']
            elif 'date' in File.header:
                HeaderDate = File.header['date']
            HeaderDate = HeaderDate.split()
            year = HeaderDate[4]
            month = str(list(calendar.month_abbr).index(HeaderDate[1]))
            day = HeaderDate[2]
            hour = HeaderDate[3][0:2]
            minute = HeaderDate[3][3:5]
            second = HeaderDate[3][6:8]
            OrderedDate.append(year + '-' + month + '-' + day + '_' +\
                hour + '-' + minute + '-' + second)
        DatedFolders.append(OrderedDate[0] + ' ' + OrderedDate[1] +\
            '\t' + Folder[len(PathToRemove):])
        File.close()

    DatedFolders = sorted(DatedFolders)
    for DatedFolder in DatedFolders:
        print(DatedFolder)
def convertDateEntry(date_entry):
    day = int(date_entry[0:2])
    month = int(date_entry[3:5])
    year = int(date_entry[6:10])
    hour = int(date_entry[11:13])
    minute = int(date_entry[14:16])
    second = int(date_entry[17:19])
    centisecond = int(date_entry[20:22])
    this_time = datetime(2000, 1, 1,
                             hour=hour,
                             minute=minute,
                             second=second,
                             microsecond=centisecond*10**4)
    this_datetime = datetime(year, month, day,
                             hour=hour,
                             minute=minute,
                             second=second,
                             microsecond=centisecond*10**4)
    return this_datetime, this_time
def getTemperaturesFromFile(file,
                            start_date=(2018, 6, 18),
                            start_time=(21, 45, 18, 78)):
    """Reads a file with temperatures as created by LabVIEW at ESRF June 2018, and finds seconds elapsed from start_date, and returns that and read temperatures in a numpy.array.

    file:
        Strin/path to file to read.
    start_date:
        tuple/list of integers (year, month, day) as binary values (meaning not text). Date to get nbr. of elapsed seconds from.
    start_time:
        tuple/list of integers (hour, minute, second, centisecond). Time to get nbr. of elapsed sedonds from.
    temps_array:
        numpy.array where each row is a temperature entry (seconds passed, cold temp, temp1, temp2, temp3, temp4)
    time_stamps:
        List of datetime.datetime objects, containing date and time of the returned temperature entries.
    """
    FilePath = path.normpath(file)
    """ To be added below: each row is [date time, coldtemp, temp1, temp2, temp3, temp4]"""
    temps_list = []
    these_datetimes = []
    these_times = []
    if path.exists(FilePath):
        File = open(FilePath, 'r')
        reader = csv.reader(File, delimiter='\t')
        start_datetime = datetime(start_date[0], start_date[1], start_date[2], hour=start_time[0], minute=start_time[1], second=start_time[2], microsecond=start_time[3]*10**4)
        for row in reader:
            this_datetime, this_time = convertDateEntry(row[0])
            datetime_diff = this_datetime-start_datetime
            # seconds passed this day
            seconds_of_day = datetime_diff.days * 24 * 60**2
            seconds_of_day += datetime_diff.seconds
            seconds_of_day += datetime_diff.microseconds/10**6
            new_row = np.zeros(np.shape(row))
            new_row[0] = np.float64(seconds_of_day)
            new_row[1:] = np.float64(row[1:])
            temps_list.append(new_row)
            these_datetimes.append(this_datetime)
            these_times.append(this_time)
        File.close()
        temps_array = np.array(temps_list)
        return temps_array, these_datetimes, these_times
    else:
        print('No File found: %s' % file)
        return None, None
def plotAllTemperatures(
        folder=path.normpath('\\\\home.ansatt.ntnu.no\\Magnussc\\Documents\\PhD\\Furnace\\LabView')):
    temps = []  # Fill in later
    file_names = namesFromFolder(folder,
                                 DataType='_Temperature_data.txt')
    for file_name in file_names:
        file_path = path.join(folder, file_name)
        temps.append(getTemperaturesFromFile(file_path))
    font = {'size'   : 22}
    rc('font', **font)
    fig = plt.figure(figsize=(25,8))
    for day in range(len(temps)):
        this_datetime = temps[day][1]  # datetime objects
        time = temps[day][2]  # datetime objects
        temp1 = temps[day][0][:,2]  # Temp. of elment nbr. 1
        temp2 = temps[day][0][:,3]  # Temp. of elment nbr. 2
        temp3 = temps[day][0][:,4]  # Temp. of elment nbr. 3
        temp4 = temps[day][0][:,5]  # Temp. of elment nbr. 4
        sample_temp = (temp2 + temp3) / 2
        plt.plot(time, sample_temp, '.',
                 label=this_datetime[0].date(),
                 markersize=3)
        # for index in range(len(time)):
        #     test = datetime.fromordinal(datetime.toordinal(this_datetime[index]))
            # if datetime.toordinal(this_datetime[index]) <= 1:
            # print(index, 'Find', test)
    ax = plt.gca()
    plt.xlim(datetime(2000,1,1),datetime(2000,1,2))
    plt.grid(which='major', axis='both', linewidth=2)
    plt.grid(which='minor', axis='both', linewidth=0.5)
    plt.legend(loc='upper right',
               bbox_to_anchor=(0.3, 1),
               markerscale=10)
    plt.title('Furnace temperature ESRF June 2018')
    plt.xlabel('Time of day (HH:MM)')
    plt.ylabel('Temperature ($\degree$C)')
    ax.yaxis.set_major_locator(ticker.MultipleLocator(100))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(10))
    ax.xaxis.set_major_locator(dates.MinuteLocator(interval=60))
    ax.xaxis.set_major_formatter(dates.DateFormatter("%H:%M"))
    ax.xaxis.set_minor_locator(dates.MinuteLocator(interval=15))
    # ax.xaxis.set_minor_formatter(dates.DateFormatter("%H:%M:%S"))
    plt.xticks(rotation=90)
    fig.tight_layout()
    fig.savefig('\\\\home.ansatt.ntnu.no\\Magnussc\\Documents\\PhD\\Furnace\\LabView\\temperatureFig.pdf')
    fig.savefig('\\\\home.ansatt.ntnu.no\\Magnussc\\Documents\\PhD\\Furnace\\LabView\\temperatureFig.jpg')
    plt.show()
    plt.close()

"""Print metadata from edf-files:"""
def printFolderMotors(DataFolder):
    """
    This function prints certain header entries from the files in the specified folder. The files are intended to be edf-files from ESRF ID06. No failsafe is implemented.

    DataFolder:
        String/path. The folder in which to find the files whose header elements should be printed.
    """
    FileNames = namesFromFolder(DataFolder)
    for index in range(len(FileNames)):
        File = fabio.open(DataFolder + '\\' + FileNames[index])
        print(FileNames[index],
              '\tchi:', getMotorValue(File.header, 'chi'),
              '\t', 'diffry', getMotorValue(File.header, 'diffry'),
              '\t', 'ffz', getMotorValue(File.header, 'ffz'),
              '\t', 'obz', getMotorValue(File.header, 'obz'),
              '\t', 'obpitch', getMotorValue(File.header, 'obpitch'),
              '\t', 'run', File.header['run'])
        File.close()
def printHeaderChange(Headers):
    """
    This function prints the motors that have moved, found with getMovedMotors(), between each of the files whose headers are in Headers. For the 'zapline-diffry' ScanType, as given by getScanType(), some other info is also printed for testing purposes.

    Headers:
        List of dictionary. Contains the headers of edf-files from ESRF.
    """
    StringToPrint = ''  # Fill in later
    for index, header in enumerate(Headers):
        if getScanType(header) == 'zapline-diffry':
            StringToPrint += 'Image: ' + header['Image']
            StringToPrint += '; acq_frame_nb: ' +\
                header['acq_frame_nb']
            StringToPrint += '; scan: ' + header['scan']
        if index > 0:
            StringToPrint += '; motor_pos change: '
            MovedMotors = getMovedMotors(header, Headers[index-1])
            for motor in MovedMotors:
                StringToPrint += motor[0] + ' '
                StringToPrint += motor[1] + '; '
        StringToPrint += '\n'
    print(StringToPrint)

"""Save functions:"""
def saveAs(File, DataType, SaveFolder, FileName, pngCpr=0,
           BitDepth=16, Size=None):
    """
    This function saves a fabio.image as a grayscale image file of the selcted format. It is intended for edf-files from ESRF ID06.

    File:
        fabio.image. Image to save.
    DataType:
         String. Data type to store image as. Allowed formats are 'tiff' and 'png', which are saved with the PIL.image and png modules, respectively. To allow other data types to be saved, modify the DataType comparisons and check that PIL or png supports the format, or add another module that does (remember possibly different scaling of the raw data). '.<DataType>' is appended to the filename of the saved file.
    SaveFolder:
        String/path. Folder/directory in which to save the file.
    FileName:
        String. Contains the filename(without directory) of the file to open. Based on this, a new filename is made with getNewFileName(), which is used for the saved file.
    pngCpr:
        int. Compression level used when saving as png. Allowed values from 0 to 9. 0 means no compression and 9 means the most compression (more time consuming).
    BitDepth:
        int. Bith depth used when saving png. 16 matches raw data edf-files from ESRF ID06. Allowed values are 1, 2, 4, 8 and 16.
    Size:
        tuple: (width, height). Only for saving png-images. If given (not None), image width and height will be reduced to these values (if larger originally) in the saved image.
    newFileName:
        String. Name of the saved file (without folders). Found with getNewFileName(), and then has '.<DataType>' as a suffix.
    """
    try:
        if DataType not in ['tiff', 'png']:
            raise MyException('Invalid DataType')
    except MyException as e:
        print(e)
        print('No file saved')
        return None
    else:
        newFileName = getNewFileName(FileName, File.header) +\
            '.'+DataType
        if newFileName == None:
            return None
        if DataType == 'tiff':
            im = Image.fromarray(File.data/File.getmax())
            im.save(SaveFolder + '\\' + newFileName)
            im.close()
        elif DataType == 'png':
            CurrentWidth = int(File.header['Dim_1'])
            CurrentHeight = int(File.header['Dim_2'])
            if Size != None and Size[0] < CurrentWidth:
                Width = Size[0]
            else:
                Width = CurrentWidth
            if Size != None and Size[1] < CurrentHeight:
                Height = Size[1]
            else:
                Height = CurrentHeight
            pngWriter = png.Writer(
                width=Width,
                height=Height,
                greyscale=True,
                bitdepth=BitDepth,
                compression=pngCpr)
            if Size != None:
                if Size[0] < CurrentWidth or Size[1] < CurrentHeight:
                    pngImage = Image.fromarray(File.data)
                    pngImage = pngImage.resize(Size)
                    DataArray = np.array(pngImage)
                else:
                    DataArray = File.data
            else:
                DataArray = File.data
            pngArray = ((DataArray/np.amax(DataArray)) *
                        (2**pngWriter.bitdepth-1)).astype(int)
            OpenFile = open((SaveFolder + '\\' + newFileName),
                            mode='wb')
            pngWriter.write(OpenFile, pngArray)
            OpenFile.close()
        print('File saved with PIL.Image (Normalized to %.0f): ' %
              np.amax(pngArray) + SaveFolder + '\\' + newFileName)
        return newFileName
def saveFolder(OriginalFolder, DataType, BitDepth=16, pngCpr=0,
               DataTypeToRead='edf', TargetFolder=None,
               PathToRemove='', Size=None):
    """
    This function opens files from a whole folder as fabio.image objects and saves them as grayscale image files of the selcted format, using saveAs(). It is intended for edf-files from ESRF ID06. Files will be saved in the same folder branch as the original data, except the tailmost folder will be a separate one, given the name of the original folder with a suffix indicating the file type and compression level (if any) (for instance 'myFolder/data/OldFileName.edf' -> 'myFolder/data_png_Cmpr2/NewFileName.png').

    OriginalFolder:
        String/path. Folder in which to read files from.
    DataType:
         String. Data type to store images as. Allowed formats are 'tiff' and 'png', which are saved with the PIL.image and png modules, respectively. To allow other data types to be saved, modify the DataType comparisons and check that PIL or png supports the format, or add another module that does (remember possibly different scaling of the raw data).
    BitDepth:
        int. Bith depth used when saving png. 16 matches raw data edf-files from ESRF ID06. Allowed values are 1, 2, 4, 8 and 16.
    pngCpr:
        int. Compression level used when saving as png. Allowed values from 0 to 9. 0 means no compression and 9 means the most compression (more time consuming).
    DataTypeToRead:
        String. Data type to open in OriginalFolder. Files with names not ending with <DataTypeToRead> are not opened or saved. The only tested type is edf from ESRF ID06.
    TargetFolder:
        String/path. If given (not None), files will be saved in this folder, with the same sub-folder structure as the original data. PathToRemove must in this case also be given.
    PathToRemove:
        String/path. If TargetFolder is given (not None), PathToRemove is removed from the root end of the original data's folder branch before this truncated path is appended to TargetFolder to give the new total path in which to save the new file. In other words, PathToRemove denotes the part of the original data's folder branch not to be considered as the branch structure to preserve.
    Size:
        tuple: (width, height). Only for saving png-images. If given (not None), image width and height will be reduced to these values (if larger originally) in the saved image, and target entered <Width>x<Height> is given in the new leaf-level folder and in within TargetFolder (if given).
    """
    try:
        if DataType not in ['tiff', 'png']:
            raise MyException('Invalid DataType')
    except MyException as e:
        print(e)
    else:
        DataFolderConvert = path.normpath(OriginalFolder + '_' +
                                          DataType + str(BitDepth))
        ModString = ''
        if pngCpr != 0:
            ModString += '_Cmpr%i' % pngCpr
        if Size != None:
            ModString += '_%ix%i' % (Size[0], Size[1])
        DataFolderConvert += ModString
        if TargetFolder != None:
            NewPathRoot = path.join(path.normpath(TargetFolder),
                                    DataType + str(BitDepth))
            NewPathRoot += ModString
            NewPathTail = DataFolderConvert[len(PathToRemove):]
            DataFolderConvert = path.join(NewPathRoot, NewPathTail)
        if not path.exists(DataFolderConvert):
            makedirs(DataFolderConvert)
        FileNames = namesFromFolder(OriginalFolder,
                                    DataType=DataTypeToRead)
        for index in range(len(FileNames)):
            File = fabio.open(OriginalFolder + '\\' + FileNames[index])
            print('File loaded with fabio: ' + OriginalFolder + '\\' +
                  FileNames[index])
            newFileName = saveAs(File, DataType, DataFolderConvert,
                                 FileNames[index], pngCpr=pngCpr,
                                 BitDepth=BitDepth, Size=Size)
            File.close()
def getAllFoldersJune2018(DriveLetter='D'):
    """
    This function returns a list of all folders/paths with data from Magnus Christensen's ESRF ID06 beamtime June 2018, as put on a harddrive on port D. Change D as appropriate if the harddrive is changed.

    DriveLetter:
        String. The letter of the harddrive currently in use.
    Directories:
        List of string. Contains all ESRF ID06 June 2018 data folders of Magnus Christensen.
    """

    # To be added later to the left side of Directories below
    RootPath = DriveLetter +\
        ':\\ESRF June 2018\\hxrm_2018-06-20_magnus\\'

    #  108 folders, root excluded (which is RootPath above)
    Directories = [
    '7_2\\nf\\casting_1',
    '7_2\\nf\\casting_2',
    '7_2\\nf\\casting_3',
    '10_1_3\\diff\\cooling_from_590',
    '10_1_3\\diff\\heating_from_540',
    '10_1_3\\diff\\rocking_saturday_552_up',
    '10_1_3\\ff\\ff_rocking_step1',
    '10_1_3\\ff\\obfoc_saturday_552',
    '10_1_3\\nf\\casting_1',
    '10_1_3\\nf\\casting_2',
    '10_1_3\\nf\\casting_3',
    '10_1_3\\nf\\casting_4',
    '10_1_3\\nf\\mosa_2_saturday_548',
    '10_1_3\\nf\\mosa_2_saturday_550',
    '10_1_3\\nf\\mosa_2_saturday_552',
    '10_1_3\\nf\\mosa_2_saturday_552_up',
    '10_1_3\\nf\\mosa_3_saturday_548',
    '10_1_3\\nf\\mosa_3_saturday_552',
    '10_1_3\\nf\\mosa_4_saturday_548',
    '10_1_3\\nf\\mosa_saturday_540',
    '10_1_3\\nf\\mosa_saturday_546',
    '10_1_3\\nf\\mosa_saturday_548',
    '10_1_3\\nf\\mosa_saturday_550',
    '10_1_3\\nf\\mosa_saturday_552',
    '10_1_3\\nf\\mosa_saturday_552_up',
    '10_1_3\\nf\\obfoc1',
    '10_1_3\\nf\\rocking_2_saturday_546',
    '10_1_3\\nf\\rocking_2_saturday_548',
    '10_1_3\\nf\\rocking_ff_2_saturday_552_up',
    '10_1_3\\nf\\rocking_ff_saturday_552_up',
    '10_1_3\\nf\\rocking_grain1_551C',
    '10_1_3\\nf\\rocking_grain1_555C',
    '10_1_3\\nf\\rocking_saturday_540',
    '10_1_3\\nf\\rocking_saturday_546',
    '10_1_3\\nf\\rocking_saturday_550',
    '10_1_3\\nf\\rocking_saturday_552',
    '10_1_3\\nf\\rocking_saturday_fine_550',
    '10_1_3\\nf\\rocking_saturday_radiography_540',
    '10_1_3\\nf\\rocking_saturday_radiography_546',
    '10_1_3\\nf\\rocking_saturdaY_radiography_548',
    '10_1_3\\nf\\rocking_saturday_radiography_550',
    '10_1_3\\nf\\rocking_saturday_radiography_552',
    '10_1_3\\nf\\rocking_saturday_radiography_552_up',
    '10_1_3\\nf\\rocking2_grain1_555C',
    '10_1_3\\nf\\snaps',
    '10_1_3\\nf\\strain_3_saturday_552',
    '10_1_3\\nf\\strain_saturday_540',
    '10_1_3\\nf\\strain_saturday_546',
    '10_1_3\\nf\\strain_saturday_548',
    '10_1_3\\nf\\strain_saturday_550',
    '10_1_3\\nf\\strain_saturday_552',
    '10_1_3\\nf\\timescan_ff_saturday_552_up',
    '10_1_5\\ff\\bg_1s',
    '10_1_5\\ff\\magnification',
    '10_1_5\\ff\\mosa_scan',
    '10_1_5\\ff\\mosa_scan2_530C',
    '10_1_5\\ff\\obfoc',
    '10_1_5\\ff\\obfoc2',
    '10_1_5\\ff\\obfoc3_530C',
    '10_1_5\\ff\\strain_scan',
    '10_1_5\\ff\\strain_scan2_530C',
    '10_1_5\\nf\\mosa_scan_555C',
    '10_1_5\\nf\\ramp_from_530',
    '10_1_5\\nf\\ramp_from_554to555C',
    '10_1_5\\nf\\snaps',
    '10_1_5\\nf\\strain_scan_555C',
    '10_1_5\\nf',
    '10_1_5\\RampTracing\\mosa_530C',
    '10_1_5\\RampTracing\\obfoc_2_530C',
    '10_1_5\\RampTracing\\obfoc_530C',
    'cooling_10_1_5\\ff\\mosa_546',
    'cooling_10_1_5\\ff\\mosa_553',
    'cooling_10_1_5\\ff\\mosa_590C',
    'cooling_10_1_5\\ff\\mosa_zap_590C',
    'cooling_10_1_5\\ff\\obfoc',
    'cooling_10_1_5\\ff\\obfoc_553',
    'cooling_10_1_5\\ff\\rocking_553',
    'cooling_10_1_5\\ff\\rocking_590C',
    'cooling_10_1_5\\ff\\strain_546',
    'cooling_10_1_5\\ff\\strain_553',
    'cooling_10_1_5\\ff\\test',
    'cooling_10_1_5\\nf\\diff_rocking_2_553',
    'cooling_10_1_5\\nf\\diff_rocking_2_600',
    'cooling_10_1_5\\nf\\diff_rocking_2_610',
    'cooling_10_1_5\\nf\\diff_rocking_3_600',
    'cooling_10_1_5\\nf\\diff_rocking_553',
    'cooling_10_1_5\\nf\\diff_rocking_560',
    'cooling_10_1_5\\nf\\diff_rocking_565',
    'cooling_10_1_5\\nf\\diff_rocking_575',
    'cooling_10_1_5\\nf\\diff_rocking_580',
    'cooling_10_1_5\\nf\\diff_rocking_585',
    'cooling_10_1_5\\nf\\diff_rocking_590',
    'cooling_10_1_5\\nf\\diff_rocking_595',
    'cooling_10_1_5\\nf\\diff_rocking_600',
    'cooling_10_1_5\\nf\\diff_rocking_605',
    'cooling_10_1_5\\nf\\diff_rocking_610',
    'cooling_10_1_5\\nf\\direct_553',
    'cooling_10_1_5\\nf\\direct_560',
    'cooling_10_1_5\\nf\\direct_565',
    'cooling_10_1_5\\nf\\direct_575',
    'cooling_10_1_5\\nf\\direct_580',
    'cooling_10_1_5\\nf\\direct_585',
    'cooling_10_1_5\\nf\\direct_590',
    'cooling_10_1_5\\nf\\direct_595',
    'cooling_10_1_5\\nf\\direct_600',
    'cooling_10_1_5\\nf\\direct_605',
    'cooling_10_1_5\\nf\\direct_610',
    'cooling_10_1_5\\nf\\timescan_575'
    ]

    for Index in range(len(Directories)):
        Directories[Index] = RootPath + Directories[Index]

    return Directories
def convertAllJune2018(DataType='png', pngCpr=1, BitDepth=16,
                       TargetFolder='F:\\ESRF June 2018',
                       DriveLetter='F', Size=None):
    """
    This function converts all of Magnus Christensen's ESRF ID06 June 2018 beamtime edf data files by performs saveFolder() on all folders returned by getAllFoldersJune2018(). It is intended for edf-files from ESRF ID06. Files will be saved in the same folder branch as the original data, except the tailmost folder will be a separate one, given the name of the original folder with a suffix indicating the file type and compression level (if any) (for instance 'myFolder/data/OldFileName.edf' -> 'myFolder/data_png_Cmpr2/NewFileName.png').

    DataType:
         String. Data type to store images as. Allowed formats are 'tiff' and 'png', which are saved with the PIL.image and png modules, respectively. To allow other data types to be saved, modify saveFolder() and saveAs().
    pngCpr:
        int. Compression level used when saving as png. Allowed values from 0 to 9. 0 means no compression and 9 means the most compression (more time consuming).
    BitDepth:
        int. Bith depth used when saving png. 16 matches raw data edf-files from ESRF ID06. Allowed values are 1, 2, 4, 8 and 16.
    TargetFolder:
        String/path. If not None, files will be saved in this folder, with the same sub-folder structure as the original data. PathToRemove is in this case removed from the root end of the original data's folder branch before this truncated path is appended to TargetFolder to give the new total path in which to save the new file. In other words, PathToRemove denotes the part of the original data's folder branch not to be considered as the branch structure to preserve. Remember to give the correct drive letter.
    DriveLetter:
        String. Drive letter of current harddrive, passed to getAllFoldersJune2018() to get the folders of the original data.
    Size:
        tuple: (width, height). Only for saving png-images. If given (not None), image width and height will be reduced to these values (if larger originally) in the saved image.
    """

    """ Not used if TargetFolder is None. Only its length is used when removing it, so the drive letter used is unimportant."""
    PathToRemove = 'D:\\ESRF June 2018\\hxrm_2018-06-20_magnus\\'

    directories = getAllFoldersJune2018(DriveLetter=DriveLetter)
    for directory in directories:
        Folder = path.normpath(directory)
        saveFolder(Folder, DataType, pngCpr=pngCpr,
                   TargetFolder=TargetFolder,
                   PathToRemove=PathToRemove, BitDepth=BitDepth,
                   Size=Size)

"""ImageBrowser functions:"""
def ChangeImage(root, ParamNbr=None, Direction=None, StartIndex=0):
    """
    This function adds/changes some attributes to/of root, incuding a widget that displays the first image found in root.FileNames. It can be used to change the displayed image to an adjacent step of the same scan (in the context of edf-files from ESRF ID06).

    root:
        Tk toplevel widget window with at least these attributes:
        ImageShape: Shape (width, height) of image displayed.
        Directory:  Path/string of folder to open files from.
        FileNames:  Names of files in Directory.
        ImageFrame: Frame widget to show image in.
    ParamNbr:
        int. This gives the direction along which to move in a scan when opening next image; 0 to move to next/previous image of the first parameter in the filename, and 1 to move along the second parameter, as given by getNextFileIndex().
    Direction:
        String. Either 'up' to increase or 'down' to decrease the parameter given by ParamNbr. If None (default), root is setup for showing an image (the first in root.FileNames) for the first time.
    """

    if Direction == None:
        # Index of the currently (first) displayed image
        root.CurrentIndex = StartIndex
        # Label widget that displays the image, store in root
        root.PhotoWidget = tk.Label(root.ImageFrame)
    else:
        NextIndex = getNextFileIndex(root, ParamNbr=ParamNbr,
                                     Direction=Direction)
        if NextIndex != None:
            # New image found in the desired direction
            root.CurrentIndex = NextIndex
            # Filename of currently displayed file, store in root.
            root.FileName = root.FileNames[root.CurrentIndex]
            # Nbr. of dimensions in scan.
            root.ScanDimensions = getScanTypeFromName(root.FileName)[3]
            for button in root.Buttons:
                button.destroy()
            ButtonDirections = ['up', 'down']
            for n in range(root.ScanDimensions):
                for d in ButtonDirections:
                    button = tk.Button(root.ControlFrame,
                                       text=d + str(n),
                                       font='16',
                                       command=lambda d=d, n=n: ChangeImage(
                                           root, n, d))
                    button.pack()
                    root.Buttons.append(button)
        else:
            # No image found in that direction
            return

    # Filename of currently displayed file, store in root.
    root.FileName = root.FileNames[root.CurrentIndex]
    # Path of currently displayed file, store in root.
    root.FilePath = path.join(root.Directory, root.FileName)
    # Intermediary Image object
    ImageObject = Image.open(root.FilePath).resize(root.ImageShape)
    print(ImageObject)
    # Photo to display, store in root.
    root.Photo = ImageTk.PhotoImage(ImageObject, master=root)
    # Put the image in the Label widget.
    root.PhotoWidget.configure(image=root.Photo)
    # Fit the Label widget around the image
    root.PhotoWidget.pack()
    # Change window title to show name of displayed file
    root.title('Image browser ' + ' %s' % root.FileName)
    print('Current file: %s' % root.FileName)
def getScanTypeFromName(FileName):
    """
    This function returns a scan type based on a filename. This is intended to use on png-files converted from edf-files from ESRF ID06. FileName must be of the structure given by getNewFileName(). This function is in some ways the inverse of getNewFileName() in that getNewFileName() gives a filename basen on a scan type, while this function gives the scan type based on the filename. There is no differentiation between timescan and loopscan, or between mosaicity and zapimage-mosaicity, or strain and rocking. Rocking is called strain in getNewFileName() also.

    FileName:
        String. Filename to find scan type from. Should be of the form created by getNewFileName() (and only contain '-' directly before the scan step part).
    ScanType:
        String. Representing different scan types from ESRF ID06.
    OtherParams:
        List. Contains indices of scan info elements in FileName.
    NoName:
        Boolean. True if FileName is nameless, here meaning containing no '-'. This is the case, according to the method of getNewFileName(), for filenames without a scan type (with scan type 'none') or files with only scan info in their names. The latter case is what is intended to be passed with this parameter.
    NScans
        Int. Number of dimensions across which the scan is taken (eg. two for strain and one for timescan).
    """

    """ Find the starting index of the part of FileName which contains the scan step(s). If not found, -1 is returned, hence LeftLimit + 1 = 0. This works out if the filename starts with the scan step (without '-', as might be produced by getNewFileName())."""
    LeftLimit = FileName.find('-')
    if LeftLimit == -1:
        NoName = True
    else:
        NoName = False
    # Find the end of the scan step part of FileName.
    RightLimit = FileName.find('.')
    """ Found in mosaicity, strain, zapline-diffry and zapimage-mosaicity."""
    DIndex = FileName.find('D', LeftLimit+1, RightLimit)
    # Found in mosaicity and zapimage-mosaicity.
    CIndex = FileName.find('C', LeftLimit+1, RightLimit)
    # Found in strain and obfoc.
    OIndex = FileName.find('O', LeftLimit+1, RightLimit)
    # Found in timescan and loopscan.
    TIndex = FileName.find('T', LeftLimit+1, RightLimit)
    # Found in diffty.
    YIndex = FileName.find('Y', LeftLimit+1, RightLimit)
    if DIndex != -1 and CIndex != -1:
        ScanType = 'mosaicity'  # or 'zapimage-mosaicity'
        OtherParams = [DIndex, CIndex, RightLimit]
    elif DIndex != -1 and OIndex != -1:
        ScanType = 'strain'  # or rocking scan
        OtherParams = [DIndex, OIndex, RightLimit]
    elif DIndex != -1 and TIndex != -1:
        ScanType = 'zapline-diffry'
        OtherParams = [DIndex, TIndex, RightLimit]
    elif TIndex != -1:
        # Case of zapline-diffry scan tested above.
        ScanType = 'timescan'  # or 'loopscan'
        OtherParams = [TIndex, RightLimit]
    elif OIndex != -1:
        # Case of strain scan tested above.
        ScanType = 'obfoc'
        # Find if 'x', 'y' or 'z' follows 'O'.
        xIndex = FileName.find('x', OIndex+1, RightLimit)
        yIndex = FileName.find('y', OIndex+1, RightLimit)
        zIndex = FileName.find('z', OIndex+1, RightLimit)
        # Find index of the last of 'x','y' and 'z'
        NLetters = (xIndex != -1) + (yIndex != -1) + (zIndex != -1)
        OtherParams = [OIndex + NLetters, RightLimit, OIndex]
    elif YIndex != -1:
        ScanType = 'diffty'
        OtherParams = [YIndex, RightLimit]
    else:
        ScanType = None
        OtherParams = []

    if ScanType == 'obfoc':
        NScans = len(OtherParams)-2
    elif ScanType == None:
        NScans = len(OtherParams)+1
    else:
        NScans = len(OtherParams)-1

    return ScanType, OtherParams, NoName, NScans
def getNextFileIndex(root, ParamNbr=0, Direction='up'):
    """
    This function returns the index of the next image in root.FileNames when moving along a certain scan direction. It is intended for png-files converted from edf-files from ESRF ID06. ScanType is found from getScanTypeFromName(), which is used to find which part of the current root.FileName that is the scan location to increase/decrease to get the filename of the next image to display.

    root:
        Tk toplevel widget window with at least these attributes:
        FileNames:  Names of files in root.Directory to browse.
        FileName:   Name of currently displayed file.
    ParamNbr:
        int. This gives the direction along which to move in a scan when opening next image; 0 to move to next/previous image of the first parameter in the filename, and 1 to move along the second parameter, as given by getNextFileIndex(). 1 (or otherwise not 0) should not be given if getScanTypeFromName() gives scan information with only one scan parameter.
    Direction:
        String. Either 'up' to increase or 'down' to decrease the parameter given by ParamNbr. If None (default), root is setup for showing an image (the first in root.FileNames) for the first time.
    NextFileIndex:
        int. Index of next image along the specified direction.
    """

    File = root.FileName  # For easier read below.
    ScanType, OtherParams, NoName, NScans = getScanTypeFromName(File)
    # Nbr of scan parameters in this ScanType.
    NPrms = len(OtherParams)  # For easier read below.
    if ScanType == 'obfoc':
        # One extra parameter given in OtherParams, not to be counted.
        NPrms -= 1
        # Get the extra parameter.
        OIndex = OtherParams[2]

    if ScanType == None:
        # If no scan type, return next file alphabetically.

        Index = root.CurrentIndex  # For easier read below.
        NFiles = len(root.FileNames)  # For easier read below.
        if Index >= NFiles - 1 and Direction == 'up':
            # No file later alphabetically exists.
            return None
        elif Index <= 0 and Direction == 'down':
            # No file earlier alphabetically exists.
            return None
        elif Direction == 'up':
            # Return index of next file alphabetically.
            return Index + 1
        elif Direction == 'down':
            # Return index of previous file alphabetically.
            return Index - 1
        else:
            print('Direction not valid')
            return None

    if NPrms in [2, 3]:
        """ If scan type is not None, 2 or 3 parameters should be given in OtherParams. If so, find next file index according to the parameter (ParamNbr) and direction (Direction) specified."""

        # Get indices of parameter letter(s) in filename.
        PrmInds = OtherParams[0:NPrms-1]
        # Get index of '.' in filename (after parameter letters).
        EndInd = OtherParams[NPrms-1]

        Prms = []  # Fill in later
        Vals = []  # Fill in later

        for Ind in range(NPrms-1):
            Prms.append(File[PrmInds[Ind]])
            Vals.append(File[OtherParams[Ind]+1:OtherParams[Ind+1]])

        if Direction == 'up':
            Vals[ParamNbr] = str(int(Vals[ParamNbr])+1)
        elif Direction == 'down':
            Vals[ParamNbr] = str(int(Vals[ParamNbr])-1)
        else:
            print('Direction not valid')
            return None

        # Build new filename.
        if NoName == True:
            NewFileNameEnd = ''
        else:
            NewFileNameEnd = '-'
        if ScanType == 'obfoc':
            """ Account for more than one letter in scan parameter. Using PrmInds[0] in this case gives instead the index of 'x', 'y' or 'z' after 'O'."""
            NameEndInd = OIndex  # Index of 'O'
            NewFileNameEnd += File[OIndex:PrmInds[0]]
        else:
            NameEndInd = PrmInds[0]
        for Ind in range(NPrms-1):
            NewFileNameEnd += Prms[Ind] + Vals[Ind]
        NewFileNameEnd += File[EndInd:]
        NewFileName = File[0:NameEndInd-1] + NewFileNameEnd

        try:
            # Check if exact (new) filename is found in root.FileNames.
            Index = root.FileNames.index(NewFileName)
        except ValueError:
            # If NewFileName not found, search only for end of name.
            for Index, File in enumerate(root.FileNames):
                if File.endswith(NewFileNameEnd):
                    return Index
        else:
            # Exact filename found at root.FileNames[Index]
            return Index
    else:
        # Unexpected return from getScanTypeFromName().
        print('ScanType not recognized')
        return None
def imageBrowser(DataType='png', DataFolder=None,
                 ImageShape=(700, 700), StartIndex=0):
    """
    This function opens a file from a folder - specified by a user prompt - and displays it with the oportunity to flip through images (within the folder) in the direction of increasing or decreasing scan step as given in the filename which is assumed to be of the form made by getNewFileName(). This is intended for png-files converted from edf-files from ESRF ID06. It does not work on 16-bit png-images.

    DataType:
        String. If specified (not None), only files with names ending with <DataType> are included, otherwise all files are included.
    DataFolder:
        String/path. If given (not None), this will be the folder whose files are browsed, and no user prompt occurs.
    ImageShape:
        Tuple with 2 elements. Width and height in pixels of the image shown.
    """

    # Create toplevel window.
    root = tk.Tk()
    # Store ImageShape in root
    root.ImageShape = ImageShape

    # Get folder to open files from, and store in root.
    if DataFolder == None:
        # Get folder from user input.
        root.Directory = path.normpath(askdirectory())
    else:
        # Get folder from function parameter
        root.Directory = path.normpath(DataFolder)

    # Store list of files in root
    root.FileNames = namesFromFolder(root.Directory, DataType=DataType)

    # Frame widget to show buttons/controls on, store in root
    root.ControlFrame = tk.Frame(root)
    root.ControlFrame.grid(row=0, column=0)  # Left window column
    # Frame widget to show image on, store in root
    root.ImageFrame = tk.Frame(root)
    root.ImageFrame.grid(row=0, column=1)  # Right window column

    # Displayed the first image in the folder (alphabetically).
    ChangeImage(root, StartIndex=StartIndex)
    # Nbr. of dimensions in scan.
    root.ScanDimensions = getScanTypeFromName(root.FileName)[3]

    # Create list of buttons in root
    root.Buttons = []  # Fill in later
    ButtonDirections = ['up', 'down']
    for n in range(root.ScanDimensions):
        for d in ButtonDirections:
            button = tk.Button(root.ControlFrame,
                               text=d + str(n),
                               font='16',
                               command=lambda d=d, n=n: ChangeImage(
                                   root, n, d))
            button.pack()
            root.Buttons.append(button)

    # Run the interface
    root.mainloop()

"""Testing functions:"""
def TestAllFolders():
    Folders = getAllFoldersJune2018(DriveLetter='D')
    for Folder in Folders:
        File, FileName = loadFile(Folder, DataType='edf', Mute=True)
        if File.header['DataType']!='UnsignedShort':
            print(Folder, 'DataType', File.header['DataType'])
        if File.header['Dim_1']!='2048':
            print(Folder, 'Dim_1', File.header['Dim_1'])
        File.close()
def TestAllFolders2():
    Folders = getAllFoldersJune2018(DriveLetter='F')
    for Folder in Folders:
        File, FileName = loadFile(Folder, DataType='edf', Mute=True)
        print(Folder[41:], 'ScanType:', getScanType(File.header))
        File.close()
"""Sandbox:"""
def doStuff():
    """
    This function is just a sandbox to do whatever.
    """
    # imageBrowser()
    # TestAllFolders2()
    # plotAllTemperatures()
    # FilePath = path.normpath(
    #     '\\\\home.ansatt.ntnu.no\\Magnussc\\Documents\\PhD\\Furnace\\LabView\\2018-06-18_Temperature_data.txt')
    # print(getTemperaturesFromFile(FilePath)[0:3])
    # printAllFolderDates()

    # convertAllJune2018(DataType='png', pngCpr=1, BitDepth=4, TargetFolder='D:\\ESRF June 2018', DriveLetter='D', Size=(256,256))

    # # 1D scan
    # Folder1 = 'D:\\ESRF June 2018\\png16_Cmpr1\\7_2\\nf\\casting_1_png16_Cmpr1'
    # # 2D scan
    # Folder2 = 'D:\\ESRF June 2018\\png16_Cmpr1\\cooling_10_1_5\\ff\\strain_553_png16_Cmpr1'
    # # Obfoc
    # Folder3 = 'D:\\ESRF June 2018\\png16_Cmpr1\\10_1_3\\ff\\obfoc_saturday_552_png16_Cmpr1'
    # Folder4 = 'D:\\ESRF June 2018\\png16_Cmpr1\\10_1_3\\nf\\obfoc1_png16_Cmpr1'
    # # NoName
    # Folder5 = 'D:\\ESRF June 2018\\png16_Cmpr1\\10_1_5\\nf_png16_Cmpr1'
    # # NoScan
    # Folder6 = 'D:\\ESRF June 2018\\png16_Cmpr1\\10_1_3\\nf\\snaps_png16_Cmpr1'
    # # 512 x 512
    # Folder7 = 'D:\\ESRF June 2018\\png16_Cmpr1\\10_1_3\\ff\\ff_rocking_step1_png16_Cmpr1'
    # # 8-bit png
    # Folder8 = '\\\\home.ansatt.ntnu.no\\Magnussc\\Documents\\PhD\\Experimental Data\\strain_553_png_Cmpr1_skin'
    # # 4 bit, 256x256
    # Folder9 = 'D:\\ESRF June 2018\\png4_Cmpr1_256x256\\7_2\\nf\\casting_1_png4_Cmpr1_256x256'
    # imageBrowser(DataFolder=Folder9, ImageShape=(300,300), StartIndex=0)

    """ FIX SUCH THAT IMAGES ARE DISPLAYED, NOT ALL WHITE
    """

    """ FIX rocking scan to show 1 pair of buttons?
    """

    """ CHECK IF ALL IMAGES ARE 16 BIT FROM ESRF.
    """
    # TestAllFolders()
    return
doStuff()

""" New functions """
def make_data_array(file_list):
    # Convert background images from list of fabio.image to numpy.array
    rows_in_image = np.shape(file_list[0].data)[0]
    cols_in_image = np.shape(file_list[0].data)[1]
    files_loaded = len(file_list)
    array = np.zeros((rows_in_image, cols_in_image, files_loaded))
    for image in range(files_loaded):
        array[:,:,image] = file_list[image].data
    return array