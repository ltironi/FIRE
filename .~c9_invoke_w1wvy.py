import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import pandas as pd

from helpers import apology, login_required, usd
from canal import canal

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///fi.db")


@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    user = session["user_id"]
    if request.method == "POST":
        EOYbalance = request.form.get("eoybalance")
        year = request.form.get("year")
        db.execute("INSERT INTO balance (user_id, EOYbalance, year) VALUES (:user_id, :EOYbalance, :year)", user_id=user, EOYbalance=EOYbalance, year=year)
        return redirect("/add")
    else:
        data = db.execute(f"SELECT year, EOYbalance FROM balance WHERE user_id = {user} ORDER BY year")
        for row in data:
            row['EOYbalance']=usd(row['EOYbalance'])
        return render_template("add.html",data=data)



@app.route("/chart", methods=["GET"])
@login_required
def chart():
    user = session["user_id"]
    data = db.execute(f"SELECT year, EOYbalance FROM balance WHERE user_id = {user} ORDER BY year")
    print(data)
    ax = []
    ay = []
    for row in data:
        #ax.append(str(row['year']))
        ay.append(int(row['EOYbalance']))


    ay1=canal()[0]
    ay2=canal()[1]

    for i in range(0,len(ay1)):
        ax.append('Year '+str(i))

    return render_template("chart.html",ax=ax,ay=ay,ay1=ay1,ay2=ay2)




@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure email was submitted
        if not request.form.get("email"):
            return apology("must provide email", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for email
        rows = db.execute("SELECT * FROM users WHERE email = :email",
                          email=request.form.get("email"))

        # Ensure email exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid email and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:

        fname = request.form.get("fname")
        if not fname:
            return apology(message="You must provide a first name.",code=400)
        lname = request.form.get("lname")
        if not lname:
            return apology(message="You must provide a last name.",code=400)
        email = request.form.get("email")
        if not email:
            return apology(message="You must provide an email.",code=400)
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not password:
            return apology(message="You must provide a password.",code=400)
        if password != confirmation:
            return apology(message="Your password and confirmation doesn't match.",code=400)
        db.execute("INSERT INTO users (fname, lname, email, hash) VALUES (:fname, :lname, :email, :hash)", fname=fname, lname=lname, email=email, hash=generate_password_hash(password))
        return redirect("/login")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)