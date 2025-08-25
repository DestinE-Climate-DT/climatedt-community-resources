# Climate DT data access

## Option 1: Interactive data analysis on the Destination Earth Service Platform (DESP)

The following steps can be followed by users who have been granted upgraded access to [DESP](https://platform.destine.eu).

To explore the ClimateDT data via the DESP one can use the Insula - Code service to run Jupyter Notebooks interactively. First go to [Insula Code](https://platform.destine.eu/services/service/insula-code/), sign in (upper left corner), then click "Go to service". Then a server will be started that will launch a Jupyter lab. There are multiple folders to begin with. Select polytope-lab -> climate-dt. There are multiple example jupyter notebooks in this folder which can be used as basis for any analysis.

As an example, you can select the DestinE storylines notebook, e.g. `climate-dt-earthkit-fe-story-nudging.ipynb`. There are different kernels that can be chosen when opening the jupyter-notebook. For the examples the `Polytope` kernel is suggested and can be selected in the upper right corner above the notebook.

Example output should be:


<img width="475" alt="image" src="https://github.com/user-attachments/assets/53576b86-6907-43bd-9c6f-0b26027e2387" />

Success!

**Updating an existing environment in Insula**  
In case you want to change the Python environment you are working with in Insula, you can install additional packages. This can be done by executing in one of the first cells `pip install` and restarting the kernel. For example you could install earthkit or kaleido like this:

```bash
pip install --upgrade --user earthkit
pip install --user kaleido
```

**Creating a new environment in Insula**   
If you are using Insula on the DESP to access data, the following instructions listed in Option 2 will generate a working Python kernel that will be visible in jupyter.

## Option 2: local data analysis

To start you can clone the [polytope-examples repository](https://github.com/destination-earth-digital-twins/polytope-examples/tree/main/). There you can find many different examples on how to access and process the Climate DT data. To run these examples you will have to authenticate with your personal DESP username and password.

To explore the Climate DT data locally (e.g. on a HPC/laptop), a Python environment can be created using the [requirements.txt](https://github.com/destination-earth-digital-twins/polytope-examples/blob/main/requirements.txt) or the [environment.yml](https://github.com/destination-earth-digital-twins/polytope-examples/blob/main/environment.yml), provided in the [polytopes examples repository](https://github.com/destination-earth-digital-twins/polytope-examples/tree/main). Here we briefly summarize two ways for you to create a suitable environment to work with the Climate DT data. 

### 2.1 Using pip

1. Generate a python virtual environment: `python -m venv /home/jovyan/my_env`

2. Activate your environment: `source /home/jovyan/my_env/bin/activate`

3. Install the required libraries from the [requirements.txt file]( https://github.com/destination-earth-digital-twins/polytope-examples/blob/main/requirements.txt): `pip install requirements.txt`

4. Install ipykernel to make the kernel visible in your notebooks: `pip install ipykernel` then run `python -m venv /home/jovyan/my_env` and lastly `ipython kernel install --user --name=my_env`

You should now be able to select this kernel and access the Climate DT data.

If you have previously created a python venv you may need to update the versions of some packages. You can do this manually or by reinstalling from the requirements.txt

### 2.2 Using conda or mamba

To create a conda or mamba environment the following steps are required (adjust accordingly for conda):

1. Get the environment file from the polytope-examples:
`wget https://raw.githubusercontent.com/destination-earth-digital-twins/polytope-examples/refs/heads/main/environment.yml`
3. Create the environment (this may take a while) by running `mamba env create -n <myenv> -f environment.yml` if necessary add `-p <path-to-your-environment-folder>` if your environment should be somewhere specific.
4. Activate the environment by running either  `mamba activate <myenv> `or  `mamba activate <path-to-your-environment-folder> `
5. Create a jupyter kernel if you want to use jupyter notebooks by running `python3 -m ipykernel install --name <myenv> --user`


