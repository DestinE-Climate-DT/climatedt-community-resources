## Overview of access methods to Climate DT data

#### There are tree major methods currently available for experienced users: Polytope, HDA, Earth Data Hub.
All are Python-based and have example notebooks or code snippets included here or linked to the source projects. For a quick test of all access methods start with the [Simplified use cases](#examples). 

> ### [Polytope](https://polytope.readthedocs.io/en/latest/ "Click here to access Polytope documentation")
> Poplytope is a service for extracting specific features or global fields. 

> ### [Harmonized Data Access (HDA)](https://destine-data-lake-docs.data.destination-earth.eu/en/latest/dedl-discovery-and-data-access/Harmonized-Data-Access/Harmonized-Data-Access.html "Click here to access HDA documentation")
> API providing unified access to the DestinE Data Portfolio.

> ### [Earth Data Hub](https://earthdatahub.destine.eu/getting-started "Click here to access Earth Data Hub documentation")
> Platform for efficient access to and analysis of data.

<!-- > 
> #### Use case:
> Access to all model outputs and the most built-in extraction features, like regridding 
>
> #### Advantages:
> Full data portfolio with few restrictions on usage
> 
> #### Drawbacks:
> Extraction is in Grib or other formats that users are not used to -->

|| Polytope | HDA |  Earth Data Hub |
|-|----------|----------|----------|
| Use case |  Access to all model outputs and the most built-in extraction features, like regridding  | Access to all model outputs in complete form (full field for a specific variable) | Analysis-ready outputs of essential variables, already regridded to a regular lon/lat grid |
|Advantages| Full data portfolio with few restrictions on usage | Easy connection to other datasets like the application output of Climate DT or Sentinel satellite products, similar features to Polytope |  Fast access without dealing with unfamiliar grids and data formats |
|Drawbacks| Extraction is in Grib or other formats that users are not used to | Some usage limits, requests are more complicated than Polytope  |  Usage limits, limited number of variables |
|<a id="examples"></a>[Simplified use cases](requirements.md "Click here to find python environment requirements")| [polytope_use_case.ipynb](polytope_use_case.ipynb) | [HDA_use_case.ipynb](HDA_use_case.ipynb) | [earthdatahub_use_case.ipynb](earthdatahub_use_case.ipynb) |
|Additional resources | [github-polytope-examples](https://github.com/destination-earth-digital-twins/polytope-examples/tree/main/climate-dt) | [DestinE-DataLake-Lab](https://github.com/destination-earth/DestinE-DataLake-Lab/tree/main)| [DestinE-earthdatahub-Tutorial](https://earthdatahub.destine.eu/tutorials) |
<br><br>


> **Note**: HDA is not a single method but rather a set of HTTP requests that can be made using different Python packages. The main connecting factor is that ```destinelab``` is used to manage the authorisation for the Destination Earth datasets. Furthermore, the main concept of the HDA are STAC catalogues that are used to search and identify data.
>
>The main methods for making the requests are using:
>  -  ```requests``` &rarr; the most basic method
>  - ```pystac-client``` &rarr; a package tailored to make STAC-compliant requests
> - ```eodag``` &rarr; a package developed by the CS group with the most advanced capabilities of handling the requests, including streaming features
>
>Going through the list, the methods become more advanced and offer more capabilities, but the packages used increase in complexity and size.