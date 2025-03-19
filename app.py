from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    with sqlite3.connect("exercise.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT NOT NULL,
            muscle_group TEXT NOT NULL,
            name TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )""")
        conn.commit()

# Populate the database with all exercises
def add_default_exercises():
    exercises = [
        # ---- Monday ----
        ("Monday", "Chest", "00:06 Chest Press w/ Step (M) R30"),
        ("Monday", "Arms", "28:39 Tension Curls (UF) R30"),
        ("Monday", "Legs", "44:56 Lat Lunge Archer Row (M)"),
        ("Monday", "Hang", "Hang"),

        ("Monday", "Chest", "00:35 Chest Fly w/ Step (M) R30"),
        ("Monday", "Shoulders", "12:39 Upright Row (Bar) B50"),
        ("Monday", "Back", "07:29 Standing Tens’n Rw (M) R30"),
        ("Monday", "Hang", "Hang"),

        ("Monday", "Arms", "31:02 Hammer Ten Curl (UF) R30"),
        ("Monday", "Shoulders", "18:14 Shoulder Shrug (Bar) B50"),
        ("Monday", "Plank", "Plank"),
        ("Monday", "Hang", "Hang"),

        # ---- Tuesday ----
        ("Tuesday", "Chest", "01:09 Tension Press (M) R30"),
        ("Tuesday", "Arms", "32:04 Rev Tension Curl (UF) R30"),
        ("Tuesday", "Legs", "46:03 Squat Lifting Twist (L)"),
        ("Tuesday", "Hang", "Hang"),

        ("Tuesday", "Chest", "02:07 Ntrl Grip Tension Pr (M) R30"),
        ("Tuesday", "Shoulders", "15:29 Shoulder Press (Bar) B50"),
        ("Tuesday", "Back", "10:14 Back Fly (M) R30"),
        ("Tuesday", "Hang", "Hang"),

        ("Tuesday", "Arms", "28:13 Low Tension Kickback (L) R30"),
        ("Tuesday", "Shoulders", "18:53 Tension Front Raises (L) Y10"),
        ("Tuesday", "Plank", "Plank"),
        ("Tuesday", "Hang", "Hang"),

        # ---- Wednesday ----
        ("Wednesday", "Chest", "03:06 Cross Body Fly (M) R30"),
        ("Wednesday", "Arms", "25:39 Cross Body Extension (M) R30"),
        ("Wednesday", "Legs", "46:56 Deadlift (L)"),
        ("Wednesday", "Hang", "Hang"),

        ("Wednesday", "Chest", "06:42 Push Up Fly Combo (H) R30"),
        ("Wednesday", "Shoulders", "19:27 Cross Body Lift (L) R30"),
        ("Wednesday", "Back", "07:54 Bent Ten Lat Pull (M) R30"),
        ("Wednesday", "Hang", "Hang"),

        ("Wednesday", "Arms", "23:19 Mid Tension Kickback (M) R30"),
        ("Wednesday", "Shoulders", "21:09 Scarecrow Tension (M) Y10"),
        ("Wednesday", "Plank", "Plank"),
        ("Wednesday", "Hang", "Hang"),

        # ---- Thursday ----
        ("Thursday", "Chest", "03:43 Upper Chest Ten Press (L) R30"),
        ("Thursday", "Arms", "22:09 'Preacher' Ten Curl (H) R30"),
        ("Thursday", "Legs", "48:08 Cross Kick Outs (UF) Y10"),
        ("Thursday", "Hang", "Hang"),

        ("Thursday", "Chest", "04:23 Upper Chest Fly w/ Step (L) R30"),
        ("Thursday", "Shoulders", "21:34 Face Tension Pulls (H) R30"),
        ("Thursday", "Back", "08:58 Archer Row (H) R30"),
        ("Thursday", "Hang", "Hang"),

        ("Thursday", "Arms", "22:34 Chest Tap Curl Ten (M) R30"),
        ("Thursday", "Shoulders", "16:28 Shrug Circles Tension (Bar)"),
        ("Thursday", "Plank", "Plank"),
        ("Thursday", "Hang", "Hang"),

        # ---- Friday ----
        ("Friday", "Chest", "02:37 Crossbody Press (M) R30"),
        ("Friday", "Arms", "25:02 Hercules Curl (H) R30"),
        ("Friday", "Legs", "49:08 Squat (Bar) B50"),
        ("Friday", "Hang", "Hang"),

        ("Friday", "Chest", "04:57 Low Chest Ten Press (H) R30"),
        ("Friday", "Shoulders", "16:01 Front Raise Tension (UF) R30"),
        ("Friday", "Back", "13:44 ChairTension Row (H) R30"),
        ("Friday", "Hang", "Hang"),

        ("Friday", "Arms", "33:01 Overhead Ten Extension (H)"),
        ("Friday", "Shoulders", "15:29 Military Press Tension (UF) R30"),
        ("Friday", "Plank", "Plank"),
        ("Friday", "Hang", "Hang"),

        # ---- Saturday ----
        ("Saturday", "Chest", "05:32 Lower Chest Fly w/ Step (H) R30"),
        ("Saturday", "Arms", "33:30 Rev Grip Ten Pushdowns (H)"),
        ("Saturday", "Legs", "49:36 Lunge (UF) R30"),
        ("Saturday", "Hang", "Hang"),

        ("Saturday", "Chest", "06:02 Low Chest Ten Press (H) R30"),
        ("Saturday", "Shoulders", "00:00 Side Raise Cross Ten (UF) Y10"),
        ("Saturday", "Back", "14:19 StrT Arm Ten Lat Pull (H) R30"),
        ("Saturday", "Hang", "Hang"),

        ("Saturday", "Arms", "33:50 Sgl Arm X Pulldown (H) R30"),
        ("Saturday", "Shoulders", "17:08 Upright Row Tension (UF) R30"),
        ("Saturday", "Plank", "Plank"),
        ("Saturday", "Hang", "Hang"),
    ]

    with sqlite3.connect("exercise.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM exercises")
        count = cursor.fetchone()[0]

        if count == 0:
            cursor.executemany("INSERT INTO exercises (day, muscle_group, name, completed) VALUES (?, ?, ?, ?)", exercises)
            conn.commit()

# Reset exercises
@app.route("/reset", methods=["POST"])
def reset_exercises():
    with sqlite3.connect("exercise.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE exercises SET completed = 0")
        conn.commit()
    return redirect(url_for("index"))

# Display exercises
@app.route("/")
def index():
    with sqlite3.connect("exercise.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, day, muscle_group, name, completed FROM exercises ORDER BY day, id")
        exercises = cursor.fetchall()

    return render_template("index.html", exercises=exercises)

# Start application
if __name__ == "__main__":
    init_db()
    add_default_exercises()
    app.run(debug=True, host="0.0.0.0")
