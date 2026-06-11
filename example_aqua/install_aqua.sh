#!/bin/bash

# Activate the conda environment for AQUA
conda activate aquarium

# Install AQUA auxiliary files
yes | aqua install <machine-name>

# Install the climatedt-gen2 catalog
aqua add climatedt-gen2

# Set up the path for grids deployment
aqua grids set <path-to-preferred-grid-folder>

grids=(
	hpz7-nested
	hpz9-nested
	hpz10-nested
	lon-lat-r100
	icon-R02B09-hpz7-nested-v3
	icon-R02B09-hpz7-nested-3d-v3
	icon-R02B09-hpz10-nested-v3
	icon-R02B09-hpz10-nested-3d-v3
	fesom-NG5-hpz7-nested-v3
	fesom-NG5-hpz7-nested-v4
	fesom-NG5-hpz7-nested-3d-v3
	fesom-NG5-hpz7-nested-3d-v4
	fesom-NG5-hpz9-nested-v4
	fesom-NG5-hpz9-nested-3d-v4
	fesom-NG5-hpz10-nested-v3
	fesom-NG5-hpz10-nested-3d-v3
	nemo-eORCA12-hpz7-nested-v3
	nemo-eORCA12-hpz7-nested-3d-v3
	nemo-eORCA12-hpz9-nested-v3
	nemo-eORCA12-hpz9-nested-3d-v3
	nemo-eORCA12-hpz10-nested-v3
	nemo-eORCA12-hpz10-nested-3d-v3
)

for grid in "${grids[@]}"; do
    aqua grids deploy $grid
done