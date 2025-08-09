import csv
from db import get_connection

CSV_PATH = "expenses.csv"

def main():
    conn = get_connection()
    cursor = conn.cursor()
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
        for row in rows:
            if len(row) < 3:
                continue
            name, amount, category = row[0].strip(), row[1].strip(), row[2].strip()
            try:
                amount_val = float(amount)
            except:
                continue
            cursor.execute("INSERT INTO expenses (name, amount, category, date) VALUES (%s, %s, %s, CURDATE())",
                           (name, amount_val, category))
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Imported CSV to DB.")

if __name__ == "__main__":
    main()
