from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"

db = SQLAlchemy(app)

class Usuario(db.Model, UserMixin):     # Herencia múltiple de UserMixing sobre nuestra clase Usuario. Ganamos así 4 métodos nuevos entre ellos is_acitve
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password): # self es el usuario de la instancia que lo llama
        return check_password_hash(self.password, password) # aquí comparo self.password (la hashed de la DB) con la contraseña introducida (pwhash, password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    
    autor = db.relationship('Usuario', backref=db.backref('posts', lazy=True))