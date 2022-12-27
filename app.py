from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session

# Resource: https://tedboy.github.io/flask/generated/werkzeug.generate_password_hash.html
from werkzeug.security import generate_password_hash, check_password_hash

from helper import loginRequired, loggedInNotAllowed, familyRequired, familyMemberNotAllowed
from idmSQLmanager import idmSQLmanager


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


@app.route("/login", methods=["GET", "POST"])
@loggedInNotAllowed
def login():
    if request.method == "POST":
        if not request.form.get("username"):
            flash('No username given.')
            return redirect("/login", code=401)
        elif not request.form.get("password"):
            flash('No password given.')
            return redirect("/login", code=401)
        else:
            userData = db.execute("SELECT * FROM users WHERE username = ?", request.form.get('username'))
            if len(userData) == 0:
                flash("Invalid username.")
                return redirect("/login")
            elif not check_password_hash(userData[0]['password'], request.form.get('password')):
                flash("Invalid password.")
                return redirect("/login")
            else:
                session['user_id'] = userData[0]['id']
                session['family_id'] = userData[0]['family_id']
                session['username'] = userData[0]['username']
                return redirect("/")
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
                userData = db.execute('SELECT * FROM users WHERE username = ?', request.form.get('username'))

                if len(userData) > 0:
                    flash('Username already taken!')
                    return redirect("/register")
                
                passwordHash = generate_password_hash(request.form.get("password"))

                db.execute("INSERT INTO users(username, password) VALUES(?,?)", request.form.get("username"), passwordHash)
                return redirect('/login?success=True')
    else:
        return render_template("register.html")

@app.route("/logout")
@loginRequired
def logout():
    session.clear()
    return redirect("/")


@app.route("/")
@loginRequired
@familyRequired
def index():
    return render_template("index.html")


@app.route('/join_family', methods=["GET", "POST"])
@loginRequired
@familyMemberNotAllowed
def join_family():
    if request.method == "POST":
        if not request.form.get("familycode"):
            flash("You must fill the family code field.")
            return redirect("/join_family")
        elif not request.form.get("familysecret"):
            flash("You must fill the family secret field.")
            return redirect("/join_family")
        elif request.form.get("familycode") == 1:
            flash("Invalid family code.")
            return redirect("/join_family")
        else:
            queryResult = db.execute("SELECT * FROM families WHERE id = ?", request.form.get("familycode"))
            print(queryResult)
            if len(queryResult) == 0:
                flash(f"There's no family with code { str(request.form.get('familycode')) }.")
                return redirect("/join_family")
            elif queryResult[0]['secret'] != request.form.get('familysecret'):
                flash(f"Incorrect secret code. Are you sure you are trying to join '{queryResult[0]['name']}'?")
                return redirect("/join_family")
            else:
                # Issue #2
                queryData = db.execute("UPDATE users SET family_id = ? WHERE id = ?", request.form.get('familycode'), session['user_id'])
                if (queryData != False) or (queryData == None):
                    print(queryData)
                    session['family_id'] = request.form.get('familycode')
                    flash("Joined successfuly.")
                    return redirect("/")
                else:
                    flash("Something went wrong.")
                    return redirect("/join_family?success=False")
                
    else:       
        return render_template('join_family.html')


@app.route("/create_family", methods=["GET", "POST"])
@loginRequired
@familyMemberNotAllowed
def create_family():
    if request.method == "POST":
        if not request.form.get("family_name"):
            flash("You must fill the family name field.")
            return redirect("/create_family")
        elif not request.form.get("family_secret"):
            flash("You must fill the family secret code field.")
            return redirect("/create_family")
        elif not request.form.get("confirmation"):
            flash("You must fill the secret code confirmation field.")
            return redirect("/create_family")
        elif not (request.form.get("confirmation") == request.form.get("family_secret")):
            flash("Secret Code and Secret Code Confirmation aren't equal.")
            return redirect("/create_family")
        else:
            queryData = db.execute("INSERT INTO families(name, secret) VALUES(?, ?)", request.form.get("family_name"), request.form.get("family_secret"))
            if queryData != False:
                session['family_id'] = queryData
                db.execute("UPDATE users SET family_id = ? WHERE id = ?", session['family_id'], session['user_id'])
                flash("Family successfuly created.")
                return redirect("/")
            else:
                return redirect("create_family?success=False")

    else:
        return render_template("create_family.html")

@app.route("/profile")
@loginRequired
@familyRequired
def profile():
    profileData = db.execute('SELECT * FROM profiles WHERE user_id = ?', session['user_id'])

    if not(request.args.get('create')):
        familyData = db.execute('SELECT * from families WHERE id = ?', session['family_id'])[0]
        print(familyData)
        print(session['family_id'])
        familyDict = {
            'name': familyData['name'],
            'assigned': 0,
            'overdue': 0
        }

        if len(profileData) == 0:
            return render_template("profile.html", familyInfo=familyDict)
        else:
            profileData = profileData[0]
            profileDict = {
                'name': profileData['name'],
                'birthday': profileData['birthday'],
                'email': profileData['email']
            }
            return render_template("profile.html", familyInfo=familyDict, personalData=profileDict)
    else:
        if len(profileData) > 0:
            return redirect("/profile")
        else:
            return render_template("create_profile.html")

@app.route("/testingRoute")
def testingRoute():
    pass