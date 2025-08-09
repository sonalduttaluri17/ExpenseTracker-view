import mysql.connector
from mysql.connector import Error

HOST = "localhost"
USER = "root"
PASSWORD = "Sonal.17"
DB_NAME = "expense_tracker"

TABLE_SQL = """
CREATE TABLE IF NOT EXISTS expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    category VARCHAR(100) NOT NULL,
    date DATE NOT NULL
);
"""

def main():
    try:
        conn = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.execute(f"USE {DB_NAME}")
        cursor.execute(TABLE_SQL)
        conn.commit()
        cursor.close()
        conn.close()
        print("Database and table ready (`expense_tracker`.expenses).")
    except Error as e:
        print("Error creating database/table:", e)

if __name__ == "__main__":
    main()
