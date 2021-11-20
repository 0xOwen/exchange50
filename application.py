from flask import Flask, render_template, request, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from cs50 import SQL
import os

from helpers import login_required

app = Flask(__name__)
db = SQL('sqlite:///database.db')
app.secret_key = os.environ['SECRET_KEY']

@app.route("/")
def homepage():
    return render_template("home.html")

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

    passHash = generate_password_hash(password)
    db.execute("INSERT INTO users(username, email, password) VALUES (? , ?, ?)", username, email, passHash)
    return render_template("register.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        if not request.form.get("username") or not request.form.get("password"):
            # implement sth in case of errors
            pass

        
        rows = db.execute("SELECT id, username, password FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return "error"
            
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]
        return redirect("/")

@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")
        
@app.route("/trade")
@login_required
def trade():
    return render_template("currency.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("user_dashboard.html", name = session["username"])

if __name__ == "__main__":
    app.debug = True
    app.run()