#!/bin/python
# Downloading Climate DT data in parallel. This will STORE the data on disk.
# The script loops over a datelist that is defined by a starting and end point.
# If a request file is not provided and example request will be used
#
# Request file should be a json file. Name doesn't matter if specified as argument. If not it will look for a file called request.json.
#
# Run as: python parallel_data_download.py <number_of_threads> <start_date_YYYY-MM-DD> <end_date_YYYY-MM-DD> <request.json>

from get_climate_dt_data import get_data_as_file

from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
from datetime import datetime, timedelta
import json

def download_date(date, request, output_path):
    """
    This function downloads data for a specific date.

    Parameters:
    ----------
    date: string
    """
    print(f'Requesting date {date}')
    output_file = output_path+'_'+date+'.grib'
    request['date'] = date
    get_data_as_file(request, output_file, parallel=True)
    return

def main():
    """
    Using multiple threads, download the data.
    """
    n = int(sys.argv[1]) # number of threads
    start_date = datetime.strptime(sys.argv[2], "%Y-%m-%d")
    end_date = datetime.strptime(sys.argv[3], "%Y-%m-%d")

    # create request from request file
    if len(sys.argv) > 4:
        with open(sys.argv[4], 'r') as f:
            request = json.load(f)
    else:
        with open("request.json", 'r') as f:
            request = json.load(f)
    
    # Set the output path
    # TODO: Make this variable!
    output_path="./data/test"

    # Create list of dates
    datelist = [
    (start_date + timedelta(days=i)).strftime("%Y%m%d")
    for i in range((end_date - start_date).days + 1)
    ]
    
    with ThreadPoolExecutor(max_workers=n) as executor:
        futures = [executor.submit(download_date, date, request, output_path) for date in datelist]
        for future in as_completed(futures):
            future.result()  # This will raise exceptions if any occurred
    return

main()