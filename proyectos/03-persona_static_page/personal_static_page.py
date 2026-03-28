from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return "<h1>Sobre mí</h1><p>Esta es la página sobre mí.</p>"

@app.route("/contact")
def contact():
    return "<h1>Contacto</h1><p>Email: ejemplo@email.com</p>"

if __name__ == "__main__":
    app.run(debug=True)