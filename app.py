from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

from cric_api import get_scorecard


app = Flask(__name__)

# Secret key for Flask sessions
app.secret_key = "cricket-secret-key"


# --------------------------------------------------
# DATABASE PATH
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "cricket.db")


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.route("/")
def home():
    return "CricketHub is running!"


# --------------------------------------------------
# LOGIN
# --------------------------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    # When login form is submitted
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Check that fields are not empty
        if not username or not password:
            return "Username and password are required."

        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT * FROM users
            WHERE username = ? AND password = ?
            """,
            (username, password)
        )

        user = cursor.fetchone()

        connection.close()

        # User found
        if user:
            session["logged_in"] = True
            session["username"] = username

            return redirect(url_for("dashboard"))

        # User not found
        return "Invalid username or password."

    # Normal GET request
    return render_template("login.html")


# --------------------------------------------------
# REGISTER
# --------------------------------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Check empty fields
        if not username or not password:
            return "Username and password are required."

        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        # Check whether username already exists
        cursor.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            connection.close()
            return "Username already exists."

        # Create new user
        cursor.execute(
            """
            INSERT INTO users (username, password)
            VALUES (?, ?)
            """,
            (username, password)
        )

        connection.commit()
        connection.close()

        # After registration → login page
        return redirect(url_for("login"))

    # Normal GET request
    return render_template("register.html")


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    # User must be logged in
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    # Default match
    match_id = 169497

    # If user searches another Match ID
    if request.method == "POST":
        entered_id = request.form.get("match_id", "").strip()

        if entered_id.isdigit():
            match_id = int(entered_id)

    try:
        # Get scorecard from API
        scorecard = get_scorecard(match_id)

        # Get useful information from API response
        appendix = scorecard.get("appendix", {})

        match_title = appendix.get(
            "seotitle",
            appendix.get("seo_title", "Cricket Match")
        )

        match_status = scorecard.get(
            "status",
            "Status not available"
        )

        last_updated = scorecard.get(
            "responselastupdated",
            "Not available"
        )

    except Exception as e:

        print("API Error:", e)

        scorecard = None
        match_title = "Match information unavailable"
        match_status = "Unable to load match"
        last_updated = "Not available"

    return render_template(
        "dashboard.html",
        scorecard=scorecard,
        match_id=match_id,
        match_title=match_title,
        match_status=match_status,
        last_updated=last_updated
    )


# --------------------------------------------------
# LOGOUT
# --------------------------------------------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# --------------------------------------------------
# RUN FLASK
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)