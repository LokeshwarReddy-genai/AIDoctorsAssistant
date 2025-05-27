from flask import Flask, request, jsonify
from openai import OpenAI
import json
import os
from services.function_handler import (
    dispatch_function,
    register_doctor,
    add_doctor_availability
)
from services.schema import function_schemas
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    print("@@@@@@@@@@Data:", data)
    user_input = data.get("message", "")
    messages = [{"role": "system", "content": "You are a helpful assistant for booking doctor appointments."}]
    messages.append({"role": "user", "content": user_input})
    print("@@@@@@@@@@Messages:", messages)
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=data['messages'] if 'messages' in data else messages,
        max_tokens=150,
        functions=function_schemas,
        function_call="auto"
    )

    message = response.choices[0].message

    if message.function_call:
        fn_name = message.function_call.name
        fn_args = message.function_call.arguments
        result = dispatch_function(fn_name, fn_args)
        return jsonify({"response": result})
    else:
        return jsonify({"response": message.content})

@app.route("/api/doctor/register", methods=["POST"])
def doctor_register():
    data = request.json
    name = data.get("name")
    specialization = data.get("specialization")
    contact = data.get("contact")
    result = register_doctor(name, specialization, contact)
    return jsonify({"response": result})

# @app.route("/api/doctor/availability", methods=["POST"])
# def doctor_availability():
#     data = request.json
#     doctor_name = data.get("doctor_name")
#     date = data.get("date")
#     time = data.get("time")
#     result = add_doctor_availability(doctor_name, date, time)
#     return jsonify({"response": result})

if __name__ == "__main__":
    app.run(debug=True)
