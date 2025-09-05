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
from tracker import detectnodes, stitchnodes, combine_all_nodes
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
formatted_sdate= start_date.strftime("%Y%m%d")
formatted_edate = end_date.strftime("%Y%m%d")
track_file = f"{track_path}/icon_{start_date.strftime("%Y%m%d")}_{end_date.strftime("%Y%m%d")}.csv" #File where the tracks will be stored

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

for date in datelist:
    nc_file = f"{ncfile_prefix}_{date}.nc"
    nodes_subpath=f"{nodes_path}/{date[:4]}/{date[4:6]}"
    nodes_file = f"{nodes_subpath}/nodes_{date}.txt"
    Path(nodes_subpath).mkdir(parents=True, exist_ok=True)
    
    # Skip date if output already exists
    if Path(nodes_file).exists():
        print(f"{nodes_file} exists, skipping...")
        continue
    
    print(f"Processing {date}")
    
    #preprocessing the data
    preprocessing(date, nc_file, request_basic)
    # run nodes detection
    detectnodes(nodes_file, nc_file)
    
    # remove netcdf files so they don't use too much space
    print(f"Removing {nc_file}")
    os.remove(nc_file) 
   # return

# combine all node files into one file
all_nodes_file = combine_all_nodes(nodes_path, formatted_sdate, formatted_edate)
# run nodes stitching
stitchnodes(all_nodes_file, track_file)

# Create a plot and save it
tracks = huracanpy.load(track_file)
huracanpy.plot.tracks(tracks.lon, tracks.lat, intensity_var=tracks.wind)
plt.title(f"ICON SSP3-7.0 {formatted_sdate} to {formatted_edate}")
plt.savefig(f"{plot_path}/icon_projection_tc_tracks_wind_{formatted_sdate}_{formatted_edate}.png")