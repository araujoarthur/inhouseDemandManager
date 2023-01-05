from inhouseDemandManager import app, flash, redirect, render_template, request, session, url_for,  generate_password_hash, check_password_hash
from . import loggedInNotAllowed, db, loginRequired, loggedInNotAllowed, familyRequired, familyMemberNotAllowed, validateEmail, validateDate, APP_DATE_FORMAT

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