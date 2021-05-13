from flask import Flask, session, redirect,render_template, request
import mysql.connector
from datetime import date
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
    if request.method == 'POST':
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
        c.close()
        return render_template("questlist.html",quest = quest)
    c.close()
    return render_template('ranklist.html', lists = lists)

@app.route('/questlist',methods = ['GET','POST'])
def questlist():
    c = conn.cursor(dictionary = True)
    if request.method == 'POST':
        questname = request.form['submit']
        c.execute('SELECT * FROM TimeRecord WHERE questname = %s AND username = %s ORDER BY minute DESC,seconds DESC',(questname,session['username']))
        records = c.fetchall()
        c.close()
        return render_template('record.html',records = records)
    c.close()
    return render_template('questlist.html')
#view record
@app.route('/record', methods = ['POST','GET'])
def record():
    if request.method == 'POST':
        if request.form['submit'] =='create':
            return render_template('recordwe.html')
#for new record creation
@app.route('/recordwe', methods = ['POST','GET'])
def recordwe():
    if request.method == 'POST':
        if request.form['submit'] == 'submit':
            session['weapon'] = request.form['weap']
            return render_template('recordcr.html')
    return render_template('recordwe.html')
@app.route('/recordcr')
def recordcr():
    c = conn.cursor(dictionary = True)
    c.execute('SELECT * FROM ArmorSet WHERE weapon = %s', (session['weapon'],))
    armorlist = c.fetchall()
    if request.method == 'POST':
        return render_template('recordcr.html')
    return render_template('recordcr.html',armorlist = armorlist)


        

app.run(host = '0.0.0.0', port = 8080)