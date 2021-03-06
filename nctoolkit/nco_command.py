
import copy
import subprocess

from nctoolkit.cleanup import cleanup, disk_clean
from nctoolkit.flatten import str_flatten
from nctoolkit.runthis import run_nco
from nctoolkit.session import nc_safe
from nctoolkit.temp_file import temp_file


def nco_command(self, command=None, ensemble=False):
    """
    Apply a cdo command

    Parameters
    -------------
    command : string
        cdo command to call. This must be of the form cdo command infile outfile, where cdo, infile and outfile are attached later.
    ensemble : boolean
        Set to True if you want the command to take all of the files as input
    """

    # First, check that the command is valid
    if command is None:
        raise ValueError("Please supply a command")

    if type(command) is not str:
        raise TypeError("Command supplied is not a str")

    new_files = []
    new_commands = []

    if (ensemble == False) or (len(self) == 1):
        for ff in self:

            target = temp_file(".nc")

            the_command = f"{command} {ff} {target}"

            target = run_nco(the_command, target=target)

            new_files.append(target)
            new_commands.append(the_command)

    else:
        target = temp_file(".nc")

        files = str_flatten(self.current, " ")

        the_command = f"{command} {files} {target}"

        target = run_nco(the_command, target=target)

        new_files.append(target)
        new_commands.append(the_command)

    self.current = new_files

    self.history.append(command)
    self._hold_history = copy.deepcopy(self.history)

    self.disk_clean()
