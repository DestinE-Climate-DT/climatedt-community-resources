# Tropical cyclone detection

This example uses the [TempestExtremes tracking algorithm](https://climate.ucdavis.edu/tempestextremes.php) as an example of a scientific application for the Climate DT data. 

To run this example you must either run the [desp-authentication.py](https://github.com/destination-earth-digital-twins/polytope-examples/blob/main/desp-authentication.py) on the machine where you want to run the example, or you must add your user name and key in the file [get_climate_dt_data.py](../example_tools/get_climate_dt_data.py). 

To run the example you need a working python environment. You can create the environment using the [environment.yml](./environment.yml) and running `mamba env create -f environment.yml`. After that you can activate the environment with `mamba activate climatedt-tc`.
Then try the example by running `python main.py`. This will take a while. To speed it up or to evaluate more days, you can change the time range in the [main.py](./main.py) by changing the values for:
```
start_date = datetime.strptime("2035-06-01", "%Y-%m-%d")
end_date = datetime.strptime("2035-06-05", "%Y-%m-%d")
```
In the end you should get a figure stored in `./plots/` showing different coloured points that have been detected. Only when running a longer time span one will get full tracks. These are not all necessarily meaningful tracks. 

Additionally, there will be a file called `./data/tracks/icon_start_date_end_date.csv` in which you can find the different detected tracks.