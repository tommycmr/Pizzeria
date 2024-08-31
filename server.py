from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

app = Flask(__name__,static_url_path='/static')
load_dotenv()

# Configuración de la conexión MySQL
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios')
    data = cur.fetchall()
    cur.close()  # Es importante cerrar el cursor después de usarlo
    return render_template('home.html')


@app.route('/login')
def vista():
    return render_template('login.html')

@app.route('/register')
def vista2():
    return render_template('register.html')

@app.route('/regis', methods=["POST"])
def registerPost2():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO usuarios (username, email, password) VALUE (%s, %s, %s)', 
                    (username, email, password))
        mysql.connection.commit()
    return redirect("/")

@app.route("/login_post", methods=['POST'])
def loginPost():
    if(request.method == "POST"):
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios')
        data = cur.fetchall()
        for i in data:
            if(i[3] == password and i[1] == username):
                user = i[1]
                return render_template("home.html", usuario = user)
            else :
                redirect("/login")
        cur.close()
    return redirect("/login")

@app.route("/pizzas")
def pizzass():
    return render_template("product.html")

@app.route('/prpizzas', methods=["POST"])
def pizzaPost():
    if request.method == "POST":
        product = request.form['product']
        address = request.form['address']
        mont = request.form['mont']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO productos (product, direccion, mont) VALUE (%s, %s, %s)', (product, address,mont,))
        mysql.connection.commit()
    return redirect("/")


if __name__ == '__main__':
    app.run(port=3000, debug=True)  # Esto hace que los cambios se ejecuten sin necesidad de apagarlo