import sqlite3

def init_db():
    with sqlite3.connect("appointments.db") as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS appointments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_name TEXT,
                    doctor_name TEXT,
                    date TEXT,
                    time TEXT,
                    contact TEXT
                )
            """)
            # Add to your init_db() function
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS doctors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                specialization TEXT,
                contact TEXT
            )
            """)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS available_slots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doctor_name TEXT,
                date TEXT,
                time TEXT
            )
            """)
            cursor.execute(""" Delete from available_slots """)
            cursor.execute(""" Insert into available_slots (doctor_name, date, time) values ('Smith', '2025-05-25', '09:00') """)
            cursor.execute(""" Insert into available_slots (doctor_name, date, time) values ('Smith', '2025-05-25', '10:00') """)
            cursor.execute(""" Insert into available_slots (doctor_name, date, time) values ('Smith', '2025-05-25', '11:00') """)
            cursor.execute(""" Insert into available_slots (doctor_name, date, time) values ('Smith', '2025-05-25', '12:00') """)
            cursor.execute(""" Insert into available_slots (doctor_name, date, time) values ('Smith', '2025-05-25', '13:00') """)
            cursor.execute(""" Insert into available_slots (doctor_name, date, time) values ('Smith', '2025-05-25', '14:00') """)
            cursor.execute(""" Insert into available_slots (doctor_name, date, time) values ('Smith', '2025-05-25', '15:00') """)
            cursor.execute(""" Insert into available_slots (doctor_name, date, time) values ('Smith', '2025-05-25', '16:00') """)
            cursor.execute(""" Insert into available_slots (doctor_name, date, time) values ('Smith', '2025-05-25', '17:00') """)
            cursor.execute(""" Insert into available_slots (doctor_name, date, time) values ('Smith', '2025-05-25', '18:00') """)
            cursor.execute(""" Insert into available_slots (doctor_name, date, time) values ('Smith', '2025-05-26', '19:00') """)
            cursor.execute(""" Insert into available_slots (doctor_name, date, time) values ('Smith', '2025-05-26', '09:00') """)
            cursor.execute(""" Insert into available_slots (doctor_name, date, time) values ('Smith', '2025-05-26', '10:00') """)
            cursor.execute(""" Insert into available_slots (doctor_name, date, time) values ('Smith', '2025-05-26', '11:00') """)
            # cursor.execute("""
            #     CREATE TABLE IF NOT EXISTS availability (
            #         doctor_name TEXT,
            #         date TEXT,
            #         time TEXT,
            #         PRIMARY KEY (doctor_name, date, time)
            #     )
            # """)
            conn.commit()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(tables)
        except sqlite3.Error as e:
            print(f"An error occurred while initializing the database: {e}")

def get_connection():
    return sqlite3.connect("appointments.db")
