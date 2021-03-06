import unittest
import nctoolkit as nc
import pandas as pd
import xarray as xr
import os
nc.options(lazy = True)


ff = "data/sst.mon.mean.nc"

class TestDailycl(unittest.TestCase):

    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)
    def test_mean(self):

        tracker = nc.open_data(["data/2003.nc", "data/2004.nc"])
        tracker.select_timestep(0)
        tracker.merge_time()
        tracker.select_months(1)
        tracker.daily_mean_climatology()
        tracker.spatial_mean()
        x = tracker.to_dataframe().analysed_sst.values[0]

        tracker = nc.open_data(["data/2003.nc", "data/2004.nc"])
        tracker.select_timestep(0)
        tracker.merge_time()
        tracker.select_months(1)
        tracker.mean()
        tracker.spatial_mean()
        y = tracker.to_dataframe().analysed_sst.values[0]

        self.assertEqual(x,y)

        n = len(nc.session_files())
        self.assertEqual(n, 1)


    def test_min(self):

        tracker = nc.open_data(["data/2003.nc", "data/2004.nc"])
        tracker.select_timestep(0)
        tracker.merge_time()
        tracker.daily_min_climatology()
        tracker.spatial_mean()
        x = tracker.to_dataframe().analysed_sst.values[0]

        tracker = nc.open_data(["data/2003.nc", "data/2004.nc"])
        tracker.select_timestep(0)
        tracker.merge_time()
        tracker.min()
        tracker.spatial_mean()
        y = tracker.to_dataframe().analysed_sst.values[0]

        self.assertEqual(x,y)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_max(self):

        tracker = nc.open_data(["data/2003.nc", "data/2004.nc"])
        tracker.select_timestep(0)
        tracker.merge_time()
        tracker.daily_max_climatology()
        tracker.spatial_mean()
        x = tracker.to_dataframe().analysed_sst.values[0]

        tracker = nc.open_data(["data/2003.nc", "data/2004.nc"])
        tracker.select_timestep(0)
        tracker.merge_time()
        tracker.max()
        tracker.spatial_mean()
        y = tracker.to_dataframe().analysed_sst.values[0]

        self.assertEqual(x,y)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_range(self):

        tracker = nc.open_data(["data/2003.nc", "data/2004.nc"])
        tracker.select_timestep(0)
        tracker.merge_time()
        tracker.daily_range_climatology()
        tracker.spatial_mean()
        x = tracker.to_dataframe().analysed_sst.values[0]

        tracker = nc.open_data(["data/2003.nc", "data/2004.nc"])
        tracker.select_timestep(0)
        tracker.merge_time()
        tracker.range()
        tracker.spatial_mean()
        y = tracker.to_dataframe().analysed_sst.values[0]

        self.assertEqual(x,y)
        n = len(nc.session_files())
        self.assertEqual(n, 1)



if __name__ == '__main__':
    unittest.main()

