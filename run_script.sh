#!/bin/bash

# Automatically determine the path to the script and navigate to the project directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Activate the pipenv environment and run the process_csv.py script
pipenv run python scripts/process_csv.py

echo "Script execution completed."
