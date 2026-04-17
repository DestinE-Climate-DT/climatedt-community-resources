# What is it AQUA

The Application for QUality Assessment (AQUA) is a model evaluation framework designed for running diagnostics on high-resolution climate models, specifically for Climate DT climate simulations being part of Destination Earth activity. The package provides a flexible and efficient python3 framework to process and analyze large volumes of climate data. With its modular design, AQUA offers seamless integration of core functions and a wide range of diagnostic tools that can be run in parallel. AQUA offers:

- Efficient handling of large datasets from high-resolution climate models;
- Support for various data formats, such as NetCDF, GRIB, Zarr, FDB or ARCO;
- Robust and fast regridding functionality based on CDO;
- Averaging and aggregation tools for temporal and spatial analyses;
- Modular design for easy integration of new diagnostics. 

The code is available at the [official repository](https://github.com/DestinE-Climate-DT/AQUA) under public license. It is possible to access the ClimateDT data with AQUA, using internally Polytope to request data. Differently from other access method, AQUA will build the entire dataset of the requested experiment, accessing the dataset as a Dask-enabled xarray Dataset. The request will be internally handled when the computation requires it.

## 1. Creating the AQUA environment

AQUA is available as a Python package and can be installed in a local environment. The package is available on PyPI and can be installed with pip, but it requires extra dependencies which are not available on PyPI, such as CDO. For this reason, we document here how to create a conda environment for AQUA, which is the recommended way to use it.

### 1.1 Install conda

Please follow the instructions available on the [conda website](https://conda-forge.org/download/) to install conda on your machine. We recommend using the Miniconda distribution, which is a minimal version of conda that includes only the necessary packages to create and manage environments.

### 1.2 Create the conda environment

We recommend creating a conda environment for AQUA to manage the dependencies and avoid conflicts with other packages. The environment can be created with the following command:

```bash
conda create -n aquarium -c conda-forge python=3.12 cdo netcdf4 eccodes=2.41.0
conda activate aquarium
pip install aqua-core==1.0.0a4
```

As it can be seen, the core package of AQUA is available on PyPI and can be installed with pip, but the dependencies are not available on PyPI and need to be installed with conda. The above command will create a conda environment named `aquarium` with Python 3.12 and the necessary dependencies for AQUA. Please check the [AQUA documentation](https://aqua.readthedocs.io/en/latest/installation.html) for more details on the installation process and for specific instructions for different HPC machines.

If you are planning to use AQUA on Jupyter notebooks, you can also install the ipykernel package to make the kernel available in Jupyter:

```bash
pip install ipykernel
python -m ipykernel install --user --name aquarium
```

You should now be able to select the `aquarium` kernel in Jupyter and use AQUA to access the Climate DT data.

## 2. Installing AQUA auxiliary files

AQUA relies on auxiliary yaml files for some of its functionalities, shielding the final user from the details of the data structure and the regridding process. The files will be installed in the `~/.aqua/` directory and can be easily installed with the following command (be sure the `aquarium` environment is activated):

```bash
aqua install <your-machine-name>
```

## 3. Installing the AQUA catalogs

### 3.1 What are AQUA catalogs

AQUA catalogs are a series of YAML files with specifications on how to retrieve data, along with specification on the grids details and other relevant metadata. They are necessary for AQUA to access the data and to know how to handle it.

The nomenclature of the catalogs for the ClimateDT is `climatedt-gen<X>`, where `X` is the generation of the data.

### 3.2 Installing the AQUA catalogs

The AQUA catalogs can be easily installed and will be added to the auxiliary files in the `~/.aqua/` directory. The command to install the Climate DT catalog for the generation 2 is:

```bash
aqua add climatedt-gen2
```

## 4. Experiment nomenclature in AQUA

Data access with AQUA is based on a 4-level hierarchical structure, which is the following:

| Name | Description | Rule | Example |
|------|-------------|------|---------|
| catalog | Top level of the hierarchy, for ClimateDT data it collects all the dataset of a specific generation. It can be automatically detected if missing.| `<dataset>-gen<X>` | `climatedt-gen2` |
| model | Name of the model used for the simulation. | `<model-name>-<km-resolution>` | `IFS-NEMO-5km` |
| exp | Name of the experiment, which is a combination of the activity and the experiment. | `<activity>-<experiment>` | `projections-ssp370` |
| source | Name of the data source, usually associated to a specific resolution and stream. |  `<freq (monthly, hourly, daily)>-<grid>-<levtype (sfc, pl, o2d, o3d, sol)>` | `hourly-hpz10-sfc` |

Please check the individual generation portfolio for the available models, experiments and sources. The above nomenclature is used to access the data with AQUA, which will automatically build the request based on the specified catalog, model, experiment and source.

## 5. Explore a catalog content

Before retrieving any data, the user can explore the content of the catalog to check which data is available and how it is organized.

```python
from aqua import show_catalog_content

# Explore all available catalogs
show_catalog_content()

# Explore climatedt-gen2 catalog
show_catalog_content(catalog="climatedt-gen2")

# Explore the experiments available for the IFS-NEMO-5km model in the climatedt-gen2 catalog
show_catalog_content(catalog="climatedt-gen2", model="IFS-NEMO-5km")
```

## 6. Grid deployment

In order to enable regridding and weighted area statistics, AQUA needs to know the details of the grids used in the simulations. The grid details are stored in the auxiliary files, while we still need to deploy the grid files in the local environment.

We first recommend to choose a target directory where the grids will be deployed and areas and weights files will be generated. The target directory can be any directory in the local environment, but we recommend to choose a directory with enough space to store the grids and the generated files. The grids occupy less than 5 GB of space.

Let it be `<path-to-target-directory>` the path to the target directory, you can set it with the following command:

```bash
aqua grids set <path-to-target-directory>
```

We then need to deploy the grids.
In this same folder, a script to deploy the grids necessary for the entire generation 2 is available.
The script is contained in the `grids_deploy.py` file and can be run with the following command:

```bash
python grids_deploy.py --targetdir <path-to-target-directory>/grids
```

Please notice the extra `/grids` at the end of the target directory. This is necessary because our target directory will contain the subfolders `grids`, `areas` and `weights`, and we want to deploy the grids in the `grids` subfolder.

## 7. Getting the upgraded access to data

Please follow the instruction available in the `introduction` folder.
At the current stage AQUA is available only for local data analysis.
AQUA authenticates users via the `.polytopeapirc` file in your home folder, as described in the Option 2 of the `climate_dt_data_access.md` file or in the [AQUA documentation](https://aqua.readthedocs.io/en/latest/advanced_topics.html#polytope-access-to-destination-earth-data).

## 8. Data access with AQUA

Now that the code is installed and all auxiliary files are in place, you can start accessing the data with AQUA.
Let's say you want to access the data for the IFS-NEMO-5km model, for the projections-ssp370 experiment, for the hourly-hpz10-sfc source. The command to access the data is the following:

```python
from aqua import Reader

reader = Reader(catalog="climatedt-gen2", model="IFS-NEMO-5km", exp="projections-ssp370", source="hourly-hpz10-sfc", engine="polytope")
data = reader.retrieve()
```

The data will be retrieved as a Dask-enabled xarray Dataset, with all the available variables and timestep for the specified source. The request will be internally handled by AQUA when the computation requires it, allowing for an efficient access to the data without the need to download the entire dataset.
