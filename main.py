from load_data import load_and_clean_data, store_data_in_db

# Load and clean the dataset
file_path = r'extracted_data\\train.csv'  # Use raw string or forward slashes
cleaned_df = load_and_clean_data(file_path)

# Store the cleaned dataset in a database
store_data_in_db(cleaned_df, db_name='banking.db', table_name='transactions')