
from os import listdir

def getLastFile(basedir):

  year     = sorted(listdir(basedir))[-1]
  rootname = sorted(listdir(basedir + year + '/'))[-1]

  return year, rootname[:18]

# getLastFileFRPath
