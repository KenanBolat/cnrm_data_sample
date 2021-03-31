import os
import rioxarray
import h5py
import numpy as np
import xarray as xr
import pandas as pd
import dask as da
import scipy
import rasterio
import datetime
import time
import glob
import geopandas as gpd
import matplotlib.pyplot as plt
import rioxarray
from shapely.geometry import mapping


def get_files(location, filter):
    return [os.path.join(location, _) for _ in glob.glob1(location, filter)]

def get_mask_shape(data_path, name, crs="epsg:4326"):
    return gpd.read_file(os.path.join(data_path, name), crs=crs)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start = datetime.datetime.now()
    processing_path = "."
    data_path = os.path.join(processing_path, "data")
    nc_files = get_files(data_path, "*.nc")

    print(data_path)
    ds = xr.open_dataset(nc_files[0])
    tr = get_mask_shape(data_path, "gadm36_TUR_0.shp")


    ds.rio.set_spatial_dims(x_dim="lon", y_dim="lat", inplace=True).rio.write_crs("EPSG:4326", inplace=True)
    clipped = ds.rio.clip(tr.geometry.apply(mapping), tr.crs, drop=False)

    # Export clipped to netcdf
    clipped.to_netcdf(os.path.join(processing_path, 'Clipped_Updated'+str(datetime.date.today())+'.nc'))

    # Example Output
    ds.sel(season="2017-01-01").tas_m[0].transpose('lat', 'lon'). \
        rio.set_spatial_dims("lon", "lat", inplace=True). \
        rio.write_crs("EPSG:4326", inplace=True). \
        rio.to_raster("c.tif")
    end = datetime.datetime.now()
    print("Duration\t:", str(end - start), "|\tStart\t:", str(start))
