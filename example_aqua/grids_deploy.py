import os
import argparse
import requests
from aqua.core.configurer import ConfigPath
from aqua.core.util import load_yaml, load_multi_yaml, create_folder
from aqua.core.logger import log_configure


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Deploy AQUA grids for climatedt-gen2 catalog.")
    parser.add_argument(
        "--targetdir",
        type=str,
        required=True,
        help="Path to the directory where the grids will be deployed. The directory will be created if it does not exist.",
    )
    parser.add_argument(
        "--config",
        type=str,
        default="grids_list.yaml",
        help="Path to the yaml file containing the list of grids to be deployed. Default is grids_list.yaml.",
    )
    parser.add_argument(
        "--loglevel",
        type=str,
        default="WARNING",
        help="Logging level. Default is WARNING. Options are: DEBUG, INFO, WARNING, ERROR, CRITICAL.",
    )

    return parser.parse_args()


def extract_grid_info(source_grid_name: str,
                      catalog: str = 'climatedt-gen2',
                      loglevel: str = "WARNING"):
    """
    Find the grid path to be downloaded in the AQUA auxiliary files.

    Args:
        source_grid_name (str): Name of the grid to be deployed, e.g. hpz10-nested
        catalog (str): Name of the catalog to be used, default is climatedt-gen2.
        loglevel (str): Logging level, default is WARNING. Options are: DEBUG, INFO, WARNING, ERROR, CRITICAL.

    Returns:
        list: List of paths to be downloaded for the specified grid.
        Returns an empty list if the grid is not found or if there is an error in the path format.
    """
    logger = log_configure(log_level=loglevel, log_name="Grids deployment - extract grid info")

    # Obtain the grids_folder path where the auxiliary files are stored.
    configurer = ConfigPath(catalog=catalog, loglevel=loglevel)
    _, grids_folder = configurer.get_reader_filenames()

    # Load the grids information from the auxiliary file.
    grids_dict = load_multi_yaml(folder_path=grids_folder,
                                 loglevel=loglevel)

    # Scan the grids_dict for a match with the source_grid_name and extract the grid path.
    if source_grid_name in grids_dict["grids"]:
        logger.info(f"Grid {source_grid_name} found in the auxiliary files.")
        single_dict = grids_dict["grids"][source_grid_name]
        logger.debug(f"Grid {source_grid_name} information: {single_dict}")

        # Extract the path, since multiple paths may be available, the output is always a list.
        # With this method the download can be always handled as a for loop.
        grid_path = single_dict["path"]
        if isinstance(grid_path, str):
            logger.debug(f"Grid {source_grid_name} path: {grid_path}")
            grid_path = [grid_path]  # Convert to list for consistency
        elif isinstance(grid_path, dict):
            logger.debug(f"Grid {source_grid_name} has multiple paths: {grid_path}")
            paths = []
            for key, path in grid_path.items():
                paths.append(path)
            grid_path = paths
        else:
            logger.error(f"Grid {source_grid_name} has an unexpected path format: {grid_path}")
            return []
    else:
        logger.error(f"Grid {source_grid_name} not found in the auxiliary files. Please check the grid name and try again.")
        return []

    # Paths are in the format { SOME_VARIABLE }/path/to/grid, we need to extract the path after the variable.
    extracted_paths = []
    for path in grid_path:
        if "{{" in path and "}}" in path:
            extracted_path = path.split("}}")[1]  # Extract the part after the variable
            logger.debug(f"Extracted path for grid {source_grid_name}: {extracted_path}")
            extracted_paths.append(extracted_path)
        else:
            logger.error(f"Grid {source_grid_name} path format is incorrect: {path}. Expected format is {{ SOME_VARIABLE }}/path/to/grid.")
            return []

    return extracted_paths


def check_directory(grid_path: str,
                    targetdir: str,
                    loglevel: str = "WARNING"):
    """
    Check if the directory exists, if not create it.
    Return the folder + filename to be downloaded.

    Args:
        grid_path (str): Path to the grid directory to be checked/created.
        targetdir (str): Path to the target directory where the grid will be deployed.
        loglevel (str): Logging level, default is WARNING. Options are: DEBUG, INFO, WARNING, ERROR, CRITICAL.

    Returns:
        tuple: A tuple containing the grid directory and the grid name to be downloaded.
    """
    # Grid_path is in the format path/to/gridname.nc, we need to extract the grid name and the parent directory.
    logger = log_configure(log_level=loglevel, log_name="Grids deployment - check directory")
    grid_name = grid_path.split("/")[-1]  # Extract the grid name
    grid_dir = "/".join(grid_path.split("/")[:-1])  # Extract the parent
    # Remove the leading slash if present to avoid issues with os.path.join
    if grid_dir.startswith("/"):
        grid_dir = grid_dir[1:]

    final_dir = os.path.join(targetdir, grid_dir)
    logger.debug(f"Checking if target path {final_dir} exists for grid {grid_name}.")
    create_folder(final_dir, loglevel=loglevel)

    logger.debug(f"Final path to download is {os.path.join(grid_dir, grid_name)}.")
    return grid_dir, grid_name


def download_grid(grid_dir: str,
                  grid_name: str,
                  targetdir: str,
                  bucket: str,
                  loglevel: str = "WARNING"):
    """
    Download the grid from the bucket to the target directory.

    Args:
        grid_dir (str): Directory of the grid to be downloaded, relative to the bucket.
        grid_name (str): Name of the grid file to be downloaded.
        targetdir (str): Path to the main target directory where the grid will be deployed.
        bucket (str): URL of the bucket where the grids are stored.
        loglevel (str): Logging level, default is WARNING. Options are: DEBUG, INFO, WARNING, ERROR, CRITICAL.
    """
    logger = log_configure(log_level=loglevel, log_name="Grids deployment - download grid")
    url = f"{bucket}/{grid_dir}/{grid_name}"
    logger.debug(f"Downloading grid from {url}.")

    final_folder = os.path.join(targetdir, grid_dir)
    final_path = os.path.join(final_folder, grid_name)
    if os.path.exists(final_path):
        logger.info(f"Grid {grid_name} already exists at {final_path}. Skipping download.")
        return

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(final_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    logger.info(f"Grid {grid_name} downloaded successfully to {final_path}.")


if __name__ == "__main__":
    args = parse_args()

    loglevel = args.loglevel
    logger = log_configure(log_level=loglevel, log_name="Grids deployment")
    targetdir = args.targetdir

    logger.warning(f"Deploying AQUA grids for climatedt-gen2 catalog in {targetdir} with log level {loglevel}")

    config = load_yaml(args.config)

    logger.debug(f"Grids to be deployed: {config['source_grid_name']}")
    grids = config["source_grid_name"]
    bucket = "https://lumidata.eu/465000454:aqua-grids/grids"

    for grid in grids:
        logger.info(f"Deploying grid {grid}")
        grid_paths = extract_grid_info(source_grid_name=grid, loglevel=loglevel)

        for grid_path in grid_paths:
            grid_dir, grid_name = check_directory(grid_path=grid_path, targetdir=targetdir, loglevel=loglevel)
            download_grid(grid_dir=grid_dir, grid_name=grid_name, targetdir=targetdir,
                          bucket=bucket, loglevel=loglevel)
