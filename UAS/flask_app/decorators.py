from functools import wraps
from flask import abort, request, session, redirect, url_for

# def check_is_htmx(request):
#     if not request.headers.get("HX-Request"):
#         abort(403)

# decorator cek apakah request berasal dari htmx

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return wrapper

def hx_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.headers.get("HX-Request") != "true":
            abort(403)
        return func(*args, **kwargs)

    return wrapper
