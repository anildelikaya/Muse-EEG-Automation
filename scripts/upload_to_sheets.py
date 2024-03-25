import gspread  # interact with Google Sheets, high-level api on low-level operation you can perform on google sheets
from google.oauth2.service_account import Credentials  # to authenticate with Google Sheets

# scopes = ["https://www.googleapis.com/auth/spreadsheets"  ] # to read and write to Google Sheets
# credentials = Credentials.from_service_account_file("./credentials/credentials.json", scopes=scopes) # to authenticate with Google Sheets
# client = gspread.authorize(credentials) # to interact with Google Sheets

# sheet_id = "1zuRaVnBL3kEQH9UU2V9lXaAG_mKZZ9-d17LDQH6N1XM"
# workbook = client.open_by_key(sheet_id) # open the sheet by its id

# sheet = workbook.worksheet('Sheet1') # open the sheet by its name
# # sheet.update_title('Sheet1') # update the title of the sheet
# sheet.update_cell(1, 1, "Hello, World!") # update the cell at row 1, column 1



sheet_id = "1zuRaVnBL3kEQH9UU2V9lXaAG_mKZZ9-d17LDQH6N1XM"
scopes = ["https://www.googleapis.com/auth/spreadsheets"  ] # to read and write to Google Sheets
# Function to authenticate with Google Sheets and return a client
def authenticate_gsheets():
    """
    Authenticate with Google Sheets using google-auth library and return a gspread client.
    """
    credentials = Credentials.from_service_account_file("./credentials/credentials.json", scopes=scopes)
    client = gspread.authorize(credentials)
    return client

# Function to upload DataFrame to a specific Google Sheet and worksheet
def upload_to_sheet(df, sheet_id):
    """
    Uploads a DataFrame to a specific worksheet in a Google Sheet by sheet ID.
    
    Parameters:
    - df: The pandas DataFrame to upload.
    - sheet_id: The ID of the Google Sheet.
    - worksheet_name: The name of the worksheet in the Google Sheet.
    """
    df['TimeStamp'] = df['TimeStamp'].dt.strftime("%Y-%m-%d %H:%M:%S")
    client = authenticate_gsheets()
    sheet = client.open_by_key(sheet_id).worksheet('Sheet1')
    
      # Check if the sheet is empty by trying to get the header row
    try:
        headers = sheet.row_values(1)
        sheet_is_empty = not bool(headers)
    except gspread.exceptions.APIError:
        # If there's an API error, assume the sheet might be empty or access is incorrect
        sheet_is_empty = True
    
    # Find the first empty row in the worksheet
    first_empty_row = len(sheet.get_all_values()) + 1
    
    # If the sheet is empty, include the headers with the data
    if sheet_is_empty:
        # values = [df.columns.tolist()] + df.values.tolist()
        # sheet.update(f'A{1}', values, value_input_option='USER_ENTERED')
        values = [df.columns.tolist()] 
        sheet.update(f'A{1}', values, value_input_option='USER_ENTERED')
        values =  df.values.tolist()
        sheet.update(f'A{2}', values, value_input_option='USER_ENTERED')
    else:
        values = df.values.tolist()
        sheet.update(f'A{first_empty_row}', values, value_input_option='USER_ENTERED')
    
    # Append the data starting from the first empty row
    

    print(f"Data uploaded to Google Sheet with ID '{sheet_id}' in worksheet 'Sheet1'.")