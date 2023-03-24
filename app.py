from flask import Flask, render_template,redirect,request,session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import registros

Connection = mysql.connector.connect(host='localhost',
                                user='root',
                                password='joahan123',
                                db='eduardo',
                                consume_results=True,
                                )

cursor = Connection.cursor()
app = Flask(__name__)
app.secret_key="pbkdf2:sha256"

@app.route('/')
def index_():
    return redirect('/login.html')

@app.route ('/login.html')
def login():
    return render_template ('login.html')

@app.route ('/register.html')
def register():
    return render_template ('register.html')

@app.route ('/index.html')
def index():
    if session['logeado']==True:  
        return render_template('index.html', username=session['username'])    
    else:    
        return redirect('/login')

@app.route ('/contactanos.html')
def contactanos():
    return render_template('contactanos.html')

@app.route('/especialidades.html')
def especialidades():
    return render_template('especialidades.html')

@app.route ('/citas.html')
def citas():
    citas = registros.obtener_citas()
    return render_template ('citas.html',citas = citas, username=session['username'])

@app.route('/servicios.html')
def servicios():
    return render_template('servicios.html')


#registro y login 
@app.route('/register', methods=['POST'])
def registeruser():
    username = request.form['username']
    password = request.form['password']
    hash_password = generate_password_hash(password)
    Query = f"INSERT INTO usuarios(username, password) VALUES (%s, %s)"
    cursor.execute(Query,(username, hash_password))
    Connection.commit()
    cursor.reset()
    return redirect("/login")

@app.route('/login', methods=['GET','POST'])
def loginuser():
    msg=''
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT username, password FROM usuarios WHERE username=%s",(username,))
        record = cursor.fetchone() 
        if record: 
            hash_password = record[1] 
            if check_password_hash(hash_password, password): 
                session['logeado']=True 
                session['username']= record[0]  
                return redirect("/index.html") 
            else: #Contraseña incorrecta 
                msg='no se encontró el usuario o contraseña incorrecto'  
        else: #No existe el usuario en la base de datos 
            msg='no se encontró el usuario o contraseña incorrecto'  
    return render_template('login.html', msg=msg)

#CRUD
@app.route('/guardar_citas', methods=['POST'])
def guardar_citas():
    nombre = request.form['nombre']
    apellido_paterno = request.form['apellido_paterno']
    apellido_materno = request.form['apellido_materno']
    email = request.form['email']
    tipo_sangre = request.form['tipo_sangre']
    numero = request.form['numero']
    direccion = request.form['direccion']
    registros.insertar_citas(nombre, apellido_paterno ,apellido_materno, email, tipo_sangre, numero, direccion)
    return redirect('citas.html')

@app.route('/eliminar_cita', methods=['POST'])
def eliminar_cita():
    registros.eliminar_cita(request.form['id'])
    return redirect ('citas.html')


@app.route("/formulario_editar_cita/<int:id>")
def editar_cita(id):
    cita = registros.obtener_citas_por_id(id)
    return render_template("editar_cita.html", cita=cita)

@app.route("/actualizar_cita", methods=["POST"])
def actualizar_cita():
    id = request.form['id']
    nombre = request.form['nombre']
    apellido_paterno = request.form['apellido_paterno']
    apellido_materno = request.form['apellido_materno']
    email = request.form['email']
    tipo_sangre = request.form['tipo_sangre']
    numero = request.form['numero']
    direccion = request.form['direccion']
    registros.actualizar_cita(nombre, apellido_paterno ,apellido_materno, email, tipo_sangre, numero, direccion, id)
    return redirect("/citas.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)