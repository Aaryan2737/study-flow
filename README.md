# ⚡ StudyFlow — AI-Powered Smart Student Productivity Planner

> *"Imagine it's 11pm. Exam in 2 days. You open your notes and have 47 things to study. Where do you even start? We built the answer."*

---

## 🚀 About

**StudyFlow** is an AI-powered study planner built for engineering students who struggle with managing academic workload, tracking goals, and optimizing study schedules.

Built at a college hackathon by first-year engineering students. 💪

---

## ✨ Features

- 🤖 **AI Daily Insights** — Personalized study recommendations powered by Google Gemini
- ✅ **Smart Task Manager** — AI priority scoring based on urgency and difficulty
- 📅 **Auto Study Schedule** — Intelligent daily schedule generation
- ⏱️ **Pomodoro Timer** — Focus sessions with streak tracking
- 📊 **Progress Analytics** — Visual weekly study hours and completion tracking
- 🔥 **Streak System** — Daily consistency tracking with level progression
- 🔐 **User Authentication** — Personal accounts with individual data

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Flask |
| AI | Google Gemini API |
| Storage | JSON files |

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/Aaryan2737/studyflow.git
cd studyflow
```

### 2. Install dependencies
```bash
pip install flask flask-cors google-genai
```

### 3. Set up your Gemini API key
Get your free API key from [aistudio.google.com](https://aistudio.google.com)

In `app.py`, replace:
```python
API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
```

### 4. Initialize users file
Create a `users.json` file in the root directory:
```json
[]
```

### 5. Run the app
```bash
python app.py
```

### 6. Open in browser
```
http://localhost:5000
```

---

## 📁 Project Structure

```
studyflow/
├── app.py                  # Flask backend
├── users.json              # User accounts
├── userdata/               # Per-user data (auto-created)
├── templates/
│   ├── login.html          # Login & Signup page
│   └── index.html          # Main dashboard
└── README.md
```

---

## 🎯 How It Works

1. **Sign up** with your name and college email
2. **Add tasks** with priority levels — AI assigns smart scores
3. **Get your schedule** — AI organizes your day optimally
4. **Focus** using the Pomodoro timer
5. **Track progress** — streaks, analytics, level system
6. **AI Insight** updates daily based on your pending tasks

---

## 👨‍💻 Built By

**Aaryan Patil** — FY Engineering Student

---

## 📄 License

MIT License — free to use and modify.
