from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("pinecone.db")
    conn.row_factory = sqlite3.Row  # Fetch rows as dictionaries
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/supply', methods=['POST'])
def add_supply():
    data = request.json
    nsn = data.get("NSN")
    name = data.get("Name")
    serial_num = data.get("Serial_Num")
    description = data.get("Description")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Supply (NSN, Name, Serial_Num, Description) VALUES (?, ?, ?, ?)",
        (nsn, name, serial_num, description)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Item added to Supply table"}), 201

@app.route('/api/supply/all', methods=['GET'])
def get_all_supplies():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Supply")
    rows = cursor.fetchall()
    conn.close()
    supplies = [dict(row) for row in rows]
    return jsonify(supplies), 200

if __name__ == "__main__":
    app.run(debug=True)
