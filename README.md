# Doctor Chatbot API (Flask + SQLite)

## Setup
```
pip install -r requirements.txt
python -c "from services.db import init_db; init_db()"
python app.py
```

Then POST to `http://localhost:5000/api/chat` with:
```json
{
  "message": "Book an appointment with Dr. Smith at 10 AM on May 18 for John"
}
```
