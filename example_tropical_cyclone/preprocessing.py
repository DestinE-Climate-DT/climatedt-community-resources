# This script applies the preprocessing required for the TC tracking with TempestExtremes.

import sys
sys.path.insert(1, '../example_tools')

from example_tools.get_climate_dt_data import get_data_polytope
import earthkit.regrid
from pathlib import Path

def preprocessing(date:str, out_file:str, request_basic:dict):
    """Get the data from the data-bridge, apply prerpocessing and store as netcdf.
    Different request are needed for different leveltypes.

    Parameters:
    ----------
    datelist: list
          List of dates to loop over.
    ncfile_prefix: string
           File path and name for netcdf output.
    request_basic: dict
           MARS request for data-bridge.
    """

    request_pl=request_basic | {
        "date": date,
        "levtype": ["pl"],
        "param": ["129"],
        "levelist": ["500", "250"],
    }

    request_sfc=request_basic | {
        "date": date,
        "levtype": ["sfc"],
        "param": ["166", "165", "151"],
    }

    # remapping to 0.2 degree lonlat grid
    data_pl = get_data_polytope(request_pl)
    data_latlon_pl = earthkit.regrid.interpolate(data_pl, out_grid={"grid": [0.2,0.2]}, method="linear")

    data_sfc = get_data_polytope(request_sfc)
    data_latlon_sfc = earthkit.regrid.interpolate(data_sfc, out_grid={"grid": [0.2,0.2]}, method="linear")

    data_pl_sfc = data_latlon_sfc.to_xarray()
    data_pl_sfc["zg500"]=data_latlon_pl.to_xarray().z.sel(level=500)
    data_pl_sfc["zg250"]=data_latlon_pl.to_xarray().z.sel(level=250)

    # get rid of weird metadata. Sadly attr_drop fails continuously. 
    variables=["zg500", "zg250", '10u', '10v', 'msl']
    for var in variables:
        data_pl_sfc[var].attrs['_earthkit']="none"

    # Renaming to avoid errors due to format in nc file
    data_pl_sfc = data_pl_sfc.rename({"forecast_reference_time":"time"})
    data_pl_sfc =  data_pl_sfc.rename({"10u":"uas"})
    data_pl_sfc =  data_pl_sfc.rename({"10v":"vas"})

    print(f"Saving to {out_file}")
    data_pl_sfc.to_netcdf(out_file)
    return