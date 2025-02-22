from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import pandas as pd
import google.generativeai as genai

app = Flask(__name__)

# Initialize the Gemini client
genai.configure(api_key="AIzaSyBVB_UHH5afm4uLJWlbCfVX6n4il_C0TZU")  # Replace with your actual API key

# Define the database schema
schema = """
Table: customers
Columns: id (INTEGER), name (TEXT), age (INTEGER), job (TEXT), balance (FLOAT), housing (TEXT), loan (TEXT), y (TEXT)
"""

# Serve the frontend
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

# Handle NL2SQL requests
@app.route('/nl2sql', methods=['POST'])
def nl2sql():
    """
    Endpoint to handle NL2SQL requests.
    """
    try:
        data = request.json
        query = data.get('query')  # Get the natural language query from the request

        if not query:
            return jsonify({"error": "No query provided"}), 400

        # Generate SQL from the query
        sql_query = generate_sql(query)

        # Execute the SQL query on the database
        result = execute_sql_query(sql_query)

        # Return the SQL query and results
        return jsonify({
            "sql_query": sql_query,
            "result": result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def generate_sql(query):
    """
    Generate an SQL query from a natural language query using the Gemini API.
    """
    try:
        # Initialize the model
        model = genai.GenerativeModel("gemini-pro")  # Use the Gemini Pro model

        # Create the prompt
        prompt = f"""
        You are a SQL expert. Given the following database schema and question, generate the correct SQL query.

        Schema:
        {schema}

        Question:
        {query}

        SQL Query:
        """

        # Generate the SQL query
        response = model.generate_content(prompt)

        # Extract and clean the SQL query
        sql_query = response.text.strip()
        if sql_query.startswith("```sql") and sql_query.endswith("```"):
            sql_query = sql_query[6:-3].strip()

        return sql_query
    except Exception as e:
        raise Exception(f"Error generating SQL query: {e}")

def execute_sql_query(sql_query):
    """
    Execute the SQL query on a SQLite database loaded from a CSV file.
    """
    try:
        # Load your dataset into a SQLite database
        csv_file = "customers.csv"  # Replace with your CSV file path
        df = pd.read_csv(csv_file)

        # Connect to an in-memory SQLite database
        with sqlite3.connect(":memory:") as conn:
            # Load the CSV data into the SQLite database
            df.to_sql("customers", conn, if_exists="replace", index=False)

            # Execute the generated SQL query
            cursor = conn.cursor()
            cursor.execute(sql_query)
            results = cursor.fetchall()

        return results
    except Exception as e:
        raise Exception(f"Error executing SQL query: {e}")

if __name__ == '__main__':
    app.run(debug=True)