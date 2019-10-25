import os
import glob
import copy
import multiprocessing
import copy

from ._temp_file import temp_file
from ._filetracker import nc_created
from ._filetracker import nc_safe
from .flatten import str_flatten
from ._select import select_variables
from ._setters import set_longname
from ._time_stat import mean
from ._rename import rename
from ._cdo_command import cdo_command 
from ._expr import transmute
from ._cleanup import cleanup
from ._runthis import run_cdo

def annual_anomaly(self, var = None, baseline = None):
    """

    Calculate annual anomalies based on a baseline period
    The anomoly is calculated by first calculating the climatological mean for the given baseline period. Annual means are then calculated for each year and the anomaly is calculated compared with the baseline mean.
    
    Parameters
    -------------
    var : string
        Variable to calculate the anomomaly for. This only works with single variables currently 
    baseline: list
        Baseline years. An annual cimatology for these years is used to calculate the anomalies.

    Returns
    -------------
    nchack.NCData
        A new tracker with the annual anomalies labelled anomaly

    """

    if type(self.current) is not str:
        raise ValueError("Splitting the file by year did not work!")

    if var is None:
        if(len(self.variables) == 1):
            var = self.variables[0]
        else:
            raise ValueError("This method currently only works with single variables. Please select one")

    if type(var) is not str:
        raise ValueError("This method currently only works with single variables")

    if type(baseline) is not list:
        raise ValueError("baseline years supplied is not a list")

    # Calculate the yearly mean 
    new_tracker = copy.deepcopy(self)
    new_tracker.select_variables(var)
    new_tracker.rename({var:"observed"})
    new_tracker.annual_mean()
    nc_safe.append(new_tracker.current)

    remove_later = copy.deepcopy(new_tracker.current)

    # calculate the climatology
    clim_tracker = copy.deepcopy(self)
    clim_tracker.select_variables(var)
    clim_tracker.select_years(baseline)
    clim_tracker.mean()
    clim_tracker.rename({var:"base"})
    nc_safe.append(copy.deepcopy(clim_tracker.current))
    
    target = temp_file("nc") 

    nc_created.append(target)
    nc_safe.append(target)
    os_command = "cdo -L -expr,'anomaly=observed-base' -merge " + new_tracker.current + " " + clim_tracker.current + " " + target

    new_tracker.history.append(os_command)

    target = run_cdo(os_command, target)

    new_tracker.current = target

    if os.path.exists(target) == False:
        raise ValueError("Calculating the anomaly failed")

    nc_safe.remove(clim_tracker.current)
    nc_safe.remove(remove_later)

    cleanup(keep = new_tracker.current)

    del clim_tracker

    nc_safe.remove(target)
    self.history = self.history + new_tracker.history

    self.current = new_tracker.current
