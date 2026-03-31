from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template, url_for, redirect

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tareas.db"
# ### DEBUG
# for key, value in app.config.items():
#     print(f"{key}: {value}")

db = SQLAlchemy(app) #Ahora SQLAlchemy sabe que debe ir a buscar dentro de app.config la dirección de la base de datos (SQLALCHEMY_DATABASE_URI)

# definir el modelo con dos columnas de la tabla en este caso. Solo una tabla.
class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    
# Esto es para que se creen las tablas automáticamente al iniciar la app
with app.app_context():
    db.create_all()
    
@app.route("/")
def index():
    tareas = Tarea.query.all()
    return render_template('index.html', tareas=tareas)

@app.route("/crear", methods=["POST"])
def crear():
    titulo = request.form["title"]
    nueva = Tarea(titulo=titulo)
    db.session.add(nueva)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/actualizar/<int:id>", methods=["POST"])
def actualizar(id):
    return

@app.route("/eliminar/<int:id>")
def eliminar(id):
    tarea = Tarea.query.get(id)
    db.session.delete(tarea)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/tarea/<string:title>")
def buscar(title):
    Tarea.query.filter_by(titulo=title).all()
    return


if __name__ == "__main__":
    app.run(debug=True) 