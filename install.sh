#!/bin/bash

# Check if pipenv is installed
if ! command -v pipenv &> /dev/null
then
    echo "pipenv could not be found, installing..."
    pip install pipenv
fi

# Automatically determine the path to the script and navigate to the project directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Assuming the script is located at the root of your project,
# no further navigation is required

# Install dependencies using pipenv
pipenv install

echo "Setup completed successfully."
