from flask import Flask, render_template, request,redirect,url_for, flash
from flask_mail import Mail, Message
import os
import database as db
#Declarar una variables donde estará nuestra carpeta principal  "Prueba flask"
template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
#Unir src y templates a la carpeta de proyectos
template_dir = os.path.join(template_dir, 'src' ,  'templates')

#Una varaibles para inicializar flask  
app = Flask(__name__, template_folder = template_dir)

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
    #Esta es la renderizacion
    return render_template ('registro.html', data=insertObject)
    
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

if __name__ =='__main__':
    app.run(debug=True, port=400)