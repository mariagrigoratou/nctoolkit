import xarray as xr
import pandas as pd
import numpy as np
import os
import tempfile
import itertools

from ._generate_grid import generate_grid
from .flatten import str_flatten
from ._cleanup import cleanup
from ._filetracker import nc_created
from ._runcommand import run_command

def rename(self, newnames, silent = True):
    """Function to rename netcdf variable"""

    if type(newnames) is not dict:
        raise ValueError("a dictionary was not supplied")

    # now, we need to loop through the renaming dictionary to get the cdo sub
    cdo_rename = ""
    
    for key, value in newnames.items():
        cdo_rename +=  "," + key
        cdo_rename += "," + value

    # need a check at this point for file validity     
    target  = tempfile.NamedTemporaryFile().name + ".nc"
    nc_created.append(target)
    cdo_command= ("cdo chname" + cdo_rename + " " + self.current + " " + target)
    self.history.append(cdo_command)
    run_command(cdo_command, self, silent)
        

    if self.run: self.current = target 

    cleanup(keep = self.current)

    return(self)

