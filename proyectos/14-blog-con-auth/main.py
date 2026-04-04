from models import app, db, Usuario, Post # importp tpdp del archivo models.py
from flask import request, redirect, url_for, render_template, flash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login" # Redirige si intentan ir a links con @login_required

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))  # si el id es válido, devuelve el usuario

app.secret_key = "mi_clave_secreta_123" 

# Crear las tablas en la base de datos (si no existen)
with app.app_context():
    db.create_all()



@app.route('/')
def home():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)

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
        flash("Usuario registrado con éxito! Ahora puedes iniciar sesión.", "success")
        return redirect(url_for("login"))
        
    return render_template("register.html")

# verificar un login con HASH
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("Ya tienes la sesión iniciada 😀", "success" )
        return redirect(url_for("home"))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        usuario = Usuario.query.filter_by(username=username).first()
        
        # Comprobar si el usuario existe Y si el hash coincide con la contraseña escrita
        if usuario and usuario.check_password(password):
            login_user(usuario) # como session['user_id'] = usuario.id pero más automático no solo guarda el id del usuario en la sesión
            flash(f"¡Bienvenido {usuario.username}! Has iniciado sesión correctamente.", "success")
            return redirect(url_for("home"))
        else:
            flash("Usuario o contraseña incorrectos.", "error")
            return redirect(url_for("login"))
            
    return render_template("login.html")

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash("¡Hasta la próxima! Has cerrado sesión correctamente.", "success")
    return redirect(url_for("home")) 
# --- CRUD DE POSTS ---

@app.route('/post/nuevo', methods=['GET', 'POST'])
@login_required     # decorador de flask login
def nuevo_post():
        
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        contenido = request.form.get('contenido')
        
        nuevo = Post(titulo=titulo, contenido=contenido, user_id=current_user.id)
        db.session.add(nuevo)
        db.session.commit()
        
        flash("¡Post publicado con éxito!", "success")
        return redirect(url_for('home'))
        
    return render_template("nuevo_post.html")

@app.route('/post/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_post(id):
    post = Post.query.get_or_404(id)    # no necesito previamente pasarle el modelo a get_or_404 como parámetro
    
    # Solo el autor puede editar
    if current_user.id != post.user_id:
        flash("No tienes permiso para editar este post.", "error")
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        post.titulo = request.form.get('titulo')
        post.contenido = request.form.get('contenido')
        db.session.commit()
        flash("Post actualizado.", "success")
        return redirect(url_for('home'))
        
    return render_template("nuevo_post.html", post=post)

@app.route('/post/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_post(id):
    post = Post.query.get_or_404(id)
    
    if current_user.id != post.user_id:
        flash("No puedes eliminar este post.", "error")
        return redirect(url_for('home'))
        
    db.session.delete(post)
    db.session.commit()
    flash("Post eliminado correctamente.", "success")
    return redirect(url_for('home'))
if __name__ == '__main__':
    app.run(debug=True)
    