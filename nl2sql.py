import google.generativeai as genai
import sqlite3
import pandas as pd

# Initialize the Gemini client
genai.configure(api_key="AIzaSyBVB_UHH5afm4uLJWlbCfVX6n4il_C0TZU")  # Replace with your actual API key

# Define the database schema
schema = """
Table: customers
Columns: id (INTEGER), name (TEXT), age (INTEGER), job (TEXT), balance (FLOAT), housing (TEXT), loan (TEXT), y (TEXT)
"""

# Define the natural language question
question = "Find all customers with a balance greater than 1000."

# Create the prompt
prompt = f"""
You are a SQL expert. Given the following database schema and question, generate the correct SQL query.

Schema:
{schema}

Question:
{question}

SQL Query:
"""

try:
    # Initialize the model
    model = genai.GenerativeModel("gemini-pro")  # Use the Gemini Pro model

    # Generate the SQL query
    response = model.generate_content(prompt)

    # Extract and clean the SQL query
    sql_query = response.text.strip()
    if sql_query.startswith("```sql") and sql_query.endswith("```"):
        # Remove Markdown formatting
        sql_query = sql_query[6:-3].strip()

    print("Generated SQL Query:")
    print(sql_query)

    # Load your dataset into a SQLite database
    csv_file = "customers.csv"  # Replace with your CSV file path
    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        exit()

    # Connect to an in-memory SQLite database
    with sqlite3.connect(":memory:") as conn:
        # Load the CSV data into the SQLite database
        df.to_sql("customers", conn, if_exists="replace", index=False)

        # Execute the generated SQL query
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()

        # Print the query results
        print("\nQuery Results:")
        for row in results:
            print(row)

except Exception as e:
    print(f"An error occurred: {e}")