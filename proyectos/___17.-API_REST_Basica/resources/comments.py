from flask import request
# ahora entiendo Resource. Es una class abstracta, la cual va a servir de padre para la clase que vamos a crear después.
# Esto significa que la clase que vamos a crear después va a heredar todos los métodos y atributos de Resource.
from flask_restful import Resource
from flask_login import current_user, login_required
from models import db, Comentario, Post
from datetime import datetime

class CommentListResource(Resource):
    def get(self, post_id):
        # Buscamos el post para asegurarnos de que existe
        post = Post.query.get_or_404(post_id)
        # Devolvemos sus comentarios
        return [
            {
                'id': c.id,
                'contenido': c.contenido,
                'fecha': c.fecha.strftime('%Y-%m-%d %H:%M:%S') if c.fecha else None,
                'usuario': c.usuario.username
            } for c in post.comentarios
        ], 200

    @login_required
    def post(self, post_id):
        # Verificar que el post existe
        Post.query.get_or_404(post_id)
        
        data = request.get_json()
        if not data or not data.get('contenido'):
            return {'message': 'El contenido es obligatorio'}, 400
            
        nuevo_comentario = Comentario(
            contenido=data.get('contenido'),
            fecha=datetime.now(),
            post_id=post_id,
            usuario_id=current_user.id
        )
        
        db.session.add(nuevo_comentario)
        db.session.commit()
        
        return {
            'message': 'Comentario creado con éxito',
            'comment': {
                'id': nuevo_comentario.id,
                'contenido': nuevo_comentario.contenido,
                'fecha': nuevo_comentario.fecha.strftime('%Y-%m-%d %H:%M:%S')
            }
        }, 201

class CommentResource(Resource):
    @login_required
    def delete(self, comment_id):
        comentario = Comentario.query.get_or_404(comment_id)
        
        # Seguridad: Solo el autor o un admin pueden borrar
        if comentario.usuario_id != current_user.id and not current_user.is_admin():
            return {'message': 'No tienes permiso para borrar este comentario'}, 403
            
        db.session.delete(comentario)
        db.session.commit()
        return {'message': 'Comentario eliminado'}, 200
