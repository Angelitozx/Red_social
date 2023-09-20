from flask import Flask, render_template, request, redirect, url_for, send_file
import database as db
import io

# Declarando nombre de la aplicación e inicializando
app = Flask(__name__)

@app.route('/')
def index():
    cursor = db.database.cursor()
    cursor.execute("SELECT id, nombre FROM imagenes")
    imagenes = cursor.fetchall()
    cursor.close()
    return render_template('subir_imagen.html', imagenes=imagenes)

@app.route('/subir', methods=['POST'])
def subir_imagen():
    if request.method == 'POST':
        imagen = request.files['imagen']
        nombre = request.form['nombre']

        if imagen:
            cursor = db.database.cursor()
            cursor.execute("INSERT INTO imagenes (nombre, imagen) VALUES (%s, %s)", (nombre, imagen.read()))
            db.database.commit()
            cursor.close()
            return redirect(url_for('index'))

@app.route('/mostrar/<int:id>')
def mostrar_imagen(id):
    cursor = db.database.cursor()
    cursor.execute("SELECT nombre, imagen FROM imagenes WHERE id = %s", (id,))
    result = cursor.fetchone()
    cursor.close()

    if result:
        nombre, imagen_bytes = result
        return send_file(
            io.BytesIO(imagen_bytes),
            mimetype='image/jpeg',  # Cambia 'image/jpeg' al tipo MIME correcto de tu imagen
            as_attachment=False,
            download_name=f"{nombre}.jpg"  # Cambia la extensión del archivo si es necesario
        )
    else:
        return "Imagen no encontrada"

if __name__ == '__main__':
    app.run(debug=True, port=5000)