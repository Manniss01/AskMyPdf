import json
import os

def save_session(session_id, question, answer):
    file_path = os.path.join("D:\PYTHON_Projects\PythonProject\data", "user_sessions.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            sessions = json.load(f)
    else:
        sessions = {}

    if session_id not in sessions:
        sessions[session_id] = []

    sessions[session_id].append({"question": question, "answer": answer})

    with open(file_path, "w") as f:
        json.dump(sessions, f, indent=2)
