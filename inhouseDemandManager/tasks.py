from inhouseDemandManager import app, flash, redirect, render_template, request, session, url_for,  generate_password_hash, check_password_hash
from . import loggedInNotAllowed, db, loginRequired, loggedInNotAllowed, familyRequired, familyMemberNotAllowed, validateEmail, validateDate, APP_DATE_FORMAT

@app.route("/")
@loginRequired
@familyRequired
def index():
    return render_template("index.html", assigned_tasks=[1], created_tasks=[1], family_tasks=[1])