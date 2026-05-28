"""
Date Proposal App for Angelina 💕
A simple Flask app to propose a date and store responses in SQLite.
"""

import sqlite3
from datetime import datetime

from flask import Flask, render_template, request, abort

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
DATABASE = "responses.db"
ADMIN_KEY = "mysecret123"  # change this to something private before sharing

# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------

def get_db() -> sqlite3.Connection:
    """Open a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create the responses table if it doesn't already exist."""
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                answer TEXT NOT NULL,
                day TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        conn.commit()


# Auto-initialize the DB on first import / startup
init_db()


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Render the proposal page."""
    return render_template("proposal.html")


@app.route("/celebrate", methods=["POST"])
def celebrate():
    """
    Accept the chosen day, render the celebration page,
    and store the response in SQLite.
    """
    day = request.form.get("day", "შაბათი")

    # Persist Angelina's response
    with get_db() as conn:
        conn.execute(
            "INSERT INTO responses (answer, day) VALUES (?, ?);",
            ("yes", day),
        )
        conn.commit()

    if day == "პარასკევი":
        message = "ძაან კაი )) თეთრი რაშით გამოგივლი მაშინ პარასკევსს ❤️"
    else:
        message = "ძაან კაი )) თეთრი რაშით გამოგივლი მაშინ შაბათს❤️"

    return render_template("celebrate.html", day=day, message=message)


@app.route("/admin")
def admin():
    """
    Simple admin panel to view all responses.
    Protected by a secret query parameter.
    """
    if request.args.get("key") != ADMIN_KEY:
        abort(404)  # hide the route's existence with a generic 404

    with get_db() as conn:
        rows = conn.execute(
            "SELECT id, answer, day, created_at FROM responses ORDER BY created_at DESC;"
        ).fetchall()

    return render_template("admin.html", rows=rows)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Run locally on http://127.0.0.1:5000
    app.run(debug=True)
