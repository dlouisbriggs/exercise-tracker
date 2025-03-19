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
                ("Chest Press w/ Step (M) R30", 0),
                ("Tension Curls (UF) R30", 0),
                ("Chest Fly w/ Step (M) R30", 0),
                ("Upright Row (Bar) B50", 0),
                ("Hammer Ten Curl (UF) R30", 0),
                ("Shoulder Shrug (Bar) B50", 0),
                ("Tension Press (M) R30", 0),
                ("Rev Tension Curl (UF) R30", 0),
                ("Ntrl Grip Tension Pr (M) R30", 0),
                ("Shoulder Press (Bar) B50", 0),
                ("Low Tension Kickback (L) R30", 0),
                ("Tension Front Raises (L) Y10", 0)
            ]
            conn.executemany("INSERT INTO exercises (name, completed) VALUES (?, ?)", exercises)
            conn.commit()

# Add default exercises if the table is empty
add_default_exercises()

# Route to display the exercise tracker
@app.route("/")
def index():
    with sqlite3.connect("exercise.db") as conn:
        cursor = conn.execute("SELECT * FROM exercises")
        exercises = cursor.fetchall()
    return render_template("index.html", exercises=exercises)

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
