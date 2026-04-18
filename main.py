from models import app, db, Usuario
from flask_login import LoginManager

# Import Blueprints
from routes.auth import auth_bp
from routes.blog import blog_bp
from routes.admin import admin_bp
from routes.main import main_bp

# Login Manager Initialization
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login" # Redirige si intentan ir a links con @login_required

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id)) # si el id es válido, devuelve el usuario

app.secret_key = "mi_clave_secreta_123" 

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(blog_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(main_bp)

# Crear las tablas en la base de datos (si no existen)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)