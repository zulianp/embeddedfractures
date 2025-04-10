#!/bin/bash

# Stop on error
set -e

# Create virtual environment in ./venv
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install package in editable mode
pip install -e .

echo "Virtual environment 'venv' created and package installed in editable mode."
