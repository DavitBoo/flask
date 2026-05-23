from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tareas.db"
db = SQLAlchemy(app)

# definir el modelo con dos columnas de la tabla en este caso. Solo una tabla.
class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    
# Esto es para que se creen las tablas automáticamente al iniciar la app
with app.app_context():
    db.create_all()

# Resources es un abstract class, de la cual en este caso TareasResource va a heredar.
# esta clase abstract me permite definir los métodos HTTP get, post, etc. tan fácil como def get(self): ...
class TareasResource(Resource):

    def get(self):
        # Obtenemos todas las tareas de la base de datos
        tareas = Tarea.query.all()
        return {"tareas": [{"id": t.id, "titulo": t.titulo} for t in tareas]}

    def post(self):
        data = request.json
        # Creamos una nueva tarea y la guardamos en la base de datos
        nueva_tarea = Tarea(titulo=data['titulo'])
        db.session.add(nueva_tarea)
        db.session.commit()
        return {"mensaje": "Tarea creada", "id": nueva_tarea.id}, 201


class TareaResource(Resource):

    def get(self, id):
        # Buscamos la tarea por su id
        tarea = Tarea.query.get(id)
        if tarea:
            return {"id": tarea.id, "titulo": tarea.titulo}
        return {"mensaje": "Tarea no encontrada"}, 404

    def delete(self, id):
        tarea = Tarea.query.get(id)
        if tarea:
            db.session.delete(tarea)
            db.session.commit()
            return {"mensaje": "Eliminada"}
        return {"mensaje": "Tarea no encontrada"}, 404

    def put(self, id):
        data = request.json
        tarea = Tarea.query.get(id)
        if tarea:
            tarea.titulo = data.get('titulo', tarea.titulo)
            db.session.commit()
            return {"mensaje": "Tarea actualizada"}
        return {"mensaje": "Tarea no encontrada"}, 404


api.add_resource(TareasResource, "/tareas")
api.add_resource(TareaResource, "/tareas/<int:id>")

if __name__ == "__main__":
    app.run(debug=True)