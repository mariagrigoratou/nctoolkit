
import subprocess
import warnings

from nctoolkit.cleanup import cleanup
from nctoolkit.flatten import str_flatten
from nctoolkit.runthis import run_this
from nctoolkit.session import nc_safe


def select_season(self, season=None):
    """
    Select season from a dataset

    Parameters
    -------------
    season : str
        Season to select. One of "DJF", "MAM", "JJA", "SON"
        #change this to the below?
        #Season to select. One of "winter", "spring", "summer", "autumn"
    """

    if season is None:
        raise ValueError("No season supplied")

    if type(season) is not str:
        raise TypeError("No season supplied")

    if season not in ["DJF", "MAM", "JJA", "SON"]:
        raise ValueError("Invalid season supplied")

    cdo_command = f"cdo -select,season={season}"
    run_this(cdo_command, self, output="ensemble")


def select_months(self, months=None):
    """
    Select months from a dataset
    This method will subset the data to only contains months within the list given. A warning message will be provided when there are missing months.

    Parameters
    -------------
    months : list, range or int
        Month(s) to select.
    """

    if months is None:
        raise ValueError("Please supply months")

    # check validity of months
    if type(months) is range:
        months = list(months)

    if type(months) is not list:
        months = [months]
    # all of the variables in months need to be converted to ints, just in case floats have been provided

    for x in months:
        if type(x) is not int:
            raise TypeError(f"{x} is not an int")
        if x not in list(range(1, 13)):
            raise ValueError(f"{x} is not a month")

    months = str_flatten(months, ",")

    cdo_command = f"cdo -selmonth,{months}"
    run_this(cdo_command, self, output="ensemble")


def select_years(self, years=None):
    """
    Select years from a dataset
    This method will subset the data to only contains years within the list given. A warning message will be provided when there are missing years.
    Parameters
    -------------
    years : list,range or int
        Years(s) to select. These should be integers

    """
    if years is None:
        raise ValueError("Please supply years")

    if type(years) is range:
        years = list(years)

    if type(years) is not list:
        years = [years]

    # convert years to int

    for yy in years:
        if type(yy) is not int:
            raise TypeError(f"{yy} is not an int")

    if self._merged == False:
        select_years = False

        missing_files = 0

        n_removed = 0
        new_current = []

        for ff in self:

            cdo_result = subprocess.run(
                f"cdo showyear {ff}",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            all_years = []
            cdo_result = str(cdo_result.stdout).replace("\\n", "")
            cdo_result = cdo_result.replace("b'", "").strip()
            cdo_result = cdo_result.replace("'", "").strip()
            cdo_result = cdo_result.split()
            all_years += cdo_result
            all_years = list(set(all_years))
            all_years = [int(v) for v in all_years]
            inter = [element for element in all_years if element in years]

            if len(inter) > 0:
                new_current.append(ff)
            if len(inter) == 0:
                n_removed += 1
                if ff in nc_safe:
                    nc_safe.remove(ff)

            # figure out if any of the files actually have years outide the period required
            if len(inter) > 0:
                if len([yy for yy in all_years if yy not in years]) > 0:
                    missing_files += 1

        if len(new_current) == 0:
            raise ValueError("Data for none of the years is available!")

        if n_removed > 0:
            warnings.warn(
                message="A total of "
                + str(n_removed)
                + " files did not have valid years, so were removed from the dataset!"
            )

        self.current = new_current

        if missing_files > 0:
            years = str_flatten(years, ",")

            cdo_command = f"cdo -selyear,{years}"

            run_this(cdo_command, self, output="ensemble")
    else:
        years = str_flatten(years, ",")

        cdo_command = f"cdo -selyear,{years}"

        run_this(cdo_command, self, output="ensemble")

    cleanup()


def select_variables(self, vars=None):
    """
    Select variables from a dataset

    Parameters
    -------------
    vars : list or str
        Variable(s) to select.

    """

    if vars is None:
        raise ValueError("vars was not supplied")

    if type(vars) is str:
        vars_list = [vars]
    else:
        vars_list = vars

    for vv in vars_list:
        if type(vv) is not str:
            raise TypeError(f"{vv} is not a str")

    vars_list = str_flatten(vars_list, ",")

    cdo_command = f"cdo -selname,{vars_list}"

    run_this(cdo_command, self, output="ensemble")


def select_timestep(self, times=None):
    """
    Select timesteps from a dataset

    Parameters
    -------------
    times : list or int
        time step(s) to select. For example, if you wanted the first time step set times = 0.
    """

    if times is None:
        raise ValueError("Please supply times")

    if type(times) is range:
        times = list(times)

    if type(times) is not list:
        times = [times]

    for tt in times:
        if type(tt) is not int:
            raise TypeError(f"{tt} is not an int")
        if tt < 0:
            raise ValueError(f"{tt} is not a valid timestep")

    # all of the variables in months need to be converted to ints, just in case floats have been provided

    times = [int(x) + 1 for x in times]
    times = [str(x) for x in times]
    times = str_flatten(times)

    cdo_command = f"cdo -seltimestep,{times}"

    run_this(cdo_command, self, output="ensemble")
