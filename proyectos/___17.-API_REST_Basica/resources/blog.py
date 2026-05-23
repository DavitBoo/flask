from flask import request
from flask_restful import Resource
from flask_login import current_user, login_required
from models import db, Post

class PostListResource(Resource):
    def get(self):
        # Obtenemos todos los posts de la base de datos
        posts = Post.query.all()
        # Los convertimos a una lista de diccionarios (JSON)
        return [
            {
                'id': p.id,
                'titulo': p.titulo,
                'contenido': p.contenido,
                'user_id': p.user_id,
                'autor': p.autor.username if p.autor else None
            } for p in posts
        ], 200

    @login_required
    def post(self):
        data = request.get_json()
        if not data or not data.get('titulo') or not data.get('contenido'):
            return {'message': 'El título y el contenido son obligatorios'}, 400
            
        nuevo_post = Post(
            titulo=data.get('titulo'),
            contenido=data.get('contenido'),
            user_id=current_user.id
        )
        
        db.session.add(nuevo_post)
        db.session.commit()
        
        return {
            'message': 'Post creado con éxito',
            'post': {
                'id': nuevo_post.id,
                'titulo': nuevo_post.titulo,
                'contenido': nuevo_post.contenido,
                'user_id': nuevo_post.user_id
            }
        }, 201

class PostResource(Resource):
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        return {
            'id': post.id,
            'titulo': post.titulo,
            'contenido': post.contenido,
            'user_id': post.user_id,
            'autor': post.autor.username if post.autor else None
        }, 200

    @login_required
    def put(self, post_id):
        post = Post.query.get_or_404(post_id)
        
        # Seguridad: Solo el autor o un admin pueden editar el post
        if post.user_id != current_user.id and not current_user.is_admin():
            return {'message': 'No tienes permiso para editar este post'}, 403
            
        data = request.get_json()
        if not data:
            return {'message': 'No se proporcionaron datos para actualizar'}, 400
            
        if 'titulo' in data:
            if not data.get('titulo'):
                return {'message': 'El título no puede estar vacío'}, 400
            post.titulo = data.get('titulo')
            
        if 'contenido' in data:
            if not data.get('contenido'):
                return {'message': 'El contenido no puede estar vacío'}, 400
            post.contenido = data.get('contenido')
            
        db.session.commit()
        
        return {
            'message': 'Post actualizado con éxito',
            'post': {
                'id': post.id,
                'titulo': post.titulo,
                'contenido': post.contenido,
                'user_id': post.user_id
            }
        }, 200

    @login_required
    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        
        # Seguridad: Solo el autor o un admin pueden borrar el post
        if post.user_id != current_user.id and not current_user.is_admin():
            return {'message': 'No tienes permiso para borrar este post'}, 403
            
        db.session.delete(post)
        db.session.commit()
        
        return {'message': 'Post eliminado correctamente'}, 200

