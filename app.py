import sqlite3
import os

app = Flask(__name__)

# Function to create database if it doesn't exist
def init_db():
    with sqlite3.connect("exercise.db") as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )""")
        conn.commit()

# Ensure the database and table exist before starting the app
init_db()


from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect("exercise_tracker.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS exercises (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        day TEXT,
                        session INTEGER,
                        exercise TEXT,
                        completed INTEGER DEFAULT 0
                    )''')
    conn.commit()
    conn.close()

init_db()

# Exercise Schedule
EXERCISE_PLAN = {
    "Monday": [(1, "Chest Press w/ Step (M) R30"), (1, "Tension Curls (UF) R30"),
                (2, "Chest Fly w/ Step (M) R30"), (2, "Upright Row (Bar) B50"),
                (3, "Hammer Ten Curl (UF) R30"), (3, "Shoulder Shrug (Bar) B50")],
    "Tuesday": [(1, "Tension Press (M) R30"), (1, "Rev Tension Curl (UF) R30"),
                 (2, "Ntrl Grip Tension Pr (M) R30"), (2, "Shoulder Press (Bar) B50"),
                 (3, "Low Tension Kickback (L) R30"), (3, "Tension Front Raises (L) Y10")]
}

# Populate database
def populate_db():
    conn = sqlite3.connect("exercise_tracker.db")
    cursor = conn.cursor()
    for day, exercises in EXERCISE_PLAN.items():
        for session, exercise in exercises:
            cursor.execute("INSERT OR IGNORE INTO exercises (day, session, exercise) VALUES (?, ?, ?)", (day, session, exercise))
    conn.commit()
    conn.close()

populate_db()

@app.route("/")
def index():
    conn = sqlite3.connect("exercise_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM exercises")
    exercises = cursor.fetchall()
    conn.close()
    return render_template("index.html", exercises=exercises)

@app.route("/update", methods=["POST"])
def update():
    @app.route("/reset", methods=["POST"])
def reset():
    with sqlite3.connect("exercise.db") as conn:
        conn.execute("UPDATE exercises SET completed = 0")
        conn.commit()
    return redirect("/")

    exercise_id = request.form["exercise_id"]
    completed = 1 if request.form.get("completed") == "on" else 0
    conn = sqlite3.connect("exercise_tracker.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE exercises SET completed = ? WHERE id = ?", (completed, exercise_id))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
