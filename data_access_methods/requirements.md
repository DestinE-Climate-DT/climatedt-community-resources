## Set up your python environment and access permissions
Here we describe how to create a python environment with all required packages to run the [Simplified use cases](#examples).

### 1. Creating python environment 

```python3 -m venv .venv```
```source .venv/bin/activate```

Make sure the Python 3.10 or higher. You can check your version with ```python3 --version```. Then install the dependencies:

```pip install -r requirements.txt```

### 2. Authentication

**Note:** Upgraded access to the DestinE data platform is required for data access and must be requested via https://platform.destine.eu/access-policy-upgrade/ and one must abide by the DestinE data policies.

Each ```*_use_case.ipynb``` specifies how the authenticate process works for every data access method.  

