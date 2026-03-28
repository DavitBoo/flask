from flask import Flask, flash, redirect, redirect, render_template, request, url_for

app = Flask(__name__)

posts = [
    {
        "id": 1,
        "titulo": "Mi primer post",
        "contenido": "Hola, este es mi blog",
        "fecha": "2024-06-01"
    },
    {
        "id": 2,
        "titulo": "Aprendiendo Flask",
        "contenido": "Flask es un framework muy ligero",
        "fecha": "2024-06-02"
    }
]

@app.route("/")
def index():
    return render_template("index.html", posts=posts)

@app.route("/post/<int:id>")
def post(id):
    for post in posts:
        if post["id"] == id:    
            return render_template("post.html", post=post)


if __name__ == "__main__":
    app.run(debug=True)
    