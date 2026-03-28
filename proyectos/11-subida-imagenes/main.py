import os
from flask import Flask, flash, redirect, render_template, request, url_for, session
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "mi_clave_secreta_123"     # Necesario para session y flash

UPLOAD_FOLDER = os.path.join('static', 'upload')
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def permitido(nombre):
    return "." in nombre and nombre.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        
        if 'imagen' not in request.files or not request.files['imagen'].filename:
            flash('No se ha seleccionado ningún archivo.', 'error')
            return redirect(url_for('index'))
        
        imagen = request.files['imagen']
        nombre = secure_filename(imagen.filename)

        if permitido(nombre):
            ruta_destino = os.path.join(UPLOAD_FOLDER, nombre)
            imagen.save(ruta_destino)
            session['ultima_imagen'] = nombre          # ← Guardamos el nombre
        else:
            flash('Tipo de archivo no permitido. Solo se permiten: png, jpg, jpeg, gif', 'error')

        return redirect(url_for('index'))

    # GET: mostramos la última imagen guardada en esta sesión
    ultima_imagen = session.get('ultima_imagen')   # None si no hay ninguna

    return render_template("index.html", nombre_imagen=ultima_imagen)


if __name__ == "__main__":
    app.run(debug=True) 