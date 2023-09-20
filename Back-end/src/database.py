#pip install mysql-connector-python==8.0.29
import mysql.connector

database=  mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234',
    database= 'ordinario'   
)