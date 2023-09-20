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
    #Esta es la renderizacion
    return render_template ('publicacion.html', data2=insertObject2)

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
        
if __name__ =='__main__':
    app.run(debug=True, port=4000)  