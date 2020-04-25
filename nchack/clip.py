from .runthis import run_this
from .runthis import run_nco
from .temp_file import temp_file
from .flatten import str_flatten
from .session import nc_safe
from .cleanup import cleanup
from .cleanup import disk_clean
import subprocess
import copy

def clip(self, lon = [-180, 180], lat = [-90, 90], cdo = True):
    """
    Clip to a rectangular longitude and latitude box

    Parameters
    -------------
    lon: list
        The longitude range to select. This must be two variables, between -180 and 180 when cdo = True.
    lat: list
        The latitude range to select. This must be two variables, between -90 and 90 when cdo = True.
    cdo: boolean
        Do you want this to use CDO or NCO for clipping? Defaults to True. Set to False if you want to call NCO. NCO is better at handling very large horizontal grids.
    """

    if  type(lon) is not list or type(lat) is not list:
        raise TypeError("Check that lon/lat ranges are tuples")

    if len(lon) != 2:
        raise ValueError("lon is a list of more than 2 variables")

    if len(lat) != 2:
        raise ValueError("lat is a list of more than 2 variables")

    for ll in lon:
        if (type(ll) is not int) or (type(ll) is not float):
            raise ValueError(f"{ff} from lon is not a float or int")

    for ll in lat:
        if (type(ll) is not int) or (type(ll) is not float):
            raise ValueError(f"{ff} from lat is not a float or int")


    # now, clip to the lonlat box we need

    if  lat[1] < lat[0]:
        raise ValueError("Check lat order")
    if  lon[1] < lon[0]:
        raise ValueError("Check lon order")

    if cdo:
        if lon[0] >= -180 and lon[1] <= 180 and lat[0] >= -90 and lat[1] <= 90:
            lat_box = str_flatten(lon + lat)
            cdo_command = ("cdo -sellonlatbox," + lat_box)
            run_this(cdo_command, self, output = "ensemble")
            return None
        else:
            raise ValueError("The lonlat box supplied is not valid!")

    self.release()

    new_files = []
    new_commands = []

    for ff in self:

        out = subprocess.run(f"cdo griddes {ff}", shell = True, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
        lon_name = [x for x in str(out.stdout).replace("b'", "").split("\\n") if "xname" in x][0].split(" ")[-1]
        lat_name = [x for x in str(out.stdout).replace("b'", "").split("\\n") if "yname" in x][0].split(" ")[-1]
        target = temp_file("nc")

        nco_command = "ncea -d " + lat_name + "," + str(float(lat[0])) + "," + str(float(lat[1])) + " -d " + lon_name + "," + str(float(lon[0])) + "," + str(float(lon[1]))  + " " + ff + " " + target
        if lon == [-180, 180]:
            nco_command = "ncea -d " + lat_name + "," + str(float(lat[0])) + "," + str(float(lat[1])) +  " " + ff + " " + target

        if lat == [-90, 90]:
            nco_command = "ncea  -d " + lon_name + "," + str(float(lon[0])) + "," + str(float(lon[1]))  + " " + ff + " " + target

        target = run_nco(nco_command, target)

        new_commands.append(nco_command)

        new_files.append(target)

    self.history+=new_commands
    self._hold_history = copy.deepcopy(self.history)

    self.current = new_files

    cleanup()
    self.disk_clean()





