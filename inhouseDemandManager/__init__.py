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

import inhouseDemandManager.tasks
import inhouseDemandManager.authentication
import inhouseDemandManager.family
import inhouseDemandManager.profile

@app.route("/testingRoute")
def testingRoute():
    pass