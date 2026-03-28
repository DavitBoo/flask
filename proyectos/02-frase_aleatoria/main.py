from flask import Flask, render_template, request
import random   

app = Flask(__name__)

frases = [
    "Nunca te rindas",
    "El éxito es la suma de pequeños esfuerzos",
    "Aprende algo nuevo cada día",
    "La creatividad es inteligencia divirtiéndose.",
    "El conocimiento es poder.",
    "Nunca dejes de aprender.",
    "Los grandes proyectos empiezan con un pequeño paso.",
    "El éxito es la suma de pequeños esfuerzos repetidos."
]

def frase():
    resultado =  random.choice(frases)
    return resultado

@app.route("/", methods=["GET", "POST"])
def mostrarFrase():
    fraseRandom = ''
    if request.method == "POST": 
        fraseRandom = frase()   
    
    return render_template("index.html", fraseRandom=fraseRandom)

if __name__ == "__main__":
    app.run(debug=True)