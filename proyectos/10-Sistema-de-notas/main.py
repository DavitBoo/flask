from flask import Flask, flash, redirect, redirect, render_template, request, url_for
import json


app = Flask(__name__)

notas = []

#if notas.json no existe, se crea un archivo vacio
try:
    with open("notas.json") as f:
        notas = json.load(f)
except FileNotFoundError:
    with open("notas.json", "w") as f:
        json.dump(notas, f)
        
def guardar_notas():        
    with open("notas.json", "w") as f:
        json.dump(notas, f)

@app.route("/", methods=["GET", "POST"])
def index():
    
    
    if request.method == "POST":
        titulo = request.form["titulo"]
        contenido = request.form["contenido"]
        
        if titulo and contenido:
            nota = {
                "id": len(notas) + 1,
                "titulo": titulo,
                "contenido": contenido
            }
            
            notas.append(nota)        
        guardar_notas()
        return redirect(url_for("index"))

    return render_template("index.html", notas=notas)

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    nota = None
    # cuando encuentra la nota sale del bucle
    for n in notas:
        if n["id"] == id:
            nota = n
            break            
                        
    if nota is None:
        return redirect(url_for("index"))
    
    if request.method == "POST":
        nota["titulo"] = request.form["titulo"]
        nota["contenido"] = request.form["contenido"]
        guardar_notas()
        return redirect(url_for("index"))    
    
    return render_template("editar.html", nota=nota)

@app.route("/borrar/<int:id>")
def borrar(id):    
    global notas
    notas = [n for n in notas if n["id"] != id ]
    guardar_notas()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
    