#!/bin/python
# Downloading Climate DT data in parallel. This will STORE the data on disk.
# The script loops over a datelist that is defined by a starting and end point.
# If a request file is not provided and example request will be used
#
# Request file should be a json file. Name doesn't matter if specified as argument. If not it will look for a file called request.json.
#
# If run without arguments, default values will be used. 
# With arguments:
# python parallel_data_download.py --num_threads 8 --start_date 2023-06-01 --end_date 2023-06-10 --request_file custom_request.json --output_prefix ./output/data


from get_climate_dt_data import get_data_as_file

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
import json
import argparse

def download_date(date:str, request:dict, output_path:str):
    """
    This function downloads data for a specific date.

    Parameters:
    ----------
    date: Requested day
    request: The data request dictionary
    output_path: Location where data will be stored
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
    parser = argparse.ArgumentParser(description="Download data using multiple threads.")
    parser.add_argument("-n", "--num_threads", type=int, default=4,
                        help="Number of threads to use (default: 4)")
    parser.add_argument("-s", "--start_date", type=str, default="2023-01-01",
                        help="Start date in YYYY-MM-DD format (default: 2023-01-01)")
    parser.add_argument("-e", "--end_date", type=str, default="2023-01-10",
                        help="End date in YYYY-MM-DD format (default: 2023-01-10)")
    parser.add_argument("-r", "--request_file", type=str, default="request.json",
                        help="Path to request JSON file (default: request.json)")
    parser.add_argument("-o", "--output_prefix", type=str, default="./data/test",
                        help="Output prefix path (default: ./data/test)")

    args = parser.parse_args()

    # Validate date format
    try:
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Dates must be in YYYY-MM-DD format.")

    if start_date > end_date:
        raise ValueError("Start date must be before or equal to end date.")

    # Load request file
    try:
        with open(args.request_file, 'r') as f:
            request = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Request file '{args.request_file}' not found.")
    except json.JSONDecodeError:
        raise ValueError(f"Request file '{args.request_file}' is not valid JSON.")


    # Create list of dates
    datelist = [
    (start_date + timedelta(days=i)).strftime("%Y%m%d")
    for i in range((end_date - start_date).days + 1)
    ]
    
    # run download in parallel.
    with ThreadPoolExecutor(max_workers=args.num_threads) as executor:
        futures = [executor.submit(download_date, date, request, args.output_prefix) for date in datelist]
        for future in as_completed(futures):
            future.result()  # This will raise exceptions if any occurred
    return

if __name__ == "__main__":
    main()
