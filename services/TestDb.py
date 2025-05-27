import sqlite3

conn = sqlite3.connect('appointments.db')
cursor = conn.cursor()

table_name = 'appointments'

cursor.execute("""
    SELECT name FROM sqlite_master 
    WHERE type='table' AND name=?;
""", (table_name,))

if cursor.fetchone():
    print(f"Table '{table_name}' exists.")
else:
    print(f"Table '{table_name}' does NOT exist.")

cursor.execute("SELECT * FROM available_slots;")
rows = cursor.fetchall()
print(rows)