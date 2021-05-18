from flask import Flask, session, redirect, render_template, request
import mysql.connector
from datetime import date
app = Flask('app')
app.secret_key = b'xx'

conn = mysql.connector.connect(

)


@app.route('/')
def first():
    c = conn.cursor(dictionary=True)
    c.execute('SELECT * FROM Users')
    info = c.fetchall()
    c.close()
    return render_template("index.html", info=info)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        c = conn.cursor(buffered=True)
        c.execute('SELECT userrole FROM Users WHERE username = %s',
                  (session['username'],))
        session['userrole'] = c.fetchone()[0]
        print(session['userrole'])
    return render_template("dashboard.html")


@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if request.method == 'POST':
        if request.form['submit'] == 'record':
            c = conn.cursor(dictionary=True)
            c.execute(
                'SELECT questrank FROM Quest GROUP BY questrank ORDER BY questrank;')
            lists = c.fetchall()
            c.close()
            return render_template('ranklist.html', lists=lists)
        if request.form['submit'] == 'export':
            c = conn.cursor(dictionary=True)
            c.execute('SELECT Quest.questname, Quest.monster, W.weap,W.minute,W.sec FROM Quest INNER JOIN(SELECT TimeRecord.questname as qn,TimeRecord.weapon as weap,min(TimeRecord.minute) as minute ,min(TimeRecord.seconds) as sec FROM TimeRecord INNER JOIN(SELECT questname,weapon,min(minute) as ma FROM TimeRecord GROUP BY questname,weapon) AS S ON S.questname = TimeRecord.questname AND S.weapon = TimeRecord.weapon AND S.ma = TimeRecord.minute GROUP BY TimeRecord.questname, TimeRecord.weapon) AS W ON Quest.questname = W.qn;')
            records = c.fetchall()
            c.close()
            return render_template('viewrecord.html', records=records)
    return render_template('dashboard.html')


@app.route('/ranklist', methods=['POST', 'GET'])
def ranklist():
    c = conn.cursor(dictionary=True)
    c.execute('SELECT questrank FROM Quest GROUP BY questrank ORDER BY questrank')
    lists = c.fetchall()
    if request.method == "POST":
        rank = int(request.form['submit'])
        c.execute('SELECT * FROM Quest WHERE questrank = %s', (rank,))
        quest = c.fetchall()
        c.close()
        return render_template("questlist.html", quest=quest)
    c.close()
    return render_template('ranklist.html', lists=lists)


@app.route('/questlist', methods=['GET', 'POST'])
def questlist():
    if request.method == 'POST':
        session['questname'] = request.form['submit']
        c = conn.cursor(dictionary=True)
        c.execute('SELECT * FROM TimeRecord WHERE questname = %s AND username = %s ORDER BY minute DESC,seconds DESC',
                  (session['questname'], session['username']))
        records = c.fetchall()
        c.close()
        return render_template('record.html', records=records)

    return render_template('questlist.html')
# view record


@app.route('/record', methods=['POST', 'GET'])
def record():
    c = conn.cursor(dictionary=True)
    c.execute('SELECT * FROM TimeRecord WHERE questname = %s AND username = %s ORDER BY minute DESC,seconds DESC',
              (session['questname'], session['username']))
    records = c.fetchall()
    if request.method == 'POST':
        if request.form['submit'] == 'create':
            c.close()
            return render_template('recordwe.html')
        if request.form['submit'] == 'prev':
            c.execute('SELECT questrank FROM Quest WHERE questname = %s',
                      (session['questname'],))
            querank = c.fetchone()['questrank']
            c.execute('SELECT * FROM Quest WHERE questrank = %s', (querank,))
            quest = c.fetchall()
            c.close()
            return render_template('questlist.html', quest=quest)
    return render_template('record.html', records=records)
# for new record creation


