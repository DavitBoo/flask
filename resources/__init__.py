from flask import Blueprint
from flask_restful import Api
from .blog import PostListResource, PostResource
from .auth import LoginResource, LogoutResource, RegisterResource, ProfileResource
from .comments import CommentListResource, CommentResource

# Creamos el Blueprint para la API
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Registramos los recursos
api.add_resource(PostListResource, '/posts')
api.add_resource(PostResource, '/posts/<int:post_id>')
api.add_resource(LoginResource, '/auth/login')
api.add_resource(LogoutResource, '/auth/logout')
api.add_resource(RegisterResource, '/auth/register')
api.add_resource(ProfileResource, '/auth/me')

# Recursos de Comentarios
api.add_resource(CommentListResource, '/posts/<int:post_id>/comments')
api.add_resource(CommentResource, '/comments/<int:comment_id>')
