from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_apscheduler import APScheduler
import sqlite3
from datetime import datetime
from dateutil.relativedelta import relativedelta
import smtplib, ssl

from email_templates import loan_reminder_template


app = Flask(__name__)
app.secret_key = "supersecretkey"
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Configuration for APScheduler
class Config:
    SCHEDULER_API_ENABLED = True

app.config.from_object(Config)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

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

    # default ORDER BY borrowID ASC, implemented in supplyData.js
    sort_column = request.args.get("sort")
    sort_order = request.args.get("order")

    query = f"""
    SELECT b.Borrowing_ID as borrowID, u2.DODID, u2.LastName as LastName, u2.FirstName as FirstName, s.NSN, s.Name as Name, s.Serial_Num, b.Count as Count, b.Checkout_Date as Checkout_Date, b.Last_Renewed_Date, b.Due_Date, b.Return_Date
    FROM Supply as s
    JOIN Borrowing AS b ON s.ID = b.Item_ID
    JOIN User AS u1 ON b.Lender_DODID = u1.DODID
    JOIN User AS u2 ON b.Borrower_DODID = u2.DODID
    WHERE u1.DODID = ?
    ORDER BY {sort_column} {sort_order}
    """ 

    print(sort_column, sort_order, user_id)
    print(query)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, (str(user_id), ))
    rows = cursor.fetchall()
    conn.close()
    supplies = [dict(row) for row in rows]

    return jsonify(supplies), 200

@app.route('/api/supply/borrowing', methods=['GET'])
def get_all_borrowed():
    user_id = request.args.get("userid")
    print(user_id)

    # default ORDER BY borrowID ASC, implemented in supplyData.js
    sort_column = request.args.get("sort")
    sort_order = request.args.get("order")

    query = f"""
    SELECT b.Borrowing_ID as borrowID, u1.DODID, u1.LastName, u1.FirstName as LastName, s.NSN, s.Name, s.Serial_Num, b.Count, b.Checkout_Date, b.Last_Renewed_Date, b.Due_Date, b.Return_Date
    FROM Supply as s
    JOIN Borrowing AS b ON s.ID = b.Item_ID
    JOIN User AS u1 ON b.Lender_DODID = u1.DODID
    JOIN User AS u2 ON b.Borrower_DODID = u2.DODID
    WHERE u2.DODID = ?
    ORDER BY {sort_column} {sort_order}
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

@app.route('/api/supply/renew', methods=['POST'])
def renew_item():
    data = request.json
    borrowing_id = data.get("borrowing_id")
    initials = data.get("initials")
    print(data)

    if not borrowing_id or not initials:
        return jsonify({"success": False, "message": "Borrowing ID and initials are required."}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Update the Last_Renewed_Date in the Borrowing table
        current_datetime = datetime.now().strftime("%Y-%m-%d")
        new_due_date = (datetime.now() + relativedelta(months=+1)).strftime("%Y-%m-%d")
        cursor.execute(
            """
            UPDATE Borrowing
            SET Last_Renewed_Date = ?, Due_Date = ?, Borrower_Initials = ?
            WHERE Borrowing_ID = ?
            """,
            (current_datetime, new_due_date, initials, borrowing_id)
        )
        conn.commit()
        conn.close()

        if cursor.rowcount == 0:
            return jsonify({"success": False, "message": "No matching borrowing record found."}), 404

        return jsonify({"success": True, "message": "Borrowing record successfully renewed."}), 200

    except Exception as e:
        print(f"Error renewing borrowing record: {e}")
        return jsonify({"success": False, "message": "Internal server error."}), 500




def get_users_with_upcoming_loans():
    query =  """
    SELECT u.DODID, u.FirstName, u.LastName, u.Email
    FROM User as u
    JOIN Borrowing as b ON u.DODID = b.Borrower_DODID
    WHERE DATE('now', '+3 days') >= b.Due_Date
    GROUP BY u.DODID, u.FirstName, u.LastName, u.Email
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return users

def send_email_reminder(dodid, first_name, last_name, email):
    print(dodid)
    query = """
    SELECT i.Name, i.NSN, i.Serial_Num, b.Due_Date
    FROM Borrowing AS b
    JOIN Supply AS i ON b.Item_ID = i.ID
    WHERE b.Borrower_DODID = ? and DATE('now', '+3 days') >= b.Due_Date"""

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, (dodid,))
    items = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    body = loan_reminder_template(f"{first_name} {last_name}", items)

    # Send email
    sender = "pinecone.emailnotifications@gmail.com"
    password = "kjqq bnrz otfc gdpn"

    port = 465  # For SSL

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, email, body)



def send_email_reminders():
    users = get_users_with_upcoming_loans()
    print("users:", users)

    for user in users:
        print("email", user.get("Email"))
        send_email_reminder(user.get("DODID"), user.get("FirstName"), user.get("LastName"), user.get("Email"))


@scheduler.task('cron', id='reminder_email', hour=9)
def send_reminders():
    send_email_reminders()
    return 

@app.route('/api/test_send_reminders', methods=['POST'])
def test_send_reminders():
    send_reminders()
    return jsonify({"success": True}), 200

if __name__ == "__main__":
    app.run(debug=True)

