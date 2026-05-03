from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required, current_user
from models import db, Post, Comentario
from utils.decorators import admin_required

blog_bp = Blueprint('blog', __name__)

# --- CRUD DE POSTS ---

@blog_bp.route('/post/nuevo', methods=['GET', 'POST'])
@login_required     # decorador de flask login
def nuevo_post():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        contenido = request.form.get('contenido')

        if not titulo or not contenido or contenido.strip() == "":
            flash("El título y el contenido no pueden estar vacíos", "error")
            return redirect(url_for("blog.nuevo_post"))
        
        nuevo = Post(titulo=titulo, contenido=contenido, user_id=current_user.id)
        db.session.add(nuevo)
        db.session.commit()
        
        flash("¡Post publicado con éxito!", "success")
        return redirect(url_for('main.home'))
        
    return render_template("nuevo_post.html")

@blog_bp.route('/post/<int:id>')
def ver_post(id):
    post = Post.query.get_or_404(id) # no necesito previamente pasarle el modelo a get_or_404 como parámetro
    return render_template("ver_post.html", post=post)

@blog_bp.route('/post/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_post(id):
    post = Post.query.get_or_404(id)
    
    # Solo el autor puede editar
    if current_user.id != post.user_id:
        flash("No tienes permiso para editar este post.", "error")
        return redirect(url_for('main.home'))
        
    if request.method == 'POST':
        post.titulo = request.form.get('titulo')
        post.contenido = request.form.get('contenido')
        db.session.commit()
        flash("Post actualizado.", "success")
        return redirect(url_for('main.home'))
        
    return render_template("nuevo_post.html", post=post)

@blog_bp.route('/post/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_post(id):
    post = Post.query.get_or_404(id)
    
    if current_user.id != post.user_id:
        flash("No puedes eliminar este post.", "error")
        return redirect(url_for('home'))
        
    db.session.delete(post)
    db.session.commit()
    flash("Post eliminado correctamente.", "success")
    return redirect(url_for('home'))

@blog_bp.route('/post/<int:id>/comentario', methods=['POST'])
@login_required
def publicar_comentario(id):
    contenido = request.form.get("contenido")
    if contenido and contenido.strip() != "":
        comentario = Comentario(
            contenido=contenido,
            post_id=id,
            usuario_id=current_user.id
        )
        db.session.add(comentario)
        db.session.commit()
        flash("Comentario añadido", "success")
    else:
        flash("El comentario no puede estar vacío", "error")
    return redirect(url_for("blog.ver_post", id=id))

@blog_bp.route('/post/<int:id>/comentario/<int:commentId>', methods=['POST'])
@login_required
@admin_required
def borrar_comentario(id, commentId):
    comentario = Comentario.query.get_or_404(commentId)
    if comentario.usuario_id == current_user.id or comentario.post.user_id == current_user.id:
        db.session.delete(comentario)
        db.session.commit()
        flash("Comentario eliminado correctamente", "success")
    else:
        flash("No tienes permiso para eliminar este comentario", "error")
    return redirect(url_for("blog.ver_post", id=id))
