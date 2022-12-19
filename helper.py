import os

import traceback

from flask import redirect, render_template, request, session
from functools import wraps


def loginRequired(route):
    """ Verify if user is logged-in for pages where it is required. """
    @wraps(route)
    def decorated_route(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect('/login')
        return route(*args, **kwargs)
    return decorated_route

def loggedInNotAllowed(route):
    @wraps(route)
    def decorated_route(*args, **kwargs):
        if not(session.get('user_id') is None):
            return redirect('/')
        return route(*args, **kwargs)
    return decorated_route