@app.route('/recordwe', methods=['POST', 'GET'])
def recordwe():
    if request.method == 'POST':
        c = conn.cursor(dictionary=True, buffered=True)
        if request.form['submit'] == 'submit':
            session['weapon'] = request.form['weap']
            c.execute('SELECT * FROM ArmorSet WHERE weapon = %s',
                      (session['weapon'],))
            armorlist = c.fetchall()
            c.close()
            return render_template('recordcr.html', armorlist=armorlist)
        if request.form['submit'] == 'prev':
            c.execute('SELECT * FROM TimeRecord WHERE questname = %s AND username = %s ORDER BY minute DESC,seconds DESC',
                      (session['questname'], session['username']))
            records = c.fetchall()
            c.close()
            return render_template('record.html', records=records)
    return render_template('recordwe.html')


@app.route('/recordcr', methods=['POST', 'GET'])
def recordcr():
    c = conn.cursor(dictionary=True, buffered=True)
    c.execute('SELECT * FROM ArmorSet WHERE weapon = %s', (session['weapon'],))
    armorlist = c.fetchall()
    if request.method == 'POST':
        if request.form['submit'] == 'prev':
            return redirect('/recordwe')
        if request.form['submit'] == 'submit':
            weaponname = request.form['weaponname']
            helm = request.form['helm']
            chest = request.form['chest']
            arm = request.form['arm']
            waist = request.form['waist']
            leg = request.form['leg']
            deco = request.form['deco']
            minute = (int)(request.form['minute'])
            seconds = (int)(request.form['seconds'])
            today = date.today()
            c.execute('SELECT * FROM ArmorSet WHERE weaponname = %s AND helm = %s AND chest = %s AND arm = %s AND waist = %s AND leg = %s AND deco = %s',
                      (weaponname, helm, chest, arm, waist, leg, deco))
            result = c.fetchall()
            if result == []:
                c.execute('INSERT INTO ArmorSet(weapon,weaponname,helm,chest,arm,waist,leg,deco) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
                          (session['weapon'], weaponname, helm, chest, arm, waist, leg, deco))
                conn.commit()
            c.execute('SELECT id FROM ArmorSet WHERE weaponname = %s AND helm = %s AND chest = %s AND arm = %s AND waist = %s AND leg = %s AND deco = %s',
                      (weaponname, helm, chest, arm, waist, leg, deco))
            armorid = c.fetchone()['id']
            c.execute('SELECT * FROM TimeRecord WHERE questname = %s AND weapon = %s AND username = %s AND armorid = %s',
                      (session['questname'], session['weapon'], session['username'], armorid))
            res = c.fetchall()
            if res == []:
                c.execute('INSERT INTO TimeRecord(questname,weapon,minute,seconds,uploaddate,username,armorid) VALUES (%s,%s,%s,%s,%s,%s,%s)',
                          (session['questname'], session['weapon'], minute, seconds, today, session['username'], armorid))
                conn.commit()
            else:
                c.execute('UPDATE TimeRecord SET minute = %s, seconds = %s, uploaddate = %s WHERE questname = %s AND weapon = %s AND username = %s AND armorid = %s',
                          (minute, seconds, today, session['questname'], session['weapon'], session['username'], armorid))

            return redirect('/record')
    return render_template('recordcr.html', armorlist=armorlist)


@app.route('/viewrecord', methods=['POST', 'GET'])
def viewre():
    c = conn.cursor(dictionary=True)
    c.execute('SELECT Quest.questname, Quest.monster, W.weap,W.minute,W.sec FROM Quest INNER JOIN(SELECT TimeRecord.questname as qn,TimeRecord.weapon as weap,min(TimeRecord.minute) as minute ,min(TimeRecord.seconds) as sec FROM TimeRecord INNER JOIN(SELECT questname,weapon,min(minute) as ma FROM TimeRecord GROUP BY questname,weapon) AS S ON S.questname = TimeRecord.questname AND S.weapon = TimeRecord.weapon AND S.ma = TimeRecord.minute GROUP BY TimeRecord.questname, TimeRecord.weapon) AS W ON Quest.questname = W.qn;')
    records = c.fetchall()
    c.close()
    if request.method == 'POST':
        if request.form['submit'] == 'prev':
            return render_template('dashboard.html')
    return render_template('viewrecord.html', records=records)


app.run(host='0.0.0.0', port=8080)
