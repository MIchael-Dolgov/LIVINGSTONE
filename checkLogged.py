from flask import session, redirect
from functools import wraps

def check_logged_in(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "logged_in" in session:
            return func(*args, **kwargs)
        return redirect("/login")
    return wrapper

def check_logged_in_for_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "logged_in" in session:
            return func(*args, **kwargs)
        return redirect("/login")
    return wrapper

def user_status() -> str:
    if "logged_in" in session:
        name = session["logged_in"]
        return f"{name}"
    else:
        return ""
    