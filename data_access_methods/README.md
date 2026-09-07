## Overview of access methods to Climate DT data

#### There are tree major methods currently available for experienced users: Polytope, HDA, Earth Data Hub.
All are Python-based and have example notebooks or code snippets included here or linked to the source projects. For a quick test of all access methods start with the [Simplified use cases](#examples). 

> ### [Polytope](https://polytope.readthedocs.io/en/latest/ "Click here to access Polytope documentation")
> Poplytope is a service for extracting specific features or global fields. 
<!-- #https://polytope-client.readthedocs.io/en/latest/index.html -->

> ### [Harmonized Data Access (HDA)](https://destine-data-lake-docs.data.destination-earth.eu/en/latest/dedl-discovery-and-data-access/Harmonized-Data-Access/Harmonized-Data-Access.html "Click here to access HDA documentation")
> API providing unified access to the DestinE Data Portfolio.

> ### [Earth Data Hub (EDH)](https://earthdatahub.destine.eu/getting-started "Click here to access Earth Data Hub documentation")
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
> 

|| Polytope | HDA |  EDH |
|-|----------|----------|----------|
| Use case |  Access to all model outputs and the most built-in extraction features, like regridding  | Access to all model outputs in complete form (full field for a specific variable) | Analysis-ready outputs of essential variables, already regridded to a regular lon/lat grid |
|Advantages| Full data portfolio with few restrictions on usage | Easy connection to other datasets like the application output of Climate DT or Sentinel satellite products, similar features to Polytope |  Fast access without dealing with unfamiliar grids and data formats |
|Limitations| Extraction is in Grib or other formats that users are not used to | Some usage limits, requests are more complicated than Polytope  |  Usage limits, limited number of variables |
|<a id="examples"></a>[Simplified use cases](requirements.md "Click here to find python environment requirements")| [polytope_use_case.ipynb](polytope_use_case.ipynb) | [HDA_use_case.ipynb](HDA_use_case.ipynb) | [EDH_use_case.ipynb](earthdatahub_use_case.ipynb) |
|<a id="resources"></a>[Additional resources](requirements.md "Click here to find python environment requirements") | [github-polytope-examples](https://github.com/destination-earth-digital-twins/polytope-examples/tree/main/climate-dt) | [DestinE-DataLake-Lab-HDA](https://github.com/destination-earth/DestinE-DataLake-Lab/tree/main/HDA)| [DestinE-earthdatahub-Tutorial](https://earthdatahub.destine.eu/tutorials) |
<br><br>
<!-- | Access method | Use case | Advantages | Drawbacks | Simplified use cases | Additional resources |
|---|---|---|---|---|---|
| **Polytope** | Access to all model outputs and the most built-in extraction features, like regridding | Full data portfolio with few restrictions on usage | Extraction is in GRIB or other formats that users are not used to | [polytope_use_case.ipynb](polytope_use_case.ipynb) | [github-polytope-examples](https://github.com/destination-earth-digital-twins/polytope-examples/tree/main/climate-dt) |
| **HDA** | Access to all model outputs in complete form (full field for a specific variable) | Easy connection to other datasets like the application output of Climate DT or Sentinel satellite products, similar features to Polytope | Some usage limits, requests are more complicated than Polytope | [HDA_use_case.ipynb](HDA_use_case.ipynb) | [DestinE-DataLake-Lab](https://github.com/destination-earth/DestinE-DataLake-Lab/tree/main) |
| **Earth Data Hub** | Analysis-ready outputs of essential variables, already regridded to a regular lon/lat grid | Fast access without dealing with unfamiliar grids and data formats | Usage limits, limited number of variables | [earthdatahub_use_case.ipynb](earthdatahub_use_case.ipynb) | [DestinE-earthdatahub-Tutorial](https://earthdatahub.destine.eu/tutorials) | -->

### DestinE Data Lake

Before accessing the data, it is essential to understand how the data is stored. In [ClimateDT user guide](https://platform.destine.eu/docs/climate-dt-user-guide/doc/index.html) you will find a detailed description of the three coupled atmosphere–ocean models within the Climate DT project, as well as an overview on the [available simulations](https://platform.destine.eu/docs/climate-dt-user-guide/doc/models/index.html#models-simulations-intro). The simulations are performed on HPC supercomputers such as LUMI (Finland) and MareNostrum 5 (Spain). The quality-checked model outputs are then stored in its respective data bridges. A Data Bridge is a component of the DestinE Data Lake that has dedicated storage, dedicated computing resources, and software/APIs for accessing Digital Twin data. Below, you will find a simplified diagram representing the Data life cycle from production until the user accessibility. A more detailed representation of the Climte DT workflow can be found in [Workflow and Architecture](https://platform.destine.eu/docs/climate-dt-user-guide/doc/workflow.html).

                            Climate DT
                    ┌────────────┴────────────┐
                    ▼                         ▼
                LUMI                  MareNostrum 5
                Finland                     Spain
            (ICON and IFS-FESOM          (IFS-NEMO
             simulations)                 simulations)
                    │                         │
                    ▼                         ▼
        Data Quality Checker         Data Quality Checker
                    │                         │
                    ▼                         ▼
            LUMI Data Bridge          MN5 Data Bridge
                    └────────────┬────────────┘
                                 ▼
                         DestinE Data Lake
                                 │
                                 ▼
                        harmonised user access
                        (polytope, HDA, EDH)

### Data Structure and Keys

The access methods generally use a dictionary-based ```request``` syntax. The Table below summarizes the Data structure that along with the data keys (see [Data Structure and Keys](https://platform.destine.eu/docs/climate-dt-user-guide/doc/data/data_structure.html#data-structure) in the User guide), will help you build a detailed request adapted to your needs. You might also be interested in the [Data Catalog](https://platform.destine.eu/docs/climate-dt-user-guide/doc/data/data_catalogue.html#data-catalogue) that provides the list of parameters as part of the DestinE Climate DT data portfolio.  


| Simulations | Activity | Data Bridge | HEALPix output resolution |
|---|---|---|---|
| ICON – control, historical, SSP3-7.0 (r1) | baseline / projections | LUMI | high/standard |
| IFS-FESOM – control, historical, SSP3-7.0 (r1) | baseline / projections | LUMI | high/standard |
| IFS-NEMO – control, historical (r1), SSP3-7.0 (r1) | baseline / projections | MN5 | high/standard |
| IFS-FESOM – storyline simulations (r1–r5) | story-nudging | MN5 | high/standard |

<br><br>
