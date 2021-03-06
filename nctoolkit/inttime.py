from nctoolkit.runthis import run_this

# to do. Some padding needs to be added in case something like 2000/1/1 is provided.


def time_interp(self, start=None, end=None, resolution="monthly"):
    """
    Temporally interpolate variables based on date range and time resolution

    Parameters
    -------------
    start : str
        Start date for interpolation. Needs to be of the form YYYY/MM/DD or YYYY-MM-DD
    end : str
        End date for interpolation. Needs to be of the form YYYY/MM/DD or YYYY-MM-DD. If end is not given interpolation will be to the final available time in the dataset
    resolution : str
        Time steps used for intpoleration. Needs to be "daily", "weekly", "monthly" or "yearly"
    """

    if resolution not in ["daily", "weekly", "monthly", "yearly"]:
        raise ValueError("Please supply a valid time resolution!")

    if resolution == "daily":
        resolution = "1day"

    if resolution == "weekly":
        resolution = "7day"

    if resolution == "monthly":
        resolution = "1month"

    if resolution == "yearly":
        resolution = "1year"

    if start is None:
        raise ValueError("No start data supplied")

    start = start.replace("/", "-")

    cdo_command = f"-inttime,{start},12:00:00,{resolution}"

    if end is None:
        cdo_command = f"cdo {cdo_command}"
    else:
        end = end.replace("/", "-")
        cdo_command = f"cdo -seldate,{start},{end} {cdo_command}"

    run_this(cdo_command, self, output="ensemble")
