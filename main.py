from flask import Flask, session, redirect,render_template, request
import mysql.connector

app =  Flask('app')
app.secret_key = b'xx'

conn = mysql.connector.connect(

)

@app.route('/')
def first():
    c = conn.cursor(dictionary = True)
    c.execute('SELECT * FROM Users')
    info = c.fetchall()
    c.close()
    return render_template("index.html",info = info)
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        
    return render_template("dashboard.html")
@app.route('/dashboard',methods = ['POST','GET'])
def dashboard():
    if request.form['submit']=='record':
        c = conn.cursor(dictionary = True)
        c.execute('SELECT questrank FROM Quest GROUP BY questrank ORDER BY questrank;')
        lists = c.fetchall()
        c.close()
        return render_template('ranklist.html', lists = lists)
    return render_template('dashboard.html')
@app.route('/ranklist',methods = ['POST','GET'])
def ranklist():
    c = conn.cursor(dictionary = True)
    c.execute('SELECT questrank FROM Quest GROUP BY questrank ORDER BY questrank;')
    lists = c.fetchall()
    if request.method == "POST":
        rank = int(request.form['submit'])
        c.execute('SELECT * FROM Quest WHERE questrank = %s',(rank,))
        quest = c.fetchall()
        return render_template("questlist.html",quest = quest)
    return render_template('ranklist.html', lists = lists)



        

app.run(host = '0.0.0.0', port = 8080)