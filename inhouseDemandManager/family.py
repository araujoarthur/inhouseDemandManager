from inhouseDemandManager import app, flash, redirect, render_template, request, session, url_for,  generate_password_hash, check_password_hash
from . import loggedInNotAllowed, db, loginRequired, loggedInNotAllowed, familyRequired, familyMemberNotAllowed, validateEmail, validateDate, APP_DATE_FORMAT


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

@app.route("/family", methods=["GET"])
@loginRequired
@familyRequired
def family():
    return render_template('familyoverview.html')

@app.route("/family_members", methods=["GET"])
@loginRequired
@familyRequired
def family_members():
    res = db.execute("SELECT username FROM users WHERE family_id = ?", session['family_id'])
    if res == False:
        flash('Something wen\'t wrong')
        return redirect('/')
    elif res == []:
        return render_template("familymembers.html")
    else:
        return render_template("familymembers.html", familyMembers=res)

@app.route('/leave_family', methods=['GET'])
@loginRequired
@familyRequired
def leave_family():
    if not request.args.get('confirmation'):
        family_name = db.execute("SELECT name FROM families WHERE ID = ?", session['family_id'])[0]['name']
        return render_template('leavefamilyprompt.html', family_name = family_name)
    else:
       res = db.execute('UPDATE users SET family_id = ? WHERE id = ?', 1, session['user_id'])
       print(res)
       session['family_id'] = 1
       return redirect('/')