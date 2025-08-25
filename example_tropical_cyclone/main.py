#!/bin/python
# 
# Cyclone detection and plotting using TempestExtremes and the ClimateDT data.
# This use-case requires TempestExtremes to be installed in the used environment.
# 
# netcdf and .txt data that has already been created for a specific
# date will not be overwritten but the date will be skipped.
# 
# Note: This is an example and not fully refined which causes TC to be detected that would likely be filtered out.  

import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from pathlib import Path
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import huracanpy
from tracker import detectnodes, stitchnodes
from preprocessing import preprocessing

#### Modify ------------------------------------------------------------------
# Define the basic requests for the data. Additional keys are added later on.
request_basic={
    "activity": ["scenariomip"],
    "class": "d1",
    "dataset": "climate-dt",
    "experiment": "ssp3-7.0",
    "expver": "0001",
    "generation": "1",
    "model": "icon",
    "realization": "1",
    "stream": "clte",
    "resolution": "high",
    "type": "fc",
    "time": "0000/to/2300/by/0300"
    }


data_path= f"{CURRENT_DIR}/data/"   # Define output data location 
ncfile_prefix = f"{data_path}/tmp_icon"  # netcdf data required for TempestExtremes. The netcdf files will be called ncfile_prexi_{date}.nc

track_path = f"{data_path}/tracks/"
nodes_path = f"{data_path}/nodes/"  # For the nodes also create a nodes subfolder
plot_path= f"{CURRENT_DIR}/plots/"  # Define plot output location

# Define start and end dates
start_date = datetime.strptime("2035-06-01", "%Y-%m-%d")
end_date = datetime.strptime("2035-06-10", "%Y-%m-%d") #"2035-07-31"

out_file = f"{track_path}/icon_{start_date}_{end_date}.csv" #File where the tracks will be stored

#### End mondify ---------------------------------------------------------------------------------

# Create all folders
Path(data_path).mkdir(parents=True, exist_ok=True)
Path(plot_path).mkdir(parents=True, exist_ok=True)
Path(nodes_path).mkdir(parents=True, exist_ok=True)
Path(track_path).mkdir(parents=True, exist_ok=True)

# Create a date list to loop over
datelist = [
    (start_date + timedelta(days=i)).strftime("%Y%m%d")
    for i in range((end_date - start_date).days + 1)
]

#preprocessing the data
preprocessing(datelist, ncfile_prefix, request_basic)

# run nodes detection
all_nodes_file = detectnodes(datelist, nodes_path, ncfile_prefix)
# run nodes stitching
stitchnodes(all_nodes_file, out_file)

# Create a plot and save it
tracks = huracanpy.load(out_file)
huracanpy.plot.tracks(tracks.lon, tracks.lat, intensity_var=tracks.wind)
plt.title(f"ICON SSP3-7.0 {start_date} to {end_date}")
plt.savefig(f"{plot_path}/icon_projection_tc_tracks_wind_{start_date}_{end_date}.png")