
from ._cleanup import cleanup
from ._runthis import run_this

def seasstat(self, stat = "mean", silent = True, cores = 1):
    """Method to calculate the seasonal statistic from a function""" 

    cdo_command = "cdo -seas" + stat

    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)

    # clean up the directory
    cleanup(keep = self.current)

    

def seasonal_mean(self, silent = True, cores = 1):
    """
    Calculate the seasonal mean for each year. Applies at the grid cell level.

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling sum
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with the seasonal mean 
    """
    return seasstat(self, stat = "mean", silent = True, cores = cores)

def seasonal_min(self, silent = True, cores = 1):
    """
    Calculate the seasonal minimum for each year. Applies at the grid cell level.

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling sum
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with the seasonal minimum 
    """
    return seasstat(self, stat = "min", silent = True, cores = cores)

def seasonal_max(self, silent = True, cores = 1):
    """
    Calculate the seasonal maximum for each year. Applies at the grid cell level.

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling sum
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with the seasonal maximum 
    """
    return seasstat(self, stat = "max", silent = True, cores = cores)
    
def seasonal_range(self, silent = True, cores = 1):
    """
    Calculate the seasonal range for each year. Applies at the grid cell level.

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling sum
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with the seasonal range 
    """
    return seasstat(self, stat = "range", silent = True, cores = cores)
