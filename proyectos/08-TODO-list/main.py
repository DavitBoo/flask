from flask import Flask, flash, redirect, redirect, render_template, request, url_for

app = Flask(__name__)

tareas = []

@app.route("/", methods=["GET", "POST", "DELETE"])
def aniadirTarea():
    if request.method == "POST":
        tarea = request.form["tarea"]
        if tarea:
            tareas.append(tarea)
            
        # Redirigimos (patrón PRG - Post/Redirect/Get)
        return redirect(url_for("aniadirTarea"))
            
    return render_template("index.html", tareas=tareas)


@app.route("/borrar/<int:id>")
def borrarTarea(id):
    if 0 <= id < len(tareas):
        tareas.remove(tareas[id])
    return redirect(url_for("aniadirTarea"))    


if __name__ == "__main__":
    app.run(debug=True)
    
    