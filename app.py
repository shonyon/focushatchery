from flask import Flask, render_template, request, jsonify
import sqlite3
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
DB_PATH = Path(__file__).with_name("focus_data.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS focus_record (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        chick_count INTEGER NOT NULL DEFAULT 0,
        total_minutes INTEGER NOT NULL DEFAULT 0,
        current_minutes INTEGER NOT NULL DEFAULT 0,
        updated_at TEXT NOT NULL
    )
    """)
    conn.execute("""
    INSERT OR IGNORE INTO focus_record
    (id, chick_count, total_minutes, current_minutes, updated_at)
    VALUES (1, 0, 0, 0, ?)
    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),))
    conn.commit()
    conn.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.get("/api/record")
def get_record():
    conn = get_db()
    row = conn.execute("SELECT * FROM focus_record WHERE id = 1").fetchone()
    conn.close()
    return jsonify({
        "chickCount": row["chick_count"],
        "totalMinutes": row["total_minutes"],
        "currentMinutes": row["current_minutes"],
        "updatedAt": row["updated_at"]
    })


@app.post("/api/add_minutes")
def add_minutes():
    data = request.get_json(force=True)
    minutes = int(data.get("minutes", 0))

    if minutes <= 0:
        return jsonify({"ok": False, "error": "minutes must be positive"}), 400

    conn = get_db()
    row = conn.execute("SELECT * FROM focus_record WHERE id = 1").fetchone()

    chick_count = row["chick_count"]
    total_minutes = row["total_minutes"] + minutes
    current_minutes = row["current_minutes"] + minutes

    hatched = False
    if current_minutes >= 60:
        chick_count += 1
        current_minutes = current_minutes - 60
        hatched = True

    conn.execute("""
    UPDATE focus_record
    SET chick_count = ?, total_minutes = ?, current_minutes = ?, updated_at = ?
    WHERE id = 1
    """, (
        chick_count,
        total_minutes,
        current_minutes,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()

    return jsonify({
        "ok": True,
        "hatched": hatched,
        "chickCount": chick_count,
        "totalMinutes": total_minutes,
        "currentMinutes": current_minutes
    })


@app.post("/api/break_egg")
def break_egg():
    conn = get_db()
    conn.execute("""
    UPDATE focus_record
    SET current_minutes = 0, updated_at = ?
    WHERE id = 1
    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


@app.post("/api/new_egg")
def new_egg():
    conn = get_db()
    conn.execute("""
    UPDATE focus_record
    SET current_minutes = 0, updated_at = ?
    WHERE id = 1
    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


@app.post("/api/clear")
def clear_record():
    conn = get_db()
    conn.execute("""
    UPDATE focus_record
    SET chick_count = 0, total_minutes = 0, current_minutes = 0, updated_at = ?
    WHERE id = 1
    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=True)
