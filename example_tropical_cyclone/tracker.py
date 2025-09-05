#!/bin/python
# 
# Cyclone detection and plotting using TempestExtremes and the ClimateDT data.
# This use-case requires TempestExtremes to be installed in the used environment.
# The data request can be added in get_data_as_nc

import sys
sys.path.insert(1, '.')

import subprocess
import glob
from pathlib import Path

def detectnodes(nodes_file:str,nc_file:str)->str:
    # For every day get the data from the data-bridge and stores it as netcdf file. 
    # Then run the DetectNodes processing to detect the tropical cyclones
                
    # Here the TempestExtremes function DetectNodes is called.
    subprocess.run([
        "DetectNodes",
        "--in_data", nc_file,
        "--out", nodes_file,
        "--searchbymin", "msl",
        "--latname", "latitude",
        "--lonname", "longitude",
        "--closedcontourcmd", "msl,200.0,5.5,0;_DIFF(zg250,zg500),-6,6.5,1.0",
        "--mergedist", "6.0",
        "--outputcmd", "msl,min,0;_VECMAG(uas,vas),max,2"
    ])
    
    #if verbose: 
    #    subprocess.run(["head", nodes_file])
    return

def combine_all_nodes(nodes_path:str,start:str, end:str)->str:
    # now combine all files 
    flist = glob.glob(f'{nodes_path}/*/*/*.txt')
    all_nodes = f'{nodes_path}/all_nodes_{start}_{end}.dat'
    
    with open(all_nodes, 'w') as outfile:
        for fname in flist:
            with open(fname, 'r') as infile:
                outfile.write(infile.read())
    
    return all_nodes

def stitchnodes(in_file:str, out_file:str) -> None:
    """Stitch the different found nodes together to produce a track.
    Parameters:
    -----------
    in_file: string
             Input file name
    out_file: string
             Output file name
    """
    # Here the TempestExtremes function StitchNodes is called.
    subprocess.run([ 
        "StitchNodes",
        "--in", in_file,
        "--out", out_file,
        "--out_file_format", "csv",
        "--in_fmt", "lon,lat,slp,wind",
        "--range", "8.0",
        "--mintime", "54h",
        "--maxgap", "24h",
        "--threshold", "wind,>=,10.0,10;lat,<=,50.0,10;lat,>=,-50.0,10",
    ])
    return