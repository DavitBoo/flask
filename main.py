from models import app, db, Usuario # importp tpdp del archivo models.py
from flask import request, redirect, url_for, render_template, session

# Crear las tablas en la base de datos (si no existen)
with app.app_context():
    db.create_all()



@app.route('/')
def home():
    return render_template("index.html")
# registrar un usuario con HASH
@app.route('/registro', methods=['GET', 'POST'])
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
        return "Usuario registrado con éxito! Tu contraseña se guardó como un hash."
        
    return render_template("register.html")

# verificar un login con HASH
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        usuario = Usuario.query.filter_by(username=username).first()
        
        # Comprobar si el usuario existe Y si el hash coincide con la contraseña escrita
        if usuario and usuario.check_password(password):
            session['user_id'] = username.id
            return f"Bienvenido {username}! Has hecho login correctamente."
        else:
            return "Usuario o contraseña incorrectos."
            
    return render_template("login.html")

# ! tengo que crear logout

if __name__ == '__main__':
    app.run(debug=True)
    