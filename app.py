from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Function to create the database if it doesn't exist
def init_db():
    with sqlite3.connect("exercise.db") as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT NOT NULL,
            muscle_group TEXT NOT NULL,
            name TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )""")
        conn.commit()

# Ensure the database exists before starting the app
init_db()

# Sample exercises (Run this only once to add default exercises)
def add_default_exercises():
    with sqlite3.connect("exercise.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM exercises")
        count = cursor.fetchone()[0]
        if count == 0:  # If no exercises exist, add them
            exercises = [
                ("Monday", "Chest", "00:06 Chest Press w/ Step (M) R30", 0),
                ("Monday", "Arms", "28:39 Tension Curls (UF) R30", 0),
                ("Monday", "Legs", "44:56 Lat Lunge Archer Row (M)", 0),
                ("Monday", "Hang", "Hang", 0),

                ("Monday", "Chest", "00:35 Chest Fly w/ Step (M) R30", 0),
                ("Monday", "Shoulders", "12:39 Upright Row (Bar) B50", 0),
                ("Monday", "Back", "07:29 Standing Tens’n Rw (M) R30", 0),
                ("Monday", "Hang", "Hang", 0),

                ("Monday", "Arms", "31:02 Hammer Ten Curl (UF) R30", 0),
                ("Monday", "Shoulders", "18:14 Shoulder Shrug (Bar) B50", 0),
                ("Monday", "Plank", "Plank", 0),
                ("Monday", "Hang", "Hang", 0),

                ("Tuesday", "Chest", "01:09 Tension Press (M) R30", 0),
                ("Tuesday", "Arms", "32:04 Rev Tension Curl (UF) R30", 0),
                ("Tuesday", "Legs", "46:03 Squat Lifting Twist (L)", 0),
                ("Tuesday", "Hang", "Hang", 0)
            ]
            conn.executemany("INSERT INTO exercises (day, muscle_group, name, completed) VALUES (?, ?, ?, ?)", exercises)
            conn.commit()

# Add default exercises if the table is empty
add_default_exercises()

# Route to display the exercise tracker
@app.route("/")
def index():
    with sqlite3.connect("exercise.db") as conn:
        cursor = conn.execute("SELECT * FROM exercises ORDER BY day, id")
        exercises = cursor.fetchall()

    # Organize exercises by day
    exercises_by_day = {}
    for exercise in exercises:
        day = exercise[1]
        if day not in exercises_by_day:
            exercises_by_day[day] = []
        exercises_by_day[day].append(exercise)

    return render_template("index.html", exercises_by_day=exercises_by_day)

# Route to update checkbox state
@app.route("/update", methods=["POST"])
def update():
    exercise_id = request.form["exercise_id"]
    completed = 1 if "completed" in request.form else 0

    with sqlite3.connect("exercise.db") as conn:
        conn.execute("UPDATE exercises SET completed = ? WHERE id = ?", (completed, exercise_id))
        conn.commit()

    return redirect("/")

# Route to reset all checkboxes
@app.route("/reset", methods=["POST"])
def reset():
    with sqlite3.connect("exercise.db") as conn:
        conn.execute("UPDATE exercises SET completed = 0")
        conn.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
