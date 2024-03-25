import os
from scripts.process_csv import   process_file, log_processed_file, read_processed_log, get_verified_email

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