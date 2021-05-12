from flask import Flask, session, redirect,render_template, request
import mysql.connector

app =  Flask('app')
app.secret_key = b'xx'

conn = mysql.connector.connect()

@app.route('/')
def first():
    return render_template("index.html")
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
    return render_template("dashboard.html")
@app.route('/dashboard',methods = ['POST','GET'])
def dashboard():
    return render_template('dashboard.html')
        

app.run(host = '0.0.0.0', port = 8080)