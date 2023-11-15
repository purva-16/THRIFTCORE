from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import pyodbc

  
app = Flask(__name__,static_folder='static', static_url_path='/static')
app.secret_key = 'xyzsdfg'

conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-IIROG91;DATABASE=online_shopping;')

@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST':
        mobile_no = request.form['mobile_no']
        password = request.form['password']
        print("db connected")
        cursor = conn.cursor()

        print("mobile_no=",mobile_no)
        print("password=",password)

        query = "SELECT * FROM m_user_customer WHERE mobile_no = ?"
        cursor.execute(query, (mobile_no,))
        user = cursor.fetchone()
        print(user)
        if user and user.mobile_no == mobile_no and user.password == password:
            # Successful login
            # You can create a session or set a login flag here
            
            session['loggedin'] = True
            session['mobile_no'] = user.mobile_no
            mesage = 'Logged in successfully !'
            return redirect(url_for('index')) 
        else:
            # Invalid login
            
            mesage = 'Please enter correct mobile_no / password !'
            # return render_template('login.html')
    return render_template('buyerlogin.html',mesage=mesage)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('mobile_no', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'mobile_no' in request.form:
        user_name = request.form['name']
        password = request.form['password']
        mobile_no = request.form['mobile_no']

        cursor = conn.cursor()

        # Check if the mobile_no already exists in the m_user_customer table
        query = "SELECT * FROM m_user_customer WHERE mobile_no = ?"
        cursor.execute(query, (mobile_no,))
        existing_user = cursor.fetchone()

        if existing_user:
            message = 'Account already exists!'
        elif not re.match(r'^[0-9]{10}$', mobile_no):
            message = 'Invalid mobile number!'
        elif not user_name or not password or not mobile_no:
            message = 'Please fill out the form!'
        else:
            # Insert the new user into the m_user_customer table
            insert_query = "INSERT INTO m_user_customer (user_name, mobile_no, password) VALUES (?, ?, ?)"
            cursor.execute(insert_query, (user_name, mobile_no, password))
            conn.commit()
            message = 'You have successfully registered!'
    elif request.method == 'POST':
        message = 'Please fill out the form!'
    return render_template('register.html', message=message)



@app.route('/index')
def index():
    #Add logic to render the index page
    # ...
    return render_template('index.html')

@app.route('/productdetails')
def productdetails(): 
    # Your productdetailsroute logic
    return render_template('productdetails.html')

@app.route('/checkout')
def checkout():
    # Your checkout route logic
    return render_template('checkout.html')

@app.route('/about')
def about():
    # Your checkout route logic
    return render_template('about.html')



@app.route('/cottagecore')
def cottagecore():
    # Your cottagecore route logic
    return render_template('cottagecore.html')

@app.route('/contact')
def contact():
    # Your cottagecore route logic
    return render_template('contact.html')


@app.route('/goth')
def goth():
    # Your goth route logic
    return render_template('goth.html')

@app.route('/vintage')
def vintage():
    # Your vintage route logic
    return render_template('vintage.html')

@app.route('/y2k')
def y2k():
    # Your y2k route logic
    return render_template('y2k.html')

@app.route('/404')
def error404():
    # Your 404 route logic
    return render_template('404.html')

@app.route('/wishlist')
def wishlist():
    # Your wishlist route logic
    return render_template('wishlist.html')

@app.route('/cart')
def cart():
    # Your wishlist route logic
    return render_template('cart.html')

@app.route('/signin')
def signin():
    # Your wishlist route logic
    return render_template('signin.html')

@app.route('/store')
def store():
    # Your wishlist route logic
    return render_template('store.html')

@app.route('/seller')
def seller():
    # Your wishlist route logic
    return render_template('seller.html')

if __name__ == "__main__":
    app.run()
