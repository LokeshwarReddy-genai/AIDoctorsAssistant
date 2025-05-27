import json
from services.db import get_connection

def book_appointment(patient_name, doctor_name, date, time, contact):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM available_slots WHERE doctor_name like? AND date=? AND time=?",
                       (doctor_name, date, time))
        if not cursor.fetchone():
            return f"Dr. {doctor_name} is not available at {time} on {date}."

        cursor.execute("DELETE FROM available_slots WHERE doctor_name like? AND date=? AND time=?",
                       (doctor_name, date, time))
        cursor.execute("INSERT INTO appointments (patient_name, doctor_name, date, time, contact) VALUES (?, ?, ?, ?, ?)",
                       (patient_name, doctor_name, date, time, contact))
        appt_id = cursor.lastrowid
        conn.commit()
        return f"✅ Appointment booked with Dr. {doctor_name} on {date} at {time}."            

def cancel_appointment(appointment_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT doctor_name, date, time FROM appointments WHERE id=?", (appointment_id,))
        row = cursor.fetchone()
        if not row:
            return "Appointment ID not found."

        doctor_name, date, time = row
        cursor.execute("DELETE FROM appointments WHERE id=?", (appointment_id,))
        cursor.execute("INSERT INTO available_slots (doctor_name, date, time) VALUES (?, ?, ?)",
                       (doctor_name, date, time))
        conn.commit()
        return f"Appointment APT-{appointment_id} has been cancelled."

def reschedule_appointment(appointment_id, new_date, new_time):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT doctor_name, date, time FROM appointments WHERE id=?", (appointment_id,))
        row = cursor.fetchone()
        if not row:
            return "Appointment ID not found."

        doctor_name, old_date, old_time = row
        cursor.execute("SELECT 1 FROM available_slots WHERE doctor_name=? AND date=? AND time=?",
                       (doctor_name, new_date, new_time))
        if not cursor.fetchone():
            return f"Dr. {doctor_name} is not available at {new_time} on {new_date}."

        cursor.execute("UPDATE appointments SET date=?, time=? WHERE id=?", (new_date, new_time, appointment_id))
        cursor.execute("DELETE FROM available_slots WHERE doctor_name=? AND date=? AND time=?",
                       (doctor_name, new_date, new_time))
        cursor.execute("INSERT INTO available_slots (doctor_name, date, time) VALUES (?, ?, ?)",
                       (doctor_name, old_date, old_time))
        conn.commit()
        return f"Appointment APT-{appointment_id} rescheduled to {new_date} at {new_time}."

def check_availability(doctor_name, date):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT time FROM available_slots WHERE doctor_name like ? AND date=?", (doctor_name, date))
        times = [row[0] for row in cursor.fetchall()]
        print (times)
        if not times:
            return f"Dr. {doctor_name} is not available on {date}."
        return f"Dr. {doctor_name} is available on {date} at: {', '.join(times)}"

def register_doctor(name, specialization, contact):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO doctors (name, specialization, contact) VALUES (?, ?, ?)",
            (name, specialization, contact)
        )
        conn.commit()
        return f"Doctor {name} registered successfully."

def add_doctor_availability(doctor_name, date, time):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO available_slots (doctor_name, date, time) VALUES (?, ?, ?)",
            (doctor_name, date, time)
        )
        conn.commit()
        return f"Availability added for Dr. {doctor_name} on {date} at {time}."

def dispatch_function(name, arguments):
    args = json.loads(arguments)
    if name == "book_appointment":
        return book_appointment(**args)
    elif name == "cancel_appointment":
        return cancel_appointment(int(args["appointment_id"]))
    elif name == "reschedule_appointment":
        return reschedule_appointment(int(args["appointment_id"]), args["new_date"], args["new_time"])
    elif name == "check_availability":
        return check_availability(**args)
    elif name == "get_appointments_by_patient":
        return get_appointments_by_patient(args["patient_name"])
    elif name == "get_all_doctors":
        return get_all_doctors()
    return "Unknown function."

def get_appointments_by_patient(patient_name):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, doctor_name, date, time, contact FROM appointments WHERE patient_name=? ORDER BY date, time",
            (patient_name,)
        )
        rows = cursor.fetchall()
        if not rows:
            return f"No appointments found for {patient_name}."
        appointments = [
            f"APT-{row[0]}: Dr. {row[1]} on {row[2]} at {row[3]}, Contact: {row[4]}"
            for row in rows
        ]
        return "\n".join(appointments)
        # return appointments

def get_all_doctors():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, specialization, contact FROM doctors")
        rows = cursor.fetchall()
        if not rows:
            return "No doctors found."
        doctors = [
            {
                "name": row[0],
                "specialization": row[1],
                "contact": row[2]
            }
            for row in rows
        ]
        return doctors
