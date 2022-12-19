from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session

from helper import loginRequired, loggedInNotAllowed
from idmSQLmanager import idmSQLmanager


## !! It seems it's not needed to clean data from user inputs as mariadb uses prepared statements.

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies) as per pset9. Still trying to understand how it works
# Why SESSION_PERMANENT = False if I can set a lifetime for a permanent session?

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

# Setup DB
dbconfig = {
    'user':'root',
    'password':'root',
    'host':'127.0.0.1',
    'port':3306,
    'database':'familymanager'
}
db = idmSQLmanager(**dbconfig)

# Taken from pset 9 to ensure responses aren't cached

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/login", methods=["GET", "POST"])
@loggedInNotAllowed
def login():
    if request.method == "POST":
        pass
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
@loggedInNotAllowed
def register():
    if request.method == "POST":
        if not request.form.get('username'):
            flash('You must fill the username field.')
            return redirect("/register")
        elif not request.form.get('password'):
            flash('You must fill the password field.')
            return redirect("/register")
        elif not request.form.get('confirmation'):
            flash('You must fill the password confirmation field.')
            return redirect("/register")
        else:
            if not(request.form.get('confirmation') == request.form.get('password')):
                flash('Password and Password Confirmation aren\'t equal. ')
                return redirect("/register")
            else:
                pass
                # Check on database if username is already taken.
    else:
        return render_template("register.html")

@app.route("/")
@loginRequired
def index():
    return []

@app.route("/testingRoute")
def testingRoute():
    pass