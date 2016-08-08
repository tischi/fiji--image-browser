#
# Image browser for Fiji
#
# Author information:
# 
# tischitischer@gmail.com
#
# Input: 
# 
# Computation:
#
# Output:
#
#


from ij.io import OpenDialog, DirectoryChooser
from ij.io import Opener
from fiji.util.gui import GenericDialogPlus
from ij.plugin import ZProjector, RGBStackMerge, SubstackMaker, Concatenator
from ij import IJ, ImagePlus, ImageStack, WindowManager
from ij.plugin import Duplicator
from ij.process import StackStatistics
from ij.plugin import ImageCalculator
from ij.measure import ResultsTable
from ij.plugin.frame import RoiManager
import os, os.path, re, sys
from subprocess import Popen, PIPE
from ij.process import ImageConverter
import os, time, shutil, sys, math
from ij.macro import MacroRunner
from ij.gui import Plot

from loci.plugins import BF
from loci.common import Region
from loci.plugins.in import ImporterOptions

from automic.table import TableModel			# this class stores the data for the table
from automic.table import ManualControlFrame 	# this class visualises TableModel via GUI
from java.io import File
from automic.utils.roi import ROIManipulator2D as ROIManipulator

#
#  Functions
#  

def close_all_image_windows():
  # forcefully closes all open images windows
  ids = WindowManager.getIDList();
  if (ids==None):
    return
  for i in ids:
     imp = WindowManager.getImage(i)
     if (imp!=None):
       win = imp.getWindow()
       if (win!=None):
         imp.changes = False # avoids the "save changes" dialog
         win.close()
 
#
# Determine Input Files
#

def get_file_list(foldername, reg_exp):

  print("#\n# Finding files in: "+foldername+"\n#")
  pattern = re.compile(reg_exp)
   
  files = []
  for root, directories, filenames in os.walk(foldername):
	for filename in filenames:
	   #print("Checking:", filename)
	   if filename == "Thumbs.db":
	     continue
	   match = re.search(pattern, filename)
	   if (match == None) or (match.group(1) == None):
	     continue
	   files.append(os.path.join(root, filename))  
	   #print("Valid file: "+str(os.path.join(root, filename)))	   

  return(sorted(files))

#
# GET PARAMETERS
#
def get_parameters(p, num_data_sets):
  gd = GenericDialogPlus("Please enter parameters")

  gd.addMessage("found "+str(num_data_sets)+" data sets")
  
  for k in p.keys():
    if "_file" in k:
      gd.addFileField(k, str(p[k]))		
    elif type(p[k]) == type(""):
      gd.addStringField(k, p[k])
    elif type(p[k]) == type(1):
      gd.addNumericField(k, p[k],0)
    elif type(p[k]) == type(1.0):
      gd.addNumericField(k, p[k],2)
  
  gd.showDialog()
  if gd.wasCanceled():
    return

  for k in p.keys():
    if type(p[k]) == type(""):
      p[k] = gd.getNextString()
    elif type(p[k]) == type(1):
      p[k] = int(gd.getNextNumber())
    elif type(p[k]) == type(1.0):
      p[k] = gd.getNextNumber()
    
  return p

    
if __name__ == '__main__':

  print("#\n# Image browser\n#")

  #
  # Get input folder
  #
  #od = OpenDialog("Select one of the images to be shown", None)
  #input_folder = od.getDirectory()
  dc = DirectoryChooser("Please select a folder.")
  input_folder = dc.getDirectory()
  if input_folder is None:
    sys.exit("No folder selected!")

  print(input_folder)      
  #
  # Determine input files
  #
  tbModel = TableModel(input_folder)
  files = get_file_list(input_folder, '(.*).tif')
  
  #
  # Get parameters
  #
  print("#\n# Parameters\n#")
  
  p = dict()
  
  # channels
  file_names = [f.split(os.path.sep)[-1] for f in files]
  file_endings = [fn.split('--')[-1] for fn in file_names]
  
  p["channels"] = list(set(file_endings))

  #
  # Get parameters
  #
  
  #p = get_parameters(p, len(files))
  #print(p)
  
  #
  # Init interactive table
  #
  
  for ch in p["channels"]:
    tbModel.addFileColumns(ch,'IMG')
   
  sorted_files = sorted(files)
  print("#\n# Image sets to be shown\n#")
  for ch in p["channels"]:
    iDataSet = 0
    for afile in sorted_files:
      if ch in afile.split(os.path.sep)[-1]:
        if ch == p["channels"][0]:
          tbModel.addRow()
        tbModel.setFileAbsolutePath(afile, iDataSet, ch,"IMG")
        print(str(iDataSet)+": "+afile)
        iDataSet = iDataSet + 1

  frame=ManualControlFrame(tbModel)
  frame.setVisible(True)