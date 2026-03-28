from flask import Flask, render_template, request, session
import random   

app = Flask(__name__)

app.secret_key = "clave_super_secreta"

@app.route("/")
def contador():
    if "visitas" in session:    # si está marcado con la clave secreta y devuelve la session tendrá "visitas"
        session["visitas"] += 1
    else: 
        session["visitas"] = 1
    
    return render_template("index.html", visitas=session["visitas"])

if __name__ == "__main__":
    app.run(debug=True)