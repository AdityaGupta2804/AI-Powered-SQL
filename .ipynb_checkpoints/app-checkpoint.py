from flask import Flask, request, jsonify
from nl2sql import generate_sql, execute_sql_query

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)