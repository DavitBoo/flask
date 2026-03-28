import os
from flask import Flask, flash, redirect, render_template, request, url_for, session
from werkzeug.utils import secure_filename

app = Flask(__name__)

votos = {
    "python": 0,
    "javascript": 0,
    "php": 0
}

@app.route("/", methods=["GET", "POST"])
def encuesta():
    opcion = None
    if request.method == "POST":
        opcion = request.form["opcion"]
        votos[opcion] += 1
        return redirect(url_for('encuesta'))
    
    return render_template("encuesta.html")

@app.route("/resultados")
def resultados():
    return render_template("resultados.html", votos=votos)


if __name__ == "__main__":
    app.run(debug=True) 