from inhouseDemandManager import app, flash, redirect, render_template, request, session, url_for,  generate_password_hash, check_password_hash
from . import loggedInNotAllowed, db, loginRequired, loggedInNotAllowed, familyRequired, familyMemberNotAllowed, validateEmail, validateDate, APP_DATE_FORMAT


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