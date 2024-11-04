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


@app.route('/api/supply/borrowing', methods=['GET'])
def get_all_loaned():
    user_id = request.args.get("userid")

    query = """
    SELECT u.DODID, u.LastName, u.FirstName, s.NSN, s.Name, s.Serial_Num, b.Count, b.Checkout_Date
    FROM Supply as s
    JOIN Borrowing AS b ON s.ID = b.Item_ID
    JOIN User AS u ON b.Lender_DODID = u.DODID
    WHERE u.DODID = ?
    """

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    supplies = [dict(row) for row in rows]

    return jsonify(supplies), 200

if __name__ == "__main__":
    app.run(debug=True)
