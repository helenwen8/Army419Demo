import sqlite3

def get_db_connection(db_path="pinecone.db"):
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  
    return conn

def fetch_all_supply(db_path="pinecone.db"):
    """Fetches all records from the Supply table."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Supply")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]  # Convert rows to dictionaries for easier handling

def fetch_all_users(db_path="pinecone.db"):
    """Fetches all records from the User table."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def fetch_all_borrowing(db_path="pinecone.db"):
    """Fetches all records from the Borrowing table."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Borrowing")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Example usage
if __name__ == "__main__":
    # Fetch and print all records from each table
    supply_data = fetch_all_supply()
    user_data = fetch_all_users()
    borrowing_data = fetch_all_borrowing()
    
    print("Supply Data:")
    for record in supply_data:
        print(record)
    
    print("\nUser Data:")
    for record in user_data:
        print(record)
    
    print("\nBorrowing Data:")
    for record in borrowing_data:
        print(record)
