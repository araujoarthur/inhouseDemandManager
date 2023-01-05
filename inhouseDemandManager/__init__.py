from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session

# Resource: https://tedboy.github.io/flask/generated/werkzeug.generate_password_hash.html
from werkzeug.security import generate_password_hash, check_password_hash

from .utils.helper import loginRequired, loggedInNotAllowed, familyRequired, familyMemberNotAllowed, validateEmail, validateDate, APP_DATE_FORMAT
from .SQLManagement.idmSQLmanager import idmSQLmanager


## !! It seems it's not needed to clean data from user inputs as mariadb uses prepared statements.

app = Flask(__name__)

# Setting some variables to be used in jinja templates.
app.jinja_env.globals['idm_version'] = '1.0.0'

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


import inhouseDemandManager.authentication
import inhouseDemandManager.family

@app.route("/")
@loginRequired
@familyRequired
def index():
    return render_template("index.html")

@app.route("/profile")
@loginRequired
@familyRequired
def profile():
    profileData = db.execute('SELECT * FROM profiles WHERE user_id = ?', session['user_id'])

    if not(request.args.get('create')):
        familyData = db.execute('SELECT * from families WHERE id = ?', session['family_id'])[0]
        familyDict = {
            'name': familyData['name'],
            'assigned': 0,
            'overdue': 0
        }

        if len(profileData) == 0:
            print('hoooooooo')
            return render_template("profile.html", familyInfo=familyDict)
        else:
            profileData = profileData[0]
            print(profileData)
            profileDict = {
                'name': profileData['name'],
                'birthday': profileData['birthday'].strftime(APP_DATE_FORMAT),
                'email': profileData['email']
            }
            return render_template("profile.html", familyInfo=familyDict, personalInfo=profileDict)
    else:
        if len(profileData) > 0:
            return redirect("/profile")
        else:
            return render_template("create_profile.html")

@app.route("/create_profile", methods=["POST"])
@loginRequired
@familyRequired
def create_profile():
    if request.method == "POST":
        if not request.form.get('person_name'):
            flash('Must fill your name.')
            return redirect("/profile?create=True")
        elif not request.form.get('person_bday'):
            flash('Must fill your birthday.')
            return redirect("/profile?create=True")
        elif not request.form.get('person_mail'):
            flash('Must fill your email.')
            return redirect("/profile?create=True")
        else:
            if not (email := validateEmail(request.form.get('person_mail'))):
                flash('Must provide a valid email.')
                return redirect("/profile?create=True")
            elif not (fdate := validateDate(request.form.get('person_bday'))):
                flash('Must provide a valid date.')
                return redirect('/profile?create=True')
            else:
                res = db.execute("INSERT INTO profiles(user_id, name, email, birthday) VALUES(?,?,?,?)", session['user_id'],
                           request.form.get('person_name'), email, fdate)
                if not res:
                    flash('Something wen\'t wrong')
                    return redirect("/profile?create=True")  
                else:
                    return redirect("/profile")

            


@app.route("/testingRoute")
def testingRoute():
    pass