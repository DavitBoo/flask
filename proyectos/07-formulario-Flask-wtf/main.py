from flask import Flask, flash, redirect, redirect, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length


app = Flask(__name__)

# ¡MUY IMPORTANTE! Necesito una secret_key para la protección CSRF
app.config['SECRET_KEY'] = 'tu-clave-secret/\-super-difiçil-123-cambia-esto'  


class ContactoForm(FlaskForm):
    nombre = StringField(
        'Nombre',
        validators=[
            DataRequired(message="El nombre es obligatorio"),
            Length(min=2, max=80, message="El nombre debe tener entre 2 y 80 caracteres")
        ]
    )
    
    email = StringField(
        'Email',
        validators=[
            DataRequired(message="El email es obligatorio"),
            Email(message="Por favor ingresa un email válido (ej: nombre@ejemplo.com)")
        ]
    )
    
    mensaje = TextAreaField(
        'Mensaje',
        validators=[
            DataRequired(message="El mensaje no puede estar vacío"),
            Length(min=10, max=2000, message="El mensaje debe tener entre 10 y 2000 caracteres")
        ]
    )
    
    enviar = SubmitField('Enviar mensaje')

@app.route("/", methods=["GET", "POST"])
def formulario():
    form = ContactoForm()   # Creamos una instancia del formulario

    if request.method == "POST":
        
        if form.validate_on_submit(): # Valida CSRF + todos los validators. Este método comprueba por nosotros que se ha enviado el formulario y que todos sus campos son válidos. 
            nombre = form.nombre.data
            email = form.email.data
            mensaje = form.mensaje.data
            
            # Ejemplo: mostrar mensaje de éxito (en producción  enviar email, guardar en DB, etc.)
            flash(f"¡Gracias {nombre}! Tu mensaje fue enviado correctamente.", "success")
            
            # Redirigimos (patrón PRG - Post/Redirect/Get)
            return redirect(url_for("formulario"))      # redirige a la ruta /formulario, dentro de la propia función con un GET.
        
    return render_template("index.html", form=form)



if __name__ == "__main__":
    app.run(debug=True)