import os
import shutil

from .runcommand import run_command
from .runthis import run_this
from .session import nc_safe

def write_nc(self, out, zip = True, overwrite = False):
    """
    Save a dataset to a named file

    Parameters
    -------------
    out : str
        output file name
    zip : boolean
        True/False depending on whether you want to zip the file. Defaults to True.

    """

    ff = self.current
    if type(ff) is not str:
        raise ValueError("You cannot save multiple files!")

    if os.path.exists(ff) == False:
        raise ValueError("The current state of the dataset does not exist")

    # Check if outfile exists and overwrite is set to False
    # This should maybe be a warning, not an error
    if os.path.exists(out) and overwrite == False:
        raise ValueError("The out file exists and overwrite is set to false")


    if len(self.history) == len(self._hold_history):
        if zip:
            os.system("cdo -z zip_9 copy " + ff + " " + out)
        else:
            os.system("cdo copy " + ff + " " + out)
    else:
        if zip:
            cdo_command = "cdo -L -z zip_9 "
        else:
            cdo_command = "cdo -L "

        self.run = True

        self.released = True

        run_this(cdo_command, self, out_file = out)
    if os.path.exists(out) == False:
        raise ValueError("File zipping was not successful")

    if ff in nc_safe:
        nc_safe.remove(ff)

    self.current = out


