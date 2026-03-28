from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = "tu_clave_secreta_super_secreta"   # session

# Funciones de conversión
def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

def fahrenheit_to_celsius(f):
    return (f - 32) * 5/9

def km_to_millas(km):
    return km * 0.621371

def millas_to_km(millas):
    return millas / 0.621371


@app.route("/", methods=["GET", "POST"])
def conversor():
    resultado = None
    error = None
    valor = ""
    conversion_seleccionada = "km_millas"  # valor por defecto

    if request.method == "POST":
        valor_str = request.form.get("valor", "").strip()
        conversion = request.form.get("conversion")

        try:
            if not valor_str:
                error = "Por favor ingresa un número"
            else:
                valor_num = float(valor_str)

                if conversion == "c_f":
                    res = celsius_to_fahrenheit(valor_num)
                    resultado = f"{res:.2f} °F"
                elif conversion == "f_c":
                    res = fahrenheit_to_celsius(valor_num)
                    resultado = f"{res:.2f} °C"
                elif conversion == "km_millas":
                    res = km_to_millas(valor_num)
                    resultado = f"{res:.2f} millas"
                elif conversion == "millas_km":
                    res = millas_to_km(valor_num)
                    resultado = f"{res:.2f} km"
                else:
                    error = "Conversión no reconocida"

                # Guardamos para mantener en el formulario
                valor = valor_str
                conversion_seleccionada = conversion

        except ValueError:
            error = "Ingresa un número válido (ej: 23.5)"

    return render_template(
        "index.html",
        resultado=resultado,
        error=error,
        valor=valor,
        conversion_seleccionada=conversion_seleccionada
    )


if __name__ == "__main__":
    app.run(debug=True)