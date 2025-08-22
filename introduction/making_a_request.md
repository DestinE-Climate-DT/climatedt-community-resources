   
# Notes on how to select data from available simulations

An overview of the available Climate DT simulations is provided [here](https://destine.ecmwf.int/climate-change-adaptation-digital-twin-climate-dt/#simulations). To work with the data it is necessary to create a `request` which will find the corresponding data. This can be done either by using the [STAC catalogue](https://qubed.lumi.apps.dte.destination-earth.eu/) (recommended to start with) or by modifying/creating ones own request. In the polytope examples the point the data selection is done with a version of following code block (this one is taken from [climate-dt-earthkit-example-domain.ipynb](https://github.com/destination-earth-digital-twins/polytope-examples/blob/main/climate-dt/climate-dt-earthkit-example-domain.ipynb)):

```
request = {
    'activity': 'ScenarioMIP',   <- What type of run
    'class': 'd1',                  
    'dataset': 'climate-dt',        
    'date': '20200102',          <- What date is requested
    'experiment': 'SSP3-7.0',
    'expver': '0001',
    'generation': '1',
    'levtype': 'sfc',            <- What type of level
    'model': 'IFS-NEMO',         <- Which model
    'param': '134/165/166',      <- Which variables using their grib IDs
    'realization': '1',
    'resolution': 'standard',
    'stream': 'clte',
    'time': '0100',              <- What time should be selected
    'type': 'fc'
}
```

This polytope request can be modified to request data from any of the available simulations.

#### Modifying the request

Generally, all requests use the same syntax and a detailed documentation is provided in the [MARS user documentation](https://confluence.ecmwf.int/display/UDOC/MARS+command+and+request+syntax). For Climate DT there are some main request keys that should be specified: 

| Key        | Relevant values    | Description                                                |
|------------|--------------------|------------------------------------------------------------|
| activity   | scenariomip, highresmip, cmip6, story-nudging, baseline     | The type of activity the simulation corresponds to in CMIP   |
| class      | d1                 | The data originates from Destination Earth |
| dataset      | climate-dt       | Selects the Climate DT data from Destination Earth |
| date       | YYYYMMDD (YYYYMMDD/to/YYYYMMDD) | Date or dates for which the data is required |  
| experiment | cont/hist/ssp3-7.0 | What kind of experiment   |
| expver     | 0001    | Experiment version remains the same  |
| generation   | 1     | Climate DT phase. Only phase 1 available currently  |
| levtype   |  sfc,pl,o2d,...                 |   Level type depends on variable                                                   |
| model   |  ifs-fesom, ifs-nemo, icon     |   Available models in Climate DT  |
| param           |   gribid or gribid1/gribid2/gribid3    |   Depends on variable    |
| realization  |  1 or ensemble number  | Number of ensemble member   |
|  resolution  |   high or standard  | HEALPix zoom level: high=10 or 9 (H1024 or H512) depending on simulation , standard=7 (H128) |
|  stream  | clte, clmn  | Daily values or monthly values        |
| time   | HHMM or HHMM/HHMM/HHMM   | Only full hour data in Climate DT    |
|  type     |  fc       |  All Climate DT data uses type forecast  |
