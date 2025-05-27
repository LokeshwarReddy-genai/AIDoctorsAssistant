function_schemas = [
    {
        "name": "book_appointment",
        "description": "Book a doctor appointment, appointment date and time must be in the future ",
        "parameters": {
            "type": "object",
            "properties": {
                "patient_name": {"type": "string"},
                "doctor_name": {"type": "string"},
                "date": {"type": "string"},
                "time": {"type": "string"},
                "contact": {"type": "string"}
            },
            "required": ["patient_name", "doctor_name", "date", "time", "contact"]
        }
    },
    {
        "name": "reschedule_appointment",
        "description": "Reschedule a doctor appointment",
        "parameters": {
            "type": "object",
            "properties": {
                "appointment_id": {"type": "string"},
                "new_date": {"type": "string"},
                "new_time": {"type": "string"}
            },
            "required": ["appointment_id", "new_date", "new_time"]
        }
    },
    {
        "name": "cancel_appointment",
        "description": "Cancel a doctor appointment",
        "parameters": {
            "type": "object",
            "properties": {
                "appointment_id": {"type": "string"}
            },
            "required": ["appointment_id"]
        }
    },
    {
        "name": "check_availability",
        "description": "Check a doctor's availability date for a specific date 'YYYY-MM-DD'",
        "parameters": {
            "type": "object",
            "properties": {
                "doctor_name": {"type": "string"},
                "date": {"type": "string"}
            },
            "required": ["doctor_name", "date"]
        }
    },
    {
        "name": "get_appointments_by_patient",
        "description": "Get all booked appointments for a patient",
        "parameters": {
            "type": "object",
            "properties": {
                "patient_name": {"type": "string"}
            },
            "required": ["patient_name"]
        }
    },
    {
        "name": "get_all_doctors",
        "description": "Get a list of all doctors with their specialization and contact info",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
]
