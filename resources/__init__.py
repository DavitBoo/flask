from flask import Blueprint
from flask_restful import Api
from .blog import PostListResource, PostResource

# Creamos el Blueprint para la API
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Registramos los recursos
api.add_resource(PostListResource, '/posts')
api.add_resource(PostResource, '/posts/<int:post_id>')
