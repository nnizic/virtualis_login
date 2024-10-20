""" Frontend aplikacije za login u Flasku """

from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests

app = Flask(__name__)
app.secret_key = "25070303"

BACKEND_URL = "http://127.0.0.1:8000"


# Index page
@app.route("/")
def index():
    return render_template("index.html")


# Register page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not username or not password:
            flash("Username and password are required")
            return redirect(url_for("register"))

        try:
            response = requests.post(
                f"{BACKEND_URL}/register",
                json={"username": username, "password": password},
            )
            if response.status_code == 200:
                flash("Registration successful!")
                return redirect(url_for("login"))
            else:
                flash(response.json().get("detail", "Error registering user"))
                return redirect(url_for("register"))
        except Exception as e:
            flash(f"Error connecting to backend: {e}")
            return redirect(url_for("register"))

    return render_template("register.html")


# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            response = requests.post(
                f"{BACKEND_URL}/login",
                json={"username": username, "password": password},
            )
            if response.status_code == 200:
                data = response.json()
                session["verification_code"] = data["verification_code"]
                session["username"] = username
                session["user_uuid"] = data["user_uuid"]
                flash("Login successful")
                return redirect(url_for("welcome"))
            else:
                flash(response.json().get("detail", "Error logging in"))
                return redirect(url_for("login"))
        except Exception as e:
            flash(f"Error connecting to backend: {e}")
            return redirect(url_for("login"))

    return render_template("login.html")


# Welcome page
@app.route("/welcome")
def welcome():
    if "username" in session:
        return render_template(
            "welcome.html", username=session["username"], user_uuid=session["user_uuid"]
        )
    else:
        flash("You need to log in first!")
        return redirect(url_for("login"))


# User page
@app.route("/user/<user_uuid>", methods=["GET", "POST"])
def user_page(user_uuid):
    if "user_uuid" not in session or session["user_uuid"] != user_uuid:
        return "Access denied. Unauthorized user."

    if request.method == "POST":
        entered_code = request.form["verification_code"]
        if entered_code == session.get("verification_code"):
            return render_template(
                "user_page.html", user_uuid=user_uuid, username=session["username"]
            )
        else:
            return "Invalid verification code. Please try again."

    return render_template("verify_code.html", user_uuid=user_uuid)


# Logout
@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("user_uuid", None)
    flash("You have been logged out")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
