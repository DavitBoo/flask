from functools import wraps
from flask_login import current_user

def admin_required_api(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Verificamos si el usuario está autenticado y si es admin
        if not current_user.is_authenticated or not current_user.is_admin():
            return {
                'message': 'Acceso denegado. Se requieren permisos de administrador.'
            }, 403
        return f(*args, **kwargs)
    return wrapper
