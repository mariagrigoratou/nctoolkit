from ._runthis import run_this
from .flatten import str_flatten
from ._cleanup import cleanup

def mask_lonlat(self, lon = [-180, 180], lat = [-90, 90], cores = 1):
    """
    Mask a lon/lat box 

    Parameters
    -------------
    lon : list
        Longitude range to mask. Must be of the form: [lon_min, lon_max]
    lat : list
        Latitude range to mask. Must be of the form: [lat_min, lat_max]
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with masked data 
    """

    if (type(lon) is not list) or (type(lat) is not list):
        raise ValueError("Check that lon/lat ranges are tuples")
    
    if(type(lon[0]) is float ) or ( type(lon[0]) is int) == False:
        raise ValueError("Check lon")
    
    if( type(lon[1]) is float ) or ( type(lon[1]) is int) == False:
        raise ValueError("Check lon")

    if( type(lat[0]) is float ) or ( type(lat[0]) is int) == False:
        raise ValueError("Check lat")
    
    if( type(lat[1]) is float ) or ( type(lat[1]) is int) == False:
        raise ValueError("Check lat")

    # now, clip to the lonlat box we need

    if lon[0] >= -180 and lon[1] <= 180 and lat[0] >= -90 and lat[1] <= 90:

        lat_box = str_flatten(lon + lat)
        cdo_command = ("cdo -masklonlatbox," + lat_box)
        run_this(cdo_command, self, output = "ensemble", cores = cores)
    else:
        raise ValueError("The lonlat box supplied is not valid!")

    # clean up the directory
    cleanup(keep = self.current)