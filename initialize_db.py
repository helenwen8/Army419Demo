import sqlite3

def initialize_db(db_path="pinecone.db"):
    with open("schema.sql") as f:
        schema = f.read()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executescript(schema)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    initialize_db()

