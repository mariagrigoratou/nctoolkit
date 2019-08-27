
import os
import tempfile

from .flatten import str_flatten
from ._filetracker import nc_created
from ._cleanup import cleanup

from ._runcommand import run_command

def yearlystat(self, stat = "mean", silent = True):
    """Function to calculate the seasonal statistic from a function""" 
    ff = self.current

    target = tempfile.NamedTemporaryFile().name + ".nc"

    global nc_created
    nc_created.append(target)

    cdo_command = ("cdo -year" + stat + " " + ff + " " + target) 

    self.history.append(cdo_command)
    run_command(cdo_command, self, silent) 
    if self.run: self.current = target 

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
