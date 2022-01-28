from logging import error
import pyotp #Genera contrase;as de un solo uso?
import sqlite3 #data base para nombres de usuarios y contrase;as
import hashlib #seguridad para hash y resumenes de mensajes. 
import uuid #for para crear identificadores universales unicos de la importacion flask.
from flask import Flask, request

app = Flask(__name__)
db_name = 'test.db'

@app .route('/')
def index():
    return 'Laboratorio practico para una revolucion de los sistemas de contrase;as!'

############################################    Password in text plain 
@app.route('/signup/v1', methods=['POST'])

def signup_v1(): #registro

    conn = sqlite3.connect(db_name)# conexion Con la data base

    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS USER_PLAIN
(USERNAME TEXT PRIMARY KEY NOT NULL,
PASSWORD TEXT NOT NULL);''')
    conn.commit()
    try:
        c.execute("INSERT INTO USER_PLAIN (USERNAME,PASSWORD) " "VALUES ('{0}', '{1}')".format(request.form['username'],request.form['password'])) # Introduccion de datos

        conn.commit()
    except sqlite3.IntegrityError:
        return "username esta registrado."
    print ('username: ', request.form['username'], 'Password: ', request.form['password'])
    return "Registro completado"

def verify_plain (username, password): #verificacion
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    query = "SELECT PASSWORD FROM USER_PLAIN WHERE USERNAME = '{0}'".format(username)
    c.execute (query)
    records = c.fetchone()
    conn.close() #cerrar conexion. 

    if not records:
        return False
    return records[0] == password

@app .route ('/login/v1', methods= ['GET', 'POST'])
def login_v1():
    Noerror = None
    if request.method == 'POST':
        if verify_plain (request.form['username'], request.form['password']):
            Noerror = 'Inicio de Sesion Exitoso'
        else:
            Noerror = 'Usuario o Password invalidos, verifica.'
    else:
        Noerror = 'Solicitud invalidad'
    return Noerror


#################################################   Hash de Contrase;as

@app.route ('/signup/v2', methods= ['GET', 'POST']) #Ruta

def signup_v2():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS USER_HASH
                (USERNAME TEXT PRIMARY KEY NOT NULL,
                HASH TEXT NOT NULL);''')  
    conn.commit()
    try:
        hash_value = hashlib.sha256(request.form['password'].encode()).hexdigest()
        c.execute("INSERT INTO USER_HASH (USERNAME, HASH) " "VALUES ('{0}', '{1}')".format(request.form['username'], hash_value))
        conn.commit()
    except sqlite3.IntegrityError:
        return "username esta registrado v2"
    print ('username: ', request.form['username'], ' password: ', request.form['password'], ' hash: ', hash_value)
    return "Registro Satisfactorio"

def verify_hash(username, password): #Verificacion de password con el hash

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    query = "SELECT HASH FROM USER_HASH WHERE USERNAME = '{0}'".format(username)
    c.execute(query)

    records = c.fetchone()
    conn.close()

    if not records:
        return False
    
    return records[0] == hashlib.sha256(password.encode()).hexdigest()

@app.route('/login/v2', methods=['GET', 'POST'])
def login_v2():
    error = None
    if request.method == 'POST':
        if verify_hash(request.form['username'], request.form['password']):
            error = 'login success'
        else:
            error = 'Invalid username/password'
    else:
        error = 'Invalid Method'
    return error



#Corre la app en el host 0.0.0.0:5000 

if __name__ == '__main__':
    app.run (host='0.0.0.0', port=5000, ssl_context='adhoc')

