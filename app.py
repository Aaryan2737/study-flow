from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from google import genai
import os

API_KEY = os.environ.get("AIzaSyBEhko1Wu3JUBh4kJJGnJGFwuG1q7eduSk", "AIzaSyBEhko1Wu3JUBh4kJJGnJGFwuG1q7eduSk")
client = genai.Client(api_key=API_KEY)
from flask_cors import CORS
import json
import os
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = "studyflow_secret_key_2024"
CORS(app)

# ─── HELPERS ───────────────────────────────────────────────────────────────

USERS_FILE = "users.json"
USERDATA_DIR = "userdata"

def load_users():
    if not os.path.exists(USERS_FILE):
        save_users([])
    with open(USERS_FILE, "r") as f:
        return json.load(f)
def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def get_user_file(email):
    safe = email.replace("@", "_at_").replace(".", "_")
    return os.path.join(USERDATA_DIR, f"{safe}.json")

def load_user_data(email):
    path = get_user_file(email)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    # New user — return fresh data
    return {
        "tasks": [],
        "streak": 0,
        "last_active": "",
        "study_hours": [0, 0, 0, 0, 0, 0, 0],
        "pomodoro_sessions": 0,
        "goals_completed": 0,
        "streak_calendar": [0] * 28
    }

def save_user_data(email, data):
    os.makedirs(USERDATA_DIR, exist_ok=True)
    with open(get_user_file(email), "w") as f:
        json.dump(data, f, indent=2)

def update_streak(data):
    today = str(date.today())
    last = data.get("last_active", "")
    if last != today:
        if last == str(date.fromordinal(date.today().toordinal() - 1)):
            data["streak"] = data.get("streak", 0) + 1
        elif last != today:
            data["streak"] = 1
        data["last_active"] = today
        # Update calendar
        cal = data.get("streak_calendar", [0] * 28)
        cal = cal[1:] + [1]
        data["streak_calendar"] = cal
    return data

# ─── ROUTES ────────────────────────────────────────────────────────────────

@app.route("/")
def home():
    if "email" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login_page"))

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "email" not in session:
        return redirect(url_for("login_page"))
    return render_template("index.html")

# ─── AUTH ──────────────────────────────────────────────────────────────────

@app.route("/api/signup", methods=["POST"])
def signup():
    body = request.json
    name      = body.get("name", "").strip()
    email     = body.get("email", "").strip().lower()
    password  = body.get("password", "").strip()
    year      = body.get("year", "").strip()

    if not all([name, email, password]):
        return jsonify({"success": False, "message": "All fields required"}), 400

    users = load_users()
    if any(u["email"] == email for u in users):
        return jsonify({"success": False, "message": "Email already registered"}), 409

    users.append({"name": name, "email": email, "password": password, "year": year})
    save_users(users)

    # Create fresh user data file
    data = load_user_data(email)
    save_user_data(email, data)

    session["email"] = email
    session["name"]  = name
    return jsonify({"success": True, "message": "Account created!", "name": name})

@app.route("/api/login", methods=["POST"])
def login():
    body     = request.json
    email    = body.get("email", "").strip().lower()
    password = body.get("password", "").strip()

    users = load_users()
    user  = next((u for u in users if u["email"] == email and u["password"] == password), None)

    if not user:
        return jsonify({"success": False, "message": "Invalid email or password"}), 401

    session["email"] = email
    session["name"]  = user["name"]
    return jsonify({"success": True, "name": user["name"]})

@app.route("/api/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))

# ─── USER DATA ─────────────────────────────────────────────────────────────

@app.route("/api/userdata", methods=["GET"])
def get_userdata():
    if "email" not in session:
        return jsonify({"success": False}), 401
    data = load_user_data(session["email"])
    data = update_streak(data)
    save_user_data(session["email"], data)
    data["name"]  = session["name"]
    data["email"] = session["email"]
    return jsonify({"success": True, "data": data})

# ─── TASKS ─────────────────────────────────────────────────────────────────

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    if "email" not in session:
        return jsonify({"success": False}), 401
    data = load_user_data(session["email"])
    return jsonify({"success": True, "tasks": data.get("tasks", [])})

@app.route("/api/tasks", methods=["POST"])
def add_task():
    if "email" not in session:
        return jsonify({"success": False}), 401
    body = request.json
    data = load_user_data(session["email"])

    priority = body.get("priority", "medium")
    score_map = {"high": round(7 + __import__('random').random() * 2, 1),
                 "medium": round(4 + __import__('random').random() * 3, 1),
                 "low": round(1 + __import__('random').random() * 3, 1)}

    task = {
        "id": int(datetime.now().timestamp() * 1000),
        "name": body.get("name", ""),
        "priority": priority,
        "score": score_map[priority],
        "due": body.get("due", "Today"),
        "done": False,
        "created": str(date.today())
    }
    data["tasks"].append(task)
    save_user_data(session["email"], data)
    return jsonify({"success": True, "task": task})

@app.route("/api/tasks/<int:task_id>", methods=["PATCH"])
def toggle_task(task_id):
    if "email" not in session:
        return jsonify({"success": False}), 401
    data = load_user_data(session["email"])
    for t in data["tasks"]:
        if t["id"] == task_id:
            t["done"] = not t["done"]
            break
    goals = sum(1 for t in data["tasks"] if t["done"])
    data["goals_completed"] = goals
    save_user_data(session["email"], data)
    return jsonify({"success": True})

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    if "email" not in session:
        return jsonify({"success": False}), 401
    data = load_user_data(session["email"])
    data["tasks"] = [t for t in data["tasks"] if t["id"] != task_id]
    save_user_data(session["email"], data)
    return jsonify({"success": True})

# ─── POMODORO ──────────────────────────────────────────────────────────────

@app.route("/api/pomodoro/complete", methods=["POST"])
def pomodoro_complete():
    if "email" not in session:
        return jsonify({"success": False}), 401
    data = load_user_data(session["email"])
    data["pomodoro_sessions"] = data.get("pomodoro_sessions", 0) + 1

    # Add 0.4 study hours per pomodoro session
    hours = data.get("study_hours", [0]*7)
    hours[-1] = round(hours[-1] + 0.4, 1)
    data["study_hours"] = hours

    save_user_data(session["email"], data)
    return jsonify({"success": True, "sessions": data["pomodoro_sessions"]})

# ─── AI INSIGHT ────────────────────────────────────────────────────────────

@app.route("/api/insight", methods=["GET"])
def get_insight():
    if "email" not in session:
        return jsonify({"success": False}), 401

    data  = load_user_data(session["email"])
    tasks = data.get("tasks", [])
    name  = session["name"].split()[0]
    streak = data.get("streak", 0)

    pending = [t for t in tasks if not t["done"]]
    pending.sort(key=lambda x: x["score"], reverse=True)

    if not pending:
        insight = f"Amazing work {name}! All tasks completed. Keep the momentum going 🚀"
        return jsonify({"success": True, "insight": insight})

    task_list = "\n".join([f"- {t['name']} (priority: {t['priority']}, score: {t['score']})" for t in pending])

    prompt = f"""You are a smart study coach for an engineering student named {name}.
Their current streak is {streak} days.
Their pending tasks are:
{task_list}

Give a short, motivating, personalized insight (2-3 sentences max).
Mention the most urgent task by name.
Be friendly, use one emoji. No markdown formatting."""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        insight = response.text.strip()
    except Exception as e:
        insight = f"Hey {name}, focus on your highest priority task today. Keep your {streak}-day streak going! 🔥"

    return jsonify({"success": True, "insight": insight})
# ───────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs(USERDATA_DIR, exist_ok=True)
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)