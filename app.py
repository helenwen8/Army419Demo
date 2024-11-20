from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import sqlite3


app = Flask(__name__)
app.secret_key = "supersecretkey"
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"


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
    identifier = request.args.get("identifier", "") + "%"  # Default to an empty string if 'identifier' is not provided

    query = """
    SELECT ID, NSN, Name, Serial_Num, Description
    FROM Supply
    WHERE NSN LIKE ? OR Name LIKE ? OR Serial_Num LIKE ?
    """

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, (identifier, identifier, identifier))
    rows = cursor.fetchall()
    conn.close()
    supplies = [dict(row) for row in rows]

    return jsonify(supplies), 200


# app.run(debug=True)

@app.route('/api/borrow', methods=['POST'])
def add_borrow():
    print(f"Current user ID: {current_user.id}")
    data = request.json
    print(f"Received data: {data}")
    item = data.get("item")
    lender = data.get("lender")
    borrower = data.get("borrower")
    count = data.get("count")
    reason = data.get("reason")
    date = data.get("date")
    # date = None
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

@app.route('/api/users', methods=['GET'])
def get_users():
    query = request.args.get("query", "")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DODID, FirstName, LastName FROM User WHERE DODID LIKE ?", (f"%{query}%",))
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(users), 200


@app.route('/api/supply/loaned', methods=['GET'])
def get_all_loaned():
    user_id = request.args.get("userid")
    print(user_id)

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
    cursor.execute(query, (str(user_id),))
    rows = cursor.fetchall()
    print(rows)
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

class User(UserMixin):
    def __init__(self, id, first_name, last_name, email):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User WHERE DODID = ?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        return User(user_data["DODID"], user_data["FirstName"], user_data["LastName"], user_data["Email"])
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User WHERE Email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user["Password"], password):
            user_obj = User(user["DODID"], user["FirstName"], user["LastName"], user["Email"])
            login_user(user_obj)
            return redirect(url_for('index'))
        else:
            return "Invalid credentials", 401

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        dodid = request.form['dodid']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        # Validate that DODID and email are unique
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User WHERE DODID = ? OR Email = ?", (dodid, email))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return "DODID or Email is already registered", 400

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Insert the new user into the database
        cursor.execute(
            "INSERT INTO User (DODID, FirstName, LastName, Email, Phone, Password) VALUES (?, ?, ?, ?, ?, ?)",
            (dodid, first_name, last_name, email, phone, hashed_password)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/profile/<user_id>')
@login_required
def profile(user_id):
    if user_id != current_user.id:
        return "Unauthorized", 403

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User WHERE DODID = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return render_template('profile.html', user=dict(user))
    else:
        return "User not found", 404


if __name__ == "__main__":
    app.run(debug=True)
