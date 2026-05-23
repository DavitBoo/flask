from flask_restful import Resource
from flask_login import login_required, current_user
from models import db, Usuario, Post, Comentario
from utils.api_decorators import admin_required_api

class AdminDashboardResource(Resource):
    @login_required
    @admin_required_api
    def get(self):
        # Estadísticas generales para el panel de control
        return {
            'total_usuarios': Usuario.query.count(),
            'total_posts': Post.query.count(),
            'total_comentarios': Comentario.query.count()
        }, 200

class AdminUserListResource(Resource):
    @login_required
    @admin_required_api
    def get(self):
        # Lista completa de usuarios
        usuarios = Usuario.query.all()
        return [
            {
                'id': u.id,
                'username': u.username,
                'rol': u.rol,
                'total_posts': len(u.posts)
            } for u in usuarios
        ], 200

class AdminUserResource(Resource):
    @login_required
    @admin_required_api
    def delete(self, user_id):
        # Protección para no borrarse a uno mismo
        if user_id == current_user.id:
            return {'message': 'No puedes eliminar tu propia cuenta de administrador'}, 400
            
        usuario = Usuario.query.get_or_404(user_id)
        db.session.delete(usuario)
        db.session.commit()
        
        return {'message': f'Usuario {usuario.username} eliminado correctamente'}, 200
