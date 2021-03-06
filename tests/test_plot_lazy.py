import unittest
import nctoolkit as nc
import pandas as pd
import xarray as xr
import os
nc.options(lazy = True)


ff = "data/sst.mon.mean.nc"

class TestPlot(unittest.TestCase):
    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    #def test_plot1(self):
    #    tracker = nc.open_data(ff)
    #    x = str(type(tracker.plot()))
    #    x = "holoviews.core.spaces.DynamicMap" in x
    #    self.assertEqual(x,True)

    def test_plot2(self):
        tracker = nc.open_data(ff)
        tracker.spatial_mean()
        x = str(type(tracker.plot()))
        x = "holoviews.element.chart.Curve" in x
        self.assertEqual(x,True)

    def test_plot3(self):
        tracker = nc.open_data(ff)
        tracker.mutate({"tos":"sst+273"})
        tracker.spatial_mean()
        x = str(type(tracker.plot()))
        print(x)
        x = "holoviews.core.spaces.DynamicMap" in x
        self.assertEqual(x,True)

    def test_plot4(self):
        tracker = nc.open_data(ff)
        tracker.mutate({"tos":"sst+273"})
        x = str(type(tracker.plot()))
        x = "holoviews.core.spaces.DynamicMap" in x
        self.assertEqual(x,True)

    def test_error(self):
        ff = "data/woa18_decav_t01_01.nc"
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.plot()

if __name__ == '__main__':
    unittest.main()

