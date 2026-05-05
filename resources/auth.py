from flask import request
from flask_restful import Resource
from flask_login import login_user, logout_user, current_user
from models import db, Usuario

class LoginResource(Resource):
    def post(self):
        # En una API pura, recibimos los datos en formato JSON
        data = request.get_json()
        if not data:
            return {'message': 'No se proporcionaron datos'}, 400
                   
        username = data.get('username')
        password = data.get('password')
        
        usuario = Usuario.query.filter_by(username=username).first()
        
        if usuario and usuario.check_password(password):
            login_user(usuario)
            return {
                'message': f'¡Bienvenido {usuario.username}!',
                'user': {
                    'id': usuario.id,
                    'username': usuario.username,
                    'rol': usuario.rol
                }
            }, 200
        return {'message': 'Usuario o contraseña incorrectos'}, 401

class LogoutResource(Resource):
    def post(self):
        logout_user()
        return {'message': 'Sesión cerrada correctamente'}, 200

class RegisterResource(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {'message': 'No se proporcionaron datos'}, 400
            
        username = data.get('username')
        password = data.get('password')
        
        if Usuario.query.filter_by(username=username).first():
            return {'message': 'El nombre de usuario ya está en uso'}, 400
            
        nuevo_usuario = Usuario(username=username)
        nuevo_usuario.set_password(password)
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        return {
            'message': 'Usuario registrado con éxito',
            'user': {'username': username}
        }, 201

class ProfileResource(Resource):
    def get(self):
        if current_user.is_authenticated:
            return {
                'id': current_user.id,
                'username': current_user.username,
                'rol': current_user.rol
            }, 200
        return {'message': 'No has iniciado sesión'}, 401
