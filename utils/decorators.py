from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def admin_required(f): # f recibe la función admin (si llamamos al decorador antes de def admin:)
    @wraps(f)   # necesitamos el decorador wraps (interno de python) para que admin_required sea de __name__ admin_required y no wrapper
    def wrapper(*args, **kwargs): #args y kwargs son convenciones, se pueden modificar durante el decorador
        if not current_user.is_authenticated or not current_user.is_admin():
            flash("No tienes permisos para acceder a esta página.", "error")
            return redirect(url_for("main.home"))
        return f(*args, **kwargs) # esto hace que se ejecute la función original (si llega hasta aquí)
    return wrapper
