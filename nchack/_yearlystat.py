
import os
import tempfile

from .flatten import str_flatten
from ._filetracker import nc_created
from ._cleanup import cleanup

from ._runthis import run_this

def yearlystat(self, stat = "mean", silent = True):
    """Function to calculate the seasonal statistic from a function""" 

    cdo_command = "cdo -year" + stat

    run_this(cdo_command, self, silent, output = "ensemble")

    # clean up the directory
    cleanup(keep = self.current)

    return(self)
    

def yearly_mean(self, silent = True):
    return yearlystat(self, stat = "mean", silent = True)

def yearly_min(self, silent = True):
    return yearlystat(self, stat = "min", silent = True)

def yearly_max(self, silent = True):
    return yearlystat(self, stat = "max", silent = True)
    
def yearly_range(self, silent = True):
    return yearlystat(self, stat = "range", silent = True)
