#!/bin/python
# Downloading Climate DT data in parallel. This will STORE the data on disk.
# The script loops over a datelist that is defined by a starting and end point.
# If a request file is not provided and example request will be used
#
# Run as: python parallel_data_download.py <number_of_threads> <start_date_YYYY-MM-DD> <end_date_YYYY-MM-DD> <optional_request_file>

#from get_climate_dt_data import get_data_as_file

from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
from datetime import datetime, timedelta

def download_date(date):
    """
    This function downloads data for a specific date.

    Parameters:
    ----------
    date: string
    """
    print(date)
    return

def main():
    """
    Using multiple threads, download the data.
    """
    n = int(sys.argv[1]) # number of threads
    start_date = datetime.strptime(sys.argv[2], "%Y-%m-%d")
    end_date = datetime.strptime(sys.argv[3], "%Y-%m-%d")

    
    datelist = [
    (start_date + timedelta(days=i)).strftime("%Y%m%d")
    for i in range((end_date - start_date).days + 1)
    ]
    
    with ThreadPoolExecutor(max_workers=n) as executor:
        futures = [executor.submit(download_date, date) for date in datelist]
        for future in as_completed(futures):
            future.result()  # This will raise exceptions if any occurred
    return

main()