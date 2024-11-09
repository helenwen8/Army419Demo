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

@app.route('/borroweditems')
def borrowedItems():
    return render_template('borrowedItems.html')

@app.route('/newitem')
def newItem():
    return render_template('newItem.html')

@app.route('/newborrow')
def newBorrow():
    return render_template('newBorrow.html')

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

@app.route('/api/supplybyidentifier', methods=['GET'])
def get_supply():
    identifier = request.args.get("identifier") + "%"

    query = """
    SELECT ID, NSN, Name, Serial_Num, Description
    FROM Supply
    WHERE NSN LIKE ? or Name LIKE ? or Serial_Num LIKE ?
    """

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, (identifier, identifier, identifier))
    rows = cursor.fetchall()
    conn.close()
    supplies = [dict(row) for row in rows]

    return jsonify(supplies), 200

@app.route('/api/borrow', methods=['POST'])
def add_borrow():
    data = request.json
    item = data.get("item")
    lender = data.get("lender")
    borrower = data.get("borrower")
    count = data.get("count")
    reason = data.get("reason")
    date = data.get("date")
    initials = data.get("initials")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO Borrowing 
        (Item_ID, Lender_DODID, Borrower_DODID, Count, Reason, Checkout_Date, Last_Renewed_Date, Borrower_Initials) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (item, lender, borrower, count, reason, date, "", initials)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Item added to Borrowing table"}), 201


@app.route('/api/supply/loaned', methods=['GET'])
def get_all_loaned():
    user_id = request.args.get("userid")

    query = """
    SELECT u2.DODID, u2.LastName, u2.FirstName, s.NSN, s.Name, s.Serial_Num, b.Count, b.Checkout_Date, b.Last_Renewed_Date
    FROM Supply as s
    JOIN Borrowing AS b ON s.ID = b.Item_ID
    JOIN User AS u1 ON b.Lender_DODID = u1.DODID
    JOIN User AS u2 ON b.Borrower_DODID = u2.DODID
    WHERE u1.DODID = ?
    """

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    supplies = [dict(row) for row in rows]

    return jsonify(supplies), 200

@app.route('/api/supply/borrowing', methods=['GET'])
def get_all_borrowed():
    user_id = request.args.get("userid")

    query = """
    SELECT u1.DODID, u1.LastName, u1.FirstName, s.NSN, s.Name, s.Serial_Num, b.Count, b.Checkout_Date, b.Last_Renewed_Date
    FROM Supply as s
    JOIN Borrowing AS b ON s.ID = b.Item_ID
    JOIN User AS u1 ON b.Lender_DODID = u1.DODID
    JOIN User AS u2 ON b.Borrower_DODID = u2.DODID
    WHERE u2.DODID = ?
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
