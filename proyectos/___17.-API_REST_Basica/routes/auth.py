from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_user, logout_user, current_user
from models import db, Usuario

auth_bp = Blueprint('auth', __name__)

# registrar un usuario con HASH
@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Crear nuevo usuario (instancia del Modelo)
        usuario = Usuario(username=username)
        # Generar el hash y guardarlo en el campo password
        # Este método usa werkzeug.security internamente
        usuario.set_password(password)
        
        db.session.add(usuario)
        db.session.commit()
        flash("Usuario registrado con éxito! Ahora puedes iniciar sesión.", "success")
        return redirect(url_for("auth.login"))
        
    return render_template("register.html")

# verificar un login con HASH
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("Ya tienes la sesión iniciada 😀", "success" )
        return redirect(url_for("main.home"))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        usuario = Usuario.query.filter_by(username=username).first()
        
        # Comprobar si el usuario existe Y si el hash coincide con la contraseña escrita
        if usuario and usuario.check_password(password):
            login_user(usuario) # como session['user_id'] = usuario.id pero más automático no solo guarda el id del usuario en la sesión
            flash(f"¡Bienvenido {usuario.username}! Has iniciado sesión correctamente.", "success")
            return redirect(url_for("main.home"))
        else:
            flash("Usuario o contraseña incorrectos.", "error")
            return redirect(url_for("auth.login"))
            
    return render_template("login.html")

@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash("¡Hasta la próxima! Has cerrado sesión correctamente.", "success")
    return redirect(url_for("main.home"))
