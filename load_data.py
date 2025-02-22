import pandas as pd
import sqlite3

def load_and_clean_data(file_path):
    """
    Load and clean the dataset.
    
    Parameters:
        file_path (str): Path to the dataset file.
    
    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    # Load the dataset
    df = pd.read_csv(file_path)

    # Inspect the first few rows
    print("Original Dataset:")
    print(df.head())

    # Clean the dataset (example steps)
    # Drop rows with missing values
    df = df.dropna()

    # Remove duplicates
    df = df.drop_duplicates()

    # Rename columns (if needed)
    # Replace with actual column names from your dataset
    df = df.rename(columns={
        'age': 'age',
        'job': 'job',
        'marital': 'marital',
        'education': 'education',
        'default': 'default',
        'balance': 'balance',
        'housing': 'housing',
        'loan': 'loan',
        'contact': 'contact',
        'day': 'day',
        'month': 'month',
        'duration': 'duration',
        'campaign': 'campaign',
        'pdays': 'pdays',
        'previous': 'previous',
        'poutcome': 'poutcome',
        'y': 'y'
    })

    # Save the cleaned dataset (optional)
    df.to_csv('cleaned_banking_dataset.csv', index=False)

    return df

def store_data_in_db(df, db_name='banking.db', table_name='transactions'):
    """
    Store the cleaned dataset in a SQLite database.
    
    Parameters:
        df (pd.DataFrame): The cleaned DataFrame.
        db_name (str): Name of the SQLite database file.
        table_name (str): Name of the table to store the data.
    """
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create a table
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique ID for each row
            age INTEGER,                          -- Age of the customer
            job TEXT,                             -- Job of the customer
            marital TEXT,                         -- Marital status
            education TEXT,                       -- Education level
            "default" TEXT,                         -- Has credit in default?
            balance INTEGER,                      -- Average yearly balance
            housing TEXT,                         -- Has housing loan?
            loan TEXT,                            -- Has personal loan?
            contact TEXT,                         -- Contact communication type
            day INTEGER,                          -- Last contact day of the month
            month TEXT,                           -- Last contact month of the year
            duration INTEGER,                     -- Last contact duration (in seconds)
            campaign INTEGER,                     -- Number of contacts performed during this campaign
            pdays INTEGER,                        -- Number of days since the last contact
            previous INTEGER,                     -- Number of contacts performed before this campaign
            poutcome TEXT,                        -- Outcome of the previous marketing campaign
            y TEXT                                -- Has the client subscribed to a term deposit?
        )
    ''')

    # Insert data from the cleaned DataFrame
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print(f"Data stored in {db_name} in table {table_name}.")