# Muse headband EEG Data Automation and  Visualization 

A Python-based automation tool for processing EEG data from Muse headbands, transforming it into cognitive metrics for creativity, relaxation, and awareness. The processed data is uploaded to Google Sheets, enabling easy visualization and analysis in Looker Studio. This project simplifies the workflow for researchers and enthusiasts working with EEG data, providing insights into brain activity patterns and cognitive states.

This project facilitates the visualization of cognitive metrics by processing EEG data from Muse headband CSV files and uploading the processed data to Google Sheets. The data is then visualized using Looker Studio, offering insights into various cognitive states such as creativity, relaxation, inward and outward awareness, and displaying EEG frequency powers and Heart Rate Variability (HRV) over time.

## Project Overview

The script automates the transformation of raw EEG data into meaningful metrics that can be easily visualized in Looker Studio. Key features include:

- **Creativity and Relaxation Metrics:** Calculations based on EEG frequency bands to gauge creativity and relaxation levels.
- **Inward and Outward Awareness:** Metrics derived from EEG data to assess states of inward and outward focus.
- **EEG Frequency Powers:** Visualization of different EEG frequency bands (Delta, Theta, Alpha, Beta, Gamma) over time to monitor brain activity.
- **Heart Rate Variability (HRV):** Displaying HRV over time as an indicator of physiological stress and emotional regulation.

## Project Structure
```bash
project_root/
│
├── data/
│ ├── raw/ # Directory for storing raw CSV files
│ └── processed/ # Directory for processed data
│
├── scripts/
│ ├── process_csv.py # Script for processing CSV files
│ ├── upload_to_sheets.py # Script for uploading data to Google Sheets
│ └── data_transformations.py # Contains functions for data cleaning and transformations
│
├── main.py # Main script that orchestrates processing and uploading
├── install.sh # Shell script for setting up the environment on macOS/Linux
├── run_script.sh # Shell script for running the project on macOS/Linux
├── credentials/
│ └── google_api_credentials.json # Credentials for Google Sheets API
└── README.md # This documentation file
```


## Setup Instructions

### Prerequisites

- Python 3 and pip (Python package manager)
- Xcode Command Line Tools (macOS) or build-essential (Linux) for compiling dependencies

### Installation

#### macOS

1. **Install Xcode Command Line Tools:** Open Terminal and run:
   ```bash
   xcode-select --install
   ```

2. **Run Install Script:** Navigate to the project directory and execute:
   ```bash
   ./install.sh
   ```

#### Linux

1. **Install build-essential:** Open Terminal and run:
   ```bash
   sudo apt update
   sudo apt install build-essential
   ```

2. **Run Install Script:** Navigate to the project directory and execute:
   ```bash
   ./install.sh
   ```

## Running the Application

Execute `run_script.sh` to process raw EEG CSV files and upload them to Google Sheets for visualization.

## Usage

- **Prepare Data:** Place Muse headband CSV files in `data/raw/`.
- **Execute Script:** Double-click `run_script.sh` or run it from the terminal.
- **Visualize in Looker Studio:** Access the uploaded data in Google Sheets as a data source in Looker Studio.

## Customization

Modify scripts in the `scripts/` directory to adjust data processing and uploading logic as needed for your specific visualization requirements in Looker Studio.

## Troubleshooting

- Ensure scripts have executable permissions: `chmod +x install.sh run_script.sh`.
- Verify that Xcode Command Line Tools (macOS) or build-essential (Linux) are installed for dependency management.

## Contributing

Contributions are welcome! Please submit pull requests for enhancements.

## License

MIT License - [Anıl Berk Delikaya]

https://github.com/anildelikaya/Muse-EEG-Automation/assets/48909776/d57a7235-29ad-454a-989f-d3dada5f8c85
