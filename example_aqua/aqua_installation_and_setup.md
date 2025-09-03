# What is it AQUA

The Application for QUality Assessment (AQUA) is a model evaluation framework designed for running diagnostics on high-resolution climate models, specifically for Climate DT climate simulations being part of Destination Earth activity. The package provides a flexible and efficient python3 framework to process and analyze large volumes of climate data. With its modular design, AQUA offers seamless integration of core functions and a wide range of diagnostic tools that can be run in parallel. AQUA offers:

- Efficient handling of large datasets from high-resolution climate models;
- Support for various data formats, such as NetCDF, GRIB, Zarr or FDB;
- Robust and fast regridding functionality based on CDO;
- Averaging and aggregation tools for temporal and spatial analyses;
- Modular design for easy integration of new diagnostics. 

The code is available at the [official repository](https://github.com/DestinE-Climate-DT/AQUA) under public license. It is possible to access the ClimateDT data with AQUA, using internally Polytope to request data. Differently from other access method, AQUA will build the entire dataset of the requested experiment, accessing the dataset as a Dask-enabled xarray Dataset. The request will be internally handled when the computation requires it.

## 1. Getting the upgraded access to data

Please follow the instruction available in the `introduction` folder.
At the current stage the AQUA is available only for local data analysis.
AQUA authenticates users via the `.polytopeapirc` file in your home folder, as described in the Option 2 of the `climate_dt_data_access.md` file or in the [AQUA documentation](https://aqua.readthedocs.io/en/latest/advanced_topics.html#polytope-access-to-destination-earth-data).

## 2. Creating the AQUA environment

Detailed tutorial and specific instructions for creating the AQUA environment on different HPC machines are available in the [AQUA documentation](https://aqua.readthedocs.io/en/latest/installation.html).

If you are in a local machine or unknown HPC with conda support:

1. Clone the repository: `git clone git@github.com:DestinE-Climate-DT/AQUA.git`
2. Enter the cloned directory: `cd AQUA`
3. Create a conda environment: `conda env create -f environment.yml`
4. Activate the conda environment: `conda activate aqua`
5. Install ipykernel: `pip install ipykernel`
6. Add the kernel to Jupyter: `python -m ipykernel install --user --name aqua`

You should now be able to select this kernel to run the AQUA notebooks.

## 3. Installing the AQUA catalogs

Differently from other access methods, AQUA needs to have an installed catalog, a series of YAML file with specifications on which data can retrieved, along with specification on the available variable, grids details and other relevant metadata.

They can be easily installed once the AQUA environment is set up and activated. Detailed information can be found in the [AQUA documentation](https://aqua.readthedocs.io/en/latest/aqua_console.html).

Here we present a short version of the installation process:

1. Install the configuration file in the `~/.aqua/` with: `aqua install <your-machine-name>`
2. Add the Climatedt Phase 1 catalog with: `aqua add catalog climatedt-phase1`

If additionally you want to enable regrid capabilities:

3. Set the path for the grids download directory with: `aqua grids set <path-to-your-grids-directory>`. This will generate a grids, areas and weights directory in the specified path.
