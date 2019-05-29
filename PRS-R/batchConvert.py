#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import os
import glob

from os.path              import isfile
from os                   import listdir
from multiprocessing      import Process
from threading            import Lock

#####
def llamarScript(scriptpath, filename):

  # subprocess.call("/sat/PRS/dev/PRS-sat/PRSgoes/videoandcopy.sh", shell=True)
  # subprocess.call(["ls", "-l"])
  subprocess.call(scriptpath + " " + filename, shell=True)

# llamarScript

#####
# ART_2018001_001538.RP
# 2018small_OR_ABI-L2-CMIPF-M3C02_G16_s20180010015387_e20180010026154_c20180010026231.nc

#####

programa   = '/sat/PRS/dev/PRS-sat/PRS-R/exec_file.sh'
sourcePath = '/sat/tmp-sat/2018/C02/small/enero/'
filesList = '/sat/PRS/dev/PRS-sat/PRS-R/data/job_imglist_VIS1'

# listing = glob.glob(sourcePath + '' )
files   = sorted(open(filesList,"r").readlines())

print files

mutex = Lock()
processes = []

while len(files)>1:

  print len(files)

  numproc = 30
  if len(files) < numproc:
    numproc = len(files)

  for m in range(0, numproc):
    mutex.acquire() # mutoexcluyo para hacer el pop sin coliciones

    file = files.pop()

    mutex.release() # libero el mutex

    # if not os.path.isfile(pngPath + file[11:] + '.png'):
    p = Process(target=llamarScript, args=(programa, file))
    p.start()
    processes.append(p)
    # if
  # for

  for p in processes:
    p.join()
  # for 

# while
