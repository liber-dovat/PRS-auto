#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import matplotlib
import netCDF4

from os       import listdir
from shutil   import copyfile

# http://scipy-cookbook.readthedocs.io/items/Matplotlib_Loading_a_colormap_dynamically.html
def gmtColormap(fileName,GMTPath = None, segmentos = 1024):
  import colorsys
  import numpy
  N = numpy
  if type(GMTPath) == type(None):
      filePath = "/usr/local/cmaps/"+ fileName+".cpt"
  else:
      filePath = GMTPath+"/"+ fileName +".cpt"
  try:
      f = open(filePath)
  except:
      print( "file " + filePath + "not found")
      return None

  lines = f.readlines()
  f.close()

  x = []
  r = []
  g = []
  b = []
  colorModel = "RGB"
  for l in lines:
      ls = l.split()
      if l[0] == "#":
         if ls[-1] == "HSV":
             colorModel = "HSV"
             continue
         else:
             continue
      if ls[0] == "B" or ls[0] == "F" or ls[0] == "N":
         pass
      else:
          x.append(float(ls[0]))
          r.append(float(ls[1]))
          g.append(float(ls[2]))
          b.append(float(ls[3]))
          xtemp = float(ls[4])
          rtemp = float(ls[5])
          gtemp = float(ls[6])
          btemp = float(ls[7])

  x.append(xtemp)
  r.append(rtemp)
  g.append(gtemp)
  b.append(btemp)

  nTable = len(r)
  x = N.array( x , N.float)
  r = N.array( r , N.float)
  g = N.array( g , N.float)
  b = N.array( b , N.float)
  if colorModel == "HSV":
     for i in range(r.shape[0]):
         rr,gg,bb = colorsys.hsv_to_rgb(r[i]/360.,g[i],b[i])
         r[i] = rr ; g[i] = gg ; b[i] = bb
  if colorModel == "HSV":
     for i in range(r.shape[0]):
         rr,gg,bb = colorsys.hsv_to_rgb(r[i]/360.,g[i],b[i])
         r[i] = rr ; g[i] = gg ; b[i] = bb
  if colorModel == "RGB":
      r = r/255.
      g = g/255.
      b = b/255.
  xNorm = (x - x[0])/(x[-1] - x[0])

  red = []
  blue = []
  green = []
  for i in range(len(x)):
      red.append([xNorm[i],r[i],r[i]])
      green.append([xNorm[i],g[i],g[i]])
      blue.append([xNorm[i],b[i],b[i]])
  colorDict = {"red":red, "green":green, "blue":blue}
  cwm = matplotlib.colors.LinearSegmentedColormap(fileName, colorDict, segmentos)
  return cwm

# gmtColormap

#########################################
#########################################
#########################################

def ncdump(url, verb=True):
    '''
    http://schubert.atmos.colostate.edu/~cslocum/netcdf_example.html
    ncdump outputs dimensions, variables and their attribute information.
    The information is similar to that of NCAR's ncdump utility.
    ncdump requires a valid instance of Dataset.

    Parameters
    ----------
    nc_fid : netCDF4.Dataset
        A netCDF4 dateset object
    verb : Boolean
        whether or not nc_attrs, nc_dims, and nc_vars are printed

    Returns
    -------
    nc_attrs : list
        A Python list of the NetCDF file global attributes
    nc_dims : list
        A Python list of the NetCDF file dimensions
    nc_vars : list
        A Python list of the NetCDF file variables
    '''
    def print_ncattr(key):
        """
        Prints the NetCDF file attributes for a given key

        Parameters
        ----------
        key : unicode
            a valid netCDF4.Dataset.variables key
        """
        try:
            print("\t\ttype:" + repr(nc_fid.variables[key].dtype))
            for ncattr in nc_fid.variables[key].ncattrs():
                print('\t\t%s:' % ncattr, repr(nc_fid.variables[key].getncattr(ncattr)))
        except KeyError:
            print("\t\tWARNING: %s does not contain variable attributes" % key)
    # def print_ncattr

    # NetCDF global attributes
    nc_fid   = netCDF4.Dataset(url, 'r', format="NETCDF4")
    nc_attrs = nc_fid.ncattrs()
    if verb:
        print("NetCDF Global Attributes:")
        for nc_attr in nc_attrs:
            print('\t%s:' % nc_attr, repr(nc_fid.getncattr(nc_attr)))
    nc_dims = [dim for dim in nc_fid.dimensions]  # list of nc dimensions

    # Dimension shape information.
    if verb:
        print("NetCDF dimension information:")
        for dim in nc_dims:
            print("\tName:" + dim )
            print("\t\tsize:" + len(nc_fid.dimensions[dim]))
            print_ncattr(dim)

    # Variable information.
    nc_vars = [var for var in nc_fid.variables]  # list of nc variables
    if verb:
        print("NetCDF variable information:")
        for var in nc_vars:
            if var not in nc_dims:
                print('\tName:', var)
                print("\t\tdimensions:", nc_fid.variables[var].dimensions)
                print("\t\tsize:", nc_fid.variables[var].size)
                print_ncattr(var)
    return nc_attrs, nc_dims, nc_vars

# def ncdump

# ---------------------------------------
# ---------------------------------------
# ---------------------------------------

def copiar_frames(carpeta_base, carpeta_destino):

  # habia usado 92 elems en las pruebas que eran cerca de tres dias
  # tambien se puede pensar que son 88 por dia, 44 normales y 44 con fondo blanco

  dir_elemens = sorted(listdir(carpeta_base))
  indice      = 88
  if len(dir_elemens) < 88:
    indice = len(dir_elemens)

  ultimas = dir_elemens[-indice:]

  i = 0

  for f in ultimas:
    copyfile(carpeta_base + '/' + f, carpeta_destino + '/' + f)
    i += 1

# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
