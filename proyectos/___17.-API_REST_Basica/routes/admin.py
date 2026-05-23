from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Usuario, Post, Comentario
from utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@login_required
@admin_required # llama a admin_required(admin) (sin parentesis en admin), al ir a /admin, se ejecuta el wrapper primero 
def dashboard():
    total_usuarios = Usuario.query.count()
    total_posts = Post.query.count()
    total_comentarios = Comentario.query.count()
    return render_template("admin/dashboard.html", 
                         total_usuarios=total_usuarios, 
                         total_posts=total_posts, 
                         total_comentarios=total_comentarios)

@admin_bp.route('/admin/usuarios')
@login_required
@admin_required
def usuarios_list():
    usuarios = Usuario.query.all()
    return render_template("admin/usuarios.html", usuarios=usuarios)

@admin_bp.route('/admin/posts')
@login_required
@admin_required
def posts_list():
    posts = Post.query.all()
    return render_template("admin/posts.html", posts=posts)

@admin_bp.route("/admin/borrar_usuario/<int:id>", methods=['POST'])
@login_required
@admin_required
def borrar_usuario(id):
    if id == current_user.id:
        flash("No puedes eliminarte a ti mismo.", "error")
        return redirect(url_for("admin.usuarios_list"))
    
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash(f"Usuario {usuario.username} eliminado correctamente.", "success")
    return redirect(url_for("admin.usuarios_list"))
