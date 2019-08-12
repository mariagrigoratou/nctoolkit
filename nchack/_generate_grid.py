
import xarray as xr
import pandas as pd
import numpy as np
import os
import tempfile
import itertools
# function to generate the grid for cdo remapping
from .flatten import str_flatten

def generate_grid(coords):
    grid_type = None
    grid_file = tempfile.NamedTemporaryFile().name
    lon_unique = np.unique(coords.iloc[:,0])
    lat_unique = np.unique(coords.iloc[:,1])
    lon_step = (max(lon_unique) - min(lon_unique)) / (len(lon_unique) - 1)
    lat_step = (max(lat_unique) - min(lat_unique)) / (len(lat_unique) - 1)
    
    if len(lon_unique) == 1:
         lon_step = 0
    if len(lat_unique) == 1:
         lat_step = 0
    x = np.arange(min(lon_unique), max(lon_unique) + lon_step, lon_step)
    y = np.arange(min(lat_unique), max(lat_unique) + lat_step, lat_step)

    if (np.array_equal(x, lon_unique) == False | np.array_equal(y, lat_unique) == False):
         grid_type = "unstructured"

    # now figure out if it is lonlat

    if(len(coords) == (len(x) * len(y))):
        grid_type = "lonlat"
    else:
        grid_type = "unstructured"
    
    # now we need to generate the grid file for cdo
    
    if grid_type == "unstructured":
        x_size = len(coords)
        x_values = str_flatten(coords.iloc[:,0], sep = " ")
        y_values = str_flatten(coords.iloc[:,1], sep = " ")
        f = open(grid_file, 'w')
        f.write("gridtype = unstructured\n")
        f.write("gridsize = " + str(x_size) + "\n")
        f.write("xvals = " + x_values + "\n")
        f.write("yvals = " + y_values)
        f.close()

    if grid_type == "lonlat":
        x_size = len(coords)
        x_values = str_flatten(coords.iloc[:,0], sep = " ")
        y_values = str_flatten(coords.iloc[:,1], sep = " ")
        f = open('mygrid', 'w')
        f.write("gridtype = lonlat\n")
        f.write("xsize = " + str(len(x)) + "\n")
        f.write("ysize = " + str(len(y)) + "\n")
        f.write("xfirst = " + str(min(x)) + "\n")
        f.write("yfirst = " + str(min(y)) + "\n")
        f.write("xinc = " + str(lon_step) +"\n")
        f.write("yinc = " + str(lat_step) +  "\n")
        f.close()
    return(grid_file)

