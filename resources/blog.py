from flask_restful import Resource
from models import Post

class PostListResource(Resource):
    def get(self):
        # Obtenemos todos los posts de la base de datos
        posts = Post.query.all()
        # Los convertimos a una lista de diccionarios (JSON)
        # En el futuro usaremos Marshmallow para esto, pero ahora lo hacemos manual
        return [
            {
                'id': p.id,
                'titulo': p.titulo,
                'contenido': p.contenido,
                'user_id': p.user_id
            } for p in posts
        ], 200

class PostResource(Resource):
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        return {
            'id': post.id,
            'titulo': post.titulo,
            'contenido': post.contenido,
            'user_id': post.user_id
        }, 200
