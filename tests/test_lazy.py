import unittest
import nctoolkit as nc
nc.options(lazy= True)
import pandas as pd
import xarray as xr
import os
import subprocess

def cdo_version():
    cdo_check = subprocess.run("cdo --version", shell = True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cdo_check = str(cdo_check.stderr).replace("\\n", "")
    cdo_check = cdo_check.replace("b'", "").strip()
    return cdo_check.split("(")[0].strip().split(" ")[-1]



class TestLazy(unittest.TestCase):
    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_select(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1970, 1979)))
        tracker.select_months([1,2,3,4,5])
        tracker.clip(lon = [0,90])
        tracker.clip(lat = [0,90])
        tracker.annual_mean()
        tracker.mean()
        tracker.spatial_mean()
        tracker.run()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x,18.435571670532227)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_lazy1(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1970, 1979)))
        tracker.select_months([1,2,3,4,5])
        tracker.clip(lon = [0,90])
        tracker.clip(lat = [0,90])
        tracker.annual_mean()
        tracker.mean()
        tracker.spatial_mean()
        tracker.run()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        y = len(tracker.history)
        self.assertEqual(x,18.435571670532227)
        if cdo_version() in ["1.9.2", "1.9.3"]:
            self.assertEqual(y, 2)
        else:
            self.assertEqual(y, 1)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_split1(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.split(by = "year")
        n_files = len(tracker.current)
        self.assertEqual(n_files, 30)
        tracker.merge_time()
        tracker.select_years(list(range(1970, 1979)))
        tracker.select_months([1,2,3,4,5])
        tracker.clip(lon = [0,90])
        tracker.clip(lat = [0,90])
        tracker.annual_mean()
        tracker.mean()
        tracker.spatial_mean()
        tracker.run()
        nc.cleanup()
        n = len(nc.session_files())
        self.assertEqual(n, 1)
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x, 18.435571670532227)


    def test_mergetime1(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.split(by = "year")
        n_files = len(tracker.current)
        tracker.merge_time()
        tracker.select_years(list(range(1970, 1979)))
        tracker.select_months([1,2,3,4,5])
        tracker.clip(lon = [0,90])
        tracker.clip(lat = [0,90])
        tracker.annual_mean()
        tracker.mean()
        tracker.spatial_mean()
        tracker.run()
        y = len(tracker.history)
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x, 18.435571670532227)
        self.assertEqual(n_files, 30)
        if cdo_version() in ["1.9.2", "1.9.3"]:
            self.assertEqual(y, 4)
        else:
            self.assertEqual(y, 2)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_ensemble_mean_1(self):
        ff = nc.create_ensemble("data/ensemble/")
        tracker = nc.open_data(ff)
        tracker.mean()
        tracker.ensemble_mean()
        tracker.spatial_mean()
        tracker.run()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x, 18.0283203125)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_transmute_1(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.transmute({"sst":"sst+273.15"})
        tracker.select_years(list(range(1970, 1979)))
        tracker.select_months([1,2,3,4,5])
        tracker.clip(lon = [0,90])
        tracker.clip(lat = [0,90])
        tracker.annual_mean()
        tracker.mean()
        tracker.spatial_mean()
        tracker.transmute({"sst":"sst-273.15"})
        tracker.run()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        y = len(tracker.history)
        self.assertEqual(x,  18.435571670532227)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_mutate_1(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.mutate({"sst1":"sst+273.15"})
        tracker.select_years(list(range(1970, 1979)))
        tracker.select_months([1,2,3,4,5])
        tracker.clip(lon = [0,90])
        tracker.clip(lat = [0,90])
        tracker.annual_mean()
        tracker.mean()
        tracker.spatial_mean()
        tracker.transmute({"sst2":"sst1-273.15"})
        tracker.run()
        x = tracker.to_xarray().sst2.values[0][0][0].astype("float")
        y = len(tracker.history)
        self.assertEqual(x, 18.435571670532227)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_seasonal_clim1(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.seasonal_mean_climatology()
        tracker.select_months(2)
        tracker.spatial_mean()
        tracker.run()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x, 17.9996280670166)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_merge_rename(self):
        ff = "data/sst.mon.mean.nc"
        tracker1 = nc.open_data(ff)
        tracker2 = nc.open_data(ff)
        tracker2.rename({"sst": "tos"})
        tracker2.run()
        tracker = nc.merge(tracker1, tracker2)
        tracker.transmute({"bias":"sst-tos"})
        tracker.mean()
        tracker.spatial_mean()
        tracker.run()
        x = tracker.to_xarray().bias.values[0][0][0].astype("float")
        self.assertEqual(x, 0)
        n = len(nc.session_files())
        self.assertEqual(n, 2)

    def test_anomaly(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.clip(lon = [-80, 20], lat = [30, 80])
        tracker.annual_anomaly(baseline = [1970, 1979])
        tracker.spatial_mean()
        tracker.mean()
        tracker.run()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x, 0.11958891153335571)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_arithall(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.add(1)
        tracker.subtract(1)
        tracker.multiply(2)
        tracker.divide(2)
        tracker.spatial_mean()
        tracker.mean()
        tracker.run()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        tracker = nc.open_data(ff)
        tracker.spatial_mean()
        tracker.mean()
        tracker.run()
        y = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x, y)
        n = len(nc.session_files())
        self.assertEqual(n, 1)


if __name__ == '__main__':
    unittest.main()

