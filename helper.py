import os

import traceback

from flask import redirect, render_template, request, session
from functools import wraps

from email_validator import validate_email, EmailNotValidError

import datetime

APP_DATE_FORMAT  = '%d/%m/%Y'

def loginRequired(route):
    """ Verify if user is logged-in for pages where it is required. """
    @wraps(route)
    def decorated_route(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect('/login')
        return route(*args, **kwargs)
    return decorated_route

def loggedInNotAllowed(route):
    """ Verify if a logged user is trying to access a page for not logged in users. """
    @wraps(route)
    def decorated_route(*args, **kwargs):
        if not(session.get('user_id') is None):
            return redirect('/')
        return route(*args, **kwargs)
    return decorated_route

def familyRequired(route):
    """ Check if user is already in a family. If not, redirects them to the family assignment page. """
    @wraps(route)
    def decorated_route(*args, **kwargs):
        if (session.get('family_id') == 1):
            return redirect('/join_family')
        return route(*args, **kwargs)
    return decorated_route

def familyMemberNotAllowed(route):
    """ Check if user is already in a family. If it is, doesn't let them into certain pages. """
    @wraps(route)
    def decorated_route(*args, **kwargs):
        if not (session.get('family_id') == 1):
            return redirect('/')
        return route(*args, **kwargs)
    return decorated_route

def validateEmail(mail):
    try:
        res = validate_email(mail).email
        return res
    except EmailNotValidError as e:
        return False

def validateDate(datestr):
    try:
        dateObj = datetime.datetime.strptime(datestr, APP_DATE_FORMAT).date()
        return dateObj
    except:
        return False