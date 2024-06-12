## Code to download NWM Retrospective 2.1 data into Pandas series
## Copy and paste the first bit into your notebook, script, etc.
##   and then see below the next comment for example function calls

import os
import pandas
import xarray
import s3fs

s3_path = 's3://noaa-nwm-retrospective-2-1-zarr-pds/chrtout.zarr'
s3 = s3fs.S3FileSystem(anon=True)
store = s3fs.S3Map(root=s3_path, s3=s3, check=False)
ds_zarr = xarray.open_zarr(store=store, consolidated=True)

def get_streamflow_by_reach(reach, start_time=None, end_time=None, make_csv=False):
  ## Full range of data is 1979-02-01 01:00 through 2020-12-31 23:00
  ## Not sure of the timezone used in the AWS bucket
  timerange = slice(start_time, end_time)
  if start_time != None:
    ser = ds_zarr.sel(feature_id=reach, time=timerange).streamflow.to_pandas().rename('streamflow')
  else:
    ser = ds_zarr.sel(feature_id=reach).streamflow.to_pandas().rename('streamflow')
  if make_csv is not None and make_csv is not False:
    if make_csv is True:
      make_csv = f'NWM{reach}.csv'
    ser.to_csv(make_csv)
  return ser

## End bit to copy

## Below are sample function calls
##   Return value q is a pandas series

  # q = get_streamflow_by_reach(166176984)
  # print(q)
  # q.to_csv('NWM166176984.csv')
  
  ## This function call does the same as the 3 lines above, minus the print(q)
  # q = get_streamflow_by_reach(166176984, make_csv=True)
  
  # q = get_streamflow_by_reach(4587228, start_time='2018-01-01', end_time='2020-12-31')
  # q = get_streamflow_by_reach(4587100, start_time='2018-01-01 06:00:00', end_time='2020-12-31 12:00:00', make_csv=True)
