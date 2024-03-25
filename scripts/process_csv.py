import os
import pandas as pd
from data_transformations_copy import clean_and_transform_data
from upload_to_sheets import upload_to_sheet, sheet_id



def get_verified_email():
    """
    Prompts the user to enter their email address and verifies it.
    
    Returns:
        The verified email address.
    """
    while True:
        email = input("Please enter your email address for this file: ")
        confirmation = input(f"You entered '{email}'. Is this correct? (yes/no): ").strip().lower()
        if confirmation == 'yes':
            return email
        else:
            print("Let's try entering the email address again.")

def read_processed_log():
    """
    Reads the log file that contains the names of processed files and their associated emails.
    Returns a dictionary where keys are file names and values are emails.
    """
    processed_files = {}
    try:
        with open('logs/processed_files.log', 'r') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 2:
                    processed_files[parts[0]] = parts[1]
        return processed_files
    except FileNotFoundError:
        return {}

def log_processed_file(file_name, email):
    """
    Adds the given file name and email to the log of processed files.
    """
    with open('logs/processed_files.log', 'a') as file:
        file.write(f"{file_name}|{email}\n")


def process_file(file_path, email):
    # Load the CSV file
    df = pd.read_csv(file_path)
    df['TimeStamp'] = pd.to_datetime(df['TimeStamp'])
    
    # Clean and transform the data
    df = clean_and_transform_data(df)
    
    # Perform your data cleaning and transformations here
    df['Email'] = email
    
    # Define the path for the processed file
    processed_path = f"data/processed/processed_{os.path.basename(file_path)}"
    
    # Save the processed DataFrame
    df.to_csv(processed_path, index=False)
    print(f"Processed file saved to {processed_path}")
    # Upload the processed DataFrame to Google Sheets
    upload_to_sheet(df, sheet_id)

def main():
    raw_folder = 'data/raw/'
    processed_files = read_processed_log()
    
    for file_name in os.listdir(raw_folder):
        if file_name.endswith('.csv') and file_name not in processed_files:
            file_path = os.path.join(raw_folder, file_name)
            print(f"Processing {file_name}...")
            email = get_verified_email()
            process_file(file_path, email)
            log_processed_file(file_name, email)
        else:
            print(f"Skipping {file_name}, already processed or not a CSV file.")



if __name__ == "__main__":
    main()