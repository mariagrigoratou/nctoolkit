import unittest
import nchack as nc
nc.options(lazy= False)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os


class TestSelect(unittest.TestCase):

    def test_1(self):
        ff = "data/sst.mon.mean.nc"
        ff1 = "/tmp/test.nc"
        data = nc.open_data(ff)
        data.select_timestep(0)
        data.write_nc(ff1)
        data1 = nc.open_data(ff1)

        data.spatial_mean()
        data1.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")
        y = data1.to_dataframe().sst.values[0].astype("float")
        os.remove(ff1)
        self.assertEqual(x,y)


    def test_2(self):
        ff = "data/sst.mon.mean.nc"
        ff1 = "/tmp/test.nc"
        data = nc.open_data(ff)
        data.select_timestep(0)
        data.release()
        data.write_nc(ff1, zip = False)
        data1 = nc.open_data(ff1)

        data.spatial_mean()
        data1.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")
        y = data1.to_dataframe().sst.values[0].astype("float")
        os.remove(ff1)
        self.assertEqual(x,y)


    def test_3(self):
        ff = "data/sst.mon.mean.nc"
        ff1 = "/tmp/test.nc"
        data = nc.open_data(ff)
        data.select_timestep(0)
        data.release()
        data.write_nc(ff1, zip = False)

        data1 = nc.open_data(ff1)
        data1.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")
        os.remove(ff1)

        ff = "data/sst.mon.mean.nc"
        ff1 = "/tmp/test.nc"
        data = nc.open_data(ff)
        data.select_timestep(0)
        data.release()
        data.write_nc(ff1, zip = True)

        data1 = nc.open_data(ff1)
        data1.spatial_mean()
        y = data.to_dataframe().sst.values[0].astype("float")
        os.remove(ff1)


        self.assertEqual(x,y)


    def test_4(self):
        ff = "data/sst.mon.mean.nc"
        ff1 = "/tmp/test.nc"
        data = nc.open_data(ff)
        data.select_timestep(0)
        data.write_nc(ff1, zip = False)

        data1 = nc.open_data(ff1)
        data1.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")
        os.remove(ff1)

        ff = "data/sst.mon.mean.nc"
        ff1 = "/tmp/test.nc"
        data = nc.open_data(ff)
        data.select_timestep(0)
        data.write_nc(ff1, zip = True)

        data1 = nc.open_data(ff1)
        data1.spatial_mean()
        y = data.to_dataframe().sst.values[0].astype("float")
        os.remove(ff1)


        self.assertEqual(x,y)

    def test_5(self):
        ff = "data/sst.mon.mean.nc"
        ff1 = "/tmp/test.nc"
        data = nc.open_data(ff)
        data.select_timestep([0,1])
        data.mean()
        data.write_nc(ff1, zip = False)

        data1 = nc.open_data(ff1)
        data1.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")
        os.remove(ff1)

        ff = "data/sst.mon.mean.nc"
        ff1 = "/tmp/test.nc"
        data = nc.open_data(ff)
        data.select_timestep([0,1])
        data.split("yearmonth")
        data.ensemble_mean()
        data.write_nc(ff1, zip = True)

        data1 = nc.open_data(ff1)
        data1.spatial_mean()
        y = data.to_dataframe().sst.values[0].astype("float")
        os.remove(ff1)


        self.assertEqual(x,y)

    def test_ens(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select_timestep([0,1,2])
        data.split("yearmonth")
        with self.assertRaises(ValueError) as context:
            data.write_nc("/tmp/test.nc")

    def test_overwrite(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            data.write_nc(ff)



if __name__ == '__main__':
    unittest.main()
