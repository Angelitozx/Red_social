from flask import Flask,flash, render_template, request,redirect, redirect, url_for, send_file, session
from flask_mail import Mail, Message
import os
import io
import database as db

#Declarar una variables donde estará nuestra carpeta principal  "Prueba flask"
template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
#Unir src y templates a la carpeta de proyectos
template_dir = os.path.join(template_dir, 'src' ,  'templates')

#Una varaibles para inicializar flask  
app = Flask(__name__, template_folder = template_dir)

#------------configuracion de correos-------------#
app.config.update(dict(                     #
    DEBUG = True,                           #
    MAIL_SERVER = 'smtp.gmail.com',         #
    MAIL_PORT = 587,                        # Configuramos la smtp gratis de gmail
    MAIL_USE_TLS = True,                    #   
    MAIL_USE_SSL = False,                   #
    MAIL_USERNAME = 'mariojuancho23@gmail.com',                #
    MAIL_PASSWORD = '123',             #
))

PROFILE_UPLOAD_FOLDER = os.path.abspath('./static/profileImages')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpge', 'gif'])
app.config["PROFILE_UPLOAD_FOLDER"] = PROFILE_UPLOAD_FOLDER

# Inicializar el servidor de correos
mail = Mail(app)

# Configurar la clave secreta para sesiones
app.secret_key = os.urandom(32)

def allowed_file(filename):
    return " " in filename and filename.rsplit(".", 1)[1] not in ALLOWED_EXTENSIONS

#Rutas de la aplicación, se pone / para que con el propio nombre de la app acceda el index
@app.route('/')
def home():
    #Crear un cursor apra acceder a la base de datos
    cursor = db.database.cursor()
    #Hacer la consulta select
    cursor.execute("SELECT * FROM users")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [colum[0] for colum in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()

#-----------PUBLICACION INICIALIZACION----------#
    #Crear un cursor apra acceder a la base de datos
    cursor2 = db.database.cursor()    
    #Hacer la consulta select
    cursor2.execute("SELECT * FROM articles")
    myresult2 = cursor2.fetchall()
    #Convertir los datos a diccionario
    insertObject2 = []
    columnNames2 = [colum[0] for colum in cursor2.description]
    for record in myresult2:
        insertObject2.append(dict(zip(columnNames2, record)))
    cursor2.close()

#-----------SUBIDA DE IMAGENES INICIALIZACION-------------#
    cursor3 = db.database.cursor()
    cursor3.execute("SELECT id, nombre FROM imagenes")
    imagenes = cursor3.fetchall()
    cursor3.close()

#-----------Esta es la renderizacion de todo-----------------------#
    return render_template ('index.html', data=insertObject, data2=insertObject2, imagenes=imagenes)

#--------------VERIFICACION DE CORREO Y LOGIN--------------------------#
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']

        cursor4 = db.database.cursor(dictionary=True)  # Configura el cursor para devolver resultados como diccionarios
        sql = "SELECT * FROM users WHERE correo = %s AND password = %s"
        data = (correo, password)
        cursor4.execute(sql, data)
        user = cursor4.fetchone()
        cursor4.close()

        if user:
            session['user_id'] = user['id_users']

            # Enviar un mensaje de correo electrónico después de iniciar sesión
            msg = Message('Inicio de sesión exitoso', sender='tu_correo@gmail.com', recipients=[user['correo']])
            msg.body = '¡Bienvenido! Has iniciado sesión en nuestra aplicación.'
            mail.send(msg)

            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('home'))
        else:
            flash('Credenciales incorrectas', 'error')

    return render_template('index.html')
#----------------Lógica para ingreso de datos de usuario---------------#
#Ruta para guardar usurarios en la base de datos
@app.route("/user",methods=["POST"])
def addUser():
    name = request.form["name"]
    apellido_paterno = request.form["apellido_paterno"]
    apellido_materno = request.form["apellido_materno"]
    telefono = request.form["telefono"]
    cumpleanos = request.form["cumpleanos"]
    correo = request.form["correo"]
    username = request.form["username"]
    password = request.form["password"]

    if username and name and password:
        cursor= db.database.cursor()
        sql = "INSERT INTO users (name, apellido_paterno, apellido_materno, telefono, cumpleanos, correo, username, password ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        data = (name, apellido_paterno, apellido_materno, telefono, cumpleanos, correo, username, password)
        cursor.execute(sql,data)
        db.database.commit()
    return redirect(url_for("home"))

@app.route("/delete/<string:id>")
def delete(id):
    cursor= db.database.cursor()
    sql = "DELETE FROM users WHERE id=%s"
    data = (id,)
    cursor.execute(sql,data)
    db.database.commit()
    return redirect(url_for("home"))

@app.route("/edit/<string:id>", methods=['POST'])
def edit(id):
    name = request.form["name"]
    apellido_paterno = request.form["apellido_paterno"]
    apellido_materno = request.form["apellido_materno"]
    telefono = request.form["telefono"]
    cumpleanos = request.form["cumpleanos"]
    correo = request.form["correo"]
    username = request.form["username"]
    password = request.form["password"]

    if username and name and password:
        cursor= db.database.cursor()
        sql = "UPDATE users SET name=%s, apellido_paterno=%s, apellido_materno=%s, telefono=%s, cumpleanos=%s, correo=%s, username=%s, password=%s WHERE id =%s"
        data = (name, apellido_paterno, apellido_materno, telefono, cumpleanos, correo, username, password,id)
        cursor.execute(sql,data)
        db.database.commit()
    return redirect(url_for("home"))

#--------PUBLICACION LOGICA-------------#
# Ruta para guardar artículos en la base de datos
@app.route("/add_article", methods=["POST"])
def add_article():
    title = request.form["title"]
    content = request.form["content"]
    
    if title and content:
        cursor2 = db.database.cursor()
        sql2  = "INSERT INTO articles (title, content) VALUES (%s, %s)"
        data2 = (title, content)
        cursor2.execute(sql2, data2)
        db.database.commit()
    return redirect(url_for("home"))

# Ruta para eliminar artículos de la base de datos
@app.route("/delete_article/<string:id>")
def delete_article(id):
    cursor2 = db.database.cursor()
    sql2 = "DELETE FROM articles WHERE id=%s"
    data2 = (id,)
    cursor2.execute(sql2, data2)
    db.database.commit()
    return redirect(url_for("home"))

# Ruta para editar artículos en la base de datos
@app.route("/edit_article/<string:id>", methods=['POST'])
def edit_article(id):
    title = request.form["title"]
    content = request.form["content"]
    
    if title and content:
        cursor2 = db.database.cursor()
        sql2 = "UPDATE articles SET title=%s, content=%s WHERE id=%s"
        data2 = (title, content, id)
        cursor2.execute(sql2, data2)
        db.database.commit()
    return redirect(url_for("home"))

#---------SUBIR IMAGEN-----------#
@app.route('/subir', methods=['POST'])
def subir_imagen():
    if request.method == 'POST':
        imagen = request.files['imagen']
        nombre = request.form['nombre']

        if imagen:
            cursor3 = db.database.cursor()
            cursor3.execute("INSERT INTO imagenes (nombre, imagen) VALUES (%s, %s)", (nombre, imagen.read()))
            db.database.commit()
            cursor3.close()
            return redirect(url_for('home'))

@app.route('/mostrar/<int:id>')
def mostrar_imagen(id):
    cursor3 = db.database.cursor()
    cursor3.execute("SELECT nombre, imagen FROM imagenes WHERE id = %s", (id,))
    result = cursor3.fetchone()
    cursor3.close()

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

if __name__ =='__main__':
    app.run(debug=True, port=400)