import matplotlib.pyplot as plt
from flask import Flask, session, redirect, render_template, request
import mysql.connector
from datetime import date
import matplotlib
from dotenv import load_dotenv, find_dotenv
import os
matplotlib.use('Agg')
app = Flask(__name__)
app.secret_key = b'xx'
UPLOAD_FOLDER = "/Users/Lan/Desktop/MHRiseUtility/static/"
# save path
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
load_dotenv(find_dotenv())
# graph color dictionary
colorDict = {
    "大剣": "#FF8F8F",
    "太刀": "#93FF33",
    "片手剣": "#D3D096",
    "双剣": "#FFFA98",
    "ランス": "#FEC1B3",
    "ガンランス": "#FFFE4C",
    "ハンマー": "#BEBFB5",
    "狩猟笛": "#FCCE38",
    "操虫棍": "#C1856F",
    "チャージアックス": "BROWN",
    "スラッシュアックス": "PINK",
    "ライトボウガン": "#C9C7FF",
    "ヘビィボウガン": "#B0F7FF",
    "弓": "#FFF460"
}
conn = mysql.connector.connect(
    user=os.getenv("USERD"),
    password=os.getenv("PASSWORDD"),
    database=os.getenv("DATABASED"),
    auth_plugin='mysql_native_password'
)


@app.route('/')
def first():
    c = conn.cursor(dictionary=True)
    c.execute('SELECT * FROM Users')
    info = c.fetchall()
    session['language'] = 'Japanese'
    c.close()
    return render_template("index.html", info=info)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # For changing language
        if request.form['submit'] == 'change':
            c = conn.cursor(dictionary=True)
            c.execute('SELECT * FROM Users')
            info = c.fetchall()
            c.close()
            if session['language'] == 'Japanese':
                session['language'] = 'English'
            else:
                session['language'] = 'Japanese'
            return render_template("index.html", info=info)
        if request.form['submit'] == 'submit':
            session['username'] = request.form['username']
            session['password'] = request.form['password']
            c = conn.cursor(buffered=True)
            c.execute('SELECT userrole FROM Users WHERE username = %s',
                      (session['username'],))
            session['userrole'] = c.fetchone()[0]
            print(session['userrole'])
        return render_template("dashboard.html")
    return render_template("index.html")

# Route for the registration page


@app.route('/register', methods=['POST', 'GET'])
def register():
    c = conn.cursor(dictionary=True)
    c.execute('SELECT username FROM Users')
    # pass username data for the validation
    usernames = c.fetchall()
    if request.method == 'POST':
        if request.form['submit'] == 'submit':
            username = request.form['username']
            password = request.form['password']
            session['username'] = username
            c.execute('INSERT INTO Users(username, pass, userrole) VALUES(%s,%s,%s);',
                      (username, password, 'user'))
            conn.commit()
            c.close()
            return render_template('dashboard.html')
    c.close()
    return render_template('register.html', usernames=usernames)


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
            c.execute(
                'SELECT Quest.questname, Quest.monster, W.weap,W.minute,W.sec FROM Quest INNER JOIN(SELECT TimeRecord.questname as qn,TimeRecord.weapon as weap,min(TimeRecord.minute) as minute ,min(TimeRecord.seconds) as sec FROM TimeRecord INNER JOIN(SELECT questname,weapon,min(minute) as ma FROM TimeRecord GROUP BY questname,weapon) AS S ON S.questname = TimeRecord.questname AND S.weapon = TimeRecord.weapon AND S.ma = TimeRecord.minute GROUP BY TimeRecord.questname, TimeRecord.weapon ORDER BY minute ASC, sec ASC) AS W ON Quest.questname = W.qn;')
            records = c.fetchall()
            # Window function example
            c.execute(
                'SELECT Quest.questname, Quest.monster, W.weap,W.minute,W.seconds FROM Quest INNER JOIN (SELECT distinct weapon as weap ,questname,minute,seconds, COUNT(weapon) OVER(PARTITION BY weapon,questname ORDER BY minute, seconds) as countrank FROM TimeRecord WHERE username = %s) as W ON Quest.questname = W.questname WHERE W.countrank = 1;', (session['username'],))
            weaprecords = c.fetchall()
            # Records by the questname
            c.execute(
                'SELECT Quest.questname, Quest.monster, W.weap,W.minute,W.seconds, Quest.questrank FROM Quest INNER JOIN (SELECT distinct weapon as weap ,questname,minute,seconds, COUNT(weapon) OVER(PARTITION BY questname,weapon ORDER BY minute, seconds) as countrank FROM TimeRecord WHERE username = %s) as W ON Quest.questname = W.questname WHERE W.countrank = 1 ORDER BY Quest.questrank;', (session['username'],))
            questrecords = c.fetchall()
            # Make the pie chart of the ratio of weapons ranking the top
            c.execute('SELECT W.weap as we, COUNT(W.weap) as toprank FROM TimeRecord INNER JOIN (SELECT distinct weapon as weap ,questname,minute,seconds, COUNT(weapon) OVER(PARTITION BY questname ORDER BY minute, seconds) as countrank FROM TimeRecord) as W ON W.questname = TimeRecord.questname AND TimeRecord.weapon = W.weap WHERE W.countrank = 1 GROUP BY W.weap ORDER BY toprank;')
            data = []
            label = []
            colors = []
            explode = []
            graphrecords = c.fetchall()
            for s in graphrecords:
                data.append(s['toprank'])
                label.append(
                    s['we']+': TopTotal( ' + str(s['toprank'])+' )')
                colors.append(colorDict[s['we']])
                explode.append(0)
            explode.remove(0)
            explode.append(0.1)
            plt.pie(data, labels=label, shadow=True,
                    colors=colors, explode=explode)
            plt.savefig(app.config['UPLOAD_FOLDER'] +
                        session['username']+'piechart1', bbox_inches='tight')
            plt.close()
            # Make the pie chart of the ratio of weapons ranking the second
            c.execute('SELECT W.weap as we, COUNT(W.weap) as toprank FROM TimeRecord INNER JOIN (SELECT distinct weapon as weap ,questname,minute,seconds, COUNT(weapon) OVER(PARTITION BY questname ORDER BY minute, seconds) as countrank FROM TimeRecord) as W ON W.questname = TimeRecord.questname AND TimeRecord.weapon = W.weap WHERE W.countrank = 2 GROUP BY W.weap ORDER BY toprank;')
            data = []
            label = []
            colors = []
            explode = []
            graphrecords = c.fetchall()
            for s in graphrecords:
                data.append(s['toprank'])
                label.append(
                    s['we']+': Total( ' + str(s['toprank'])+' )')
                colors.append(colorDict[s['we']])
                explode.append(0)
            explode.remove(0)
            explode.append(0.1)
            plt.pie(data, labels=label, shadow=True,
                    colors=colors, explode=explode)
            plt.savefig(app.config['UPLOAD_FOLDER'] +
                        session['username']+'piechart2', bbox_inches='tight')
            plt.close()
            # Make the pie chart of the ratio of weapons ranking the third
            c.execute('SELECT W.weap as we, COUNT(W.weap) as toprank FROM TimeRecord INNER JOIN (SELECT distinct weapon as weap ,questname,minute,seconds, COUNT(weapon) OVER(PARTITION BY questname ORDER BY minute, seconds) as countrank FROM TimeRecord) as W ON W.questname = TimeRecord.questname AND TimeRecord.weapon = W.weap WHERE W.countrank = 3 GROUP BY W.weap ORDER BY toprank;')
            data = []
            label = []
            colors = []
            explode = []
            graphrecords = c.fetchall()
            for s in graphrecords:
                data.append(s['toprank'])
                label.append(
                    s['we']+': Total( ' + str(s['toprank'])+' )')
                colors.append(colorDict[s['we']])
                explode.append(0)
            explode.remove(0)
            explode.append(0.1)
            plt.pie(data, labels=label, shadow=True,
                    colors=colors, explode=explode)
            plt.savefig(app.config['UPLOAD_FOLDER'] +
                        session['username']+'piechart3', bbox_inches='tight')
            plt.close()
            # Make the pie chart of the ratio of weapons ranking the last
            c.execute('SELECT W.weap as we, COUNT(W.weap) as toprank FROM TimeRecord INNER JOIN (SELECT distinct weapon as weap ,questname,minute,seconds, COUNT(weapon) OVER(PARTITION BY questname ORDER BY minute, seconds) as countrank FROM TimeRecord) as W ON W.questname = TimeRecord.questname AND TimeRecord.weapon = W.weap WHERE W.countrank = 14 GROUP BY W.weap ORDER BY toprank;')
            data = []
            label = []
            colors = []
            explode = []
            graphrecords = c.fetchall()
            for s in graphrecords:
                data.append(s['toprank'])
                label.append(
                    s['we']+': Total( ' + str(s['toprank'])+' )')
                colors.append(colorDict[s['we']])
                explode.append(0)
            explode.remove(0)
            explode.append(0.1)
            plt.pie(data, labels=label, shadow=True,
                    colors=colors, explode=explode)
            plt.savefig(app.config['UPLOAD_FOLDER'] +
                        session['username']+'piechart14', bbox_inches='tight')
            plt.close()
            # Make the bar graph of the average time of each weapon
            c.execute('SELECT W.weap, AVG(W.minute*60+W.seconds) as average FROM TimeRecord INNER JOIN (SELECT distinct weapon as weap ,questname,minute,seconds, COUNT(weapon) OVER(PARTITION BY questname ORDER BY minute, seconds) as countrank FROM TimeRecord) as W ON W.questname = TimeRecord.questname AND TimeRecord.weapon = W.weap GROUP BY W.weap ORDER BY average;')
            avgrecords = c.fetchall()
            avgdata = []
            label = []
            colors = []
            x = []
            i = 0
            for a in avgrecords:
                i += 1
                avgdata.append(a['average'])
                label.append(a['weap'])
                x.append(i)
                colors.append(colorDict[a['weap']])
            plt.bar(x, avgdata, tick_label=label,
                    width=0.8, color=colors)
            plt.xlabel('武器')
            plt.ylabel('タイム　（秒）')
            plt.title('平均記録表')
            plt.xticks(rotation=270, fontsize=7)
            plt.savefig(app.config['UPLOAD_FOLDER'] +
                        session['username']+'average')
            plt.close()
            c.close()
            return render_template('viewrecord.html', records=records, weaprecords=weaprecords, questrecords=questrecords)
        if request.form['submit'] == 'addque':
            return render_template('addquest.html')
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
        c.execute('SELECT * FROM TimeRecord WHERE questname = %s AND username = %s ORDER BY minute ASC,seconds ASC',
                  (session['questname'], session['username']))
        records = c.fetchall()
        c.execute('SELECT Quest.questname, Quest.monster, W.weap,W.minute,W.sec FROM Quest INNER JOIN(SELECT TimeRecord.questname as qn,TimeRecord.weapon as weap,min(TimeRecord.minute) as minute ,min(TimeRecord.seconds) as sec FROM TimeRecord INNER JOIN(SELECT questname,weapon,min(minute) as ma FROM TimeRecord GROUP BY questname,weapon) AS S ON S.questname = TimeRecord.questname AND S.weapon = TimeRecord.weapon AND S.ma = TimeRecord.minute GROUP BY TimeRecord.questname, TimeRecord.weapon) AS W ON Quest.questname = W.qn WHERE Quest.questname= %s ORDER BY W.minute ASC, W.sec ASC  LIMIT 1;',
                  (session['questname'],))
        fastest = c.fetchone()
        c.execute('SELECT TimeRecord.weapon as weap,min(TimeRecord.minute) as minute ,min(TimeRecord.seconds) as sec FROM TimeRecord INNER JOIN(SELECT questname,weapon,min(minute) as ma FROM TimeRecord GROUP BY questname,weapon) AS S ON S.questname = TimeRecord.questname AND S.weapon = TimeRecord.weapon AND S.ma = TimeRecord.minute GROUP BY TimeRecord.questname, TimeRecord.weapon HAVING questname = %s ORDER BY minute, sec;',
                  (session['questname'],))
        x = []
        tick_label = []
        y = []
        i = 0
        colors = []
        graphrecords = c.fetchall()
        for s in graphrecords:
            i += 1
            x.append(i)
            tick_label.append(s['weap'])
            y.append(s['minute']*60+s['sec'])
            colors.append(colorDict[s['weap']])
        plt.bar(x, y, tick_label=tick_label, width=0.8, color=colors)
        plt.xlabel('武器')
        plt.ylabel('タイム　（秒）')
        plt.title('記録表')
        plt.xticks(rotation=270, fontsize=7)
        plt.savefig(app.config['UPLOAD_FOLDER']+session['questname'])
        plt.close()
        c.close()
        return render_template('record.html', records=records, fastest=fastest)

    return render_template('dashboard.html')
# view record


@app.route('/record', methods=['POST', 'GET'])
def record():
    c = conn.cursor(dictionary=True)
    c.execute('SELECT * FROM TimeRecord WHERE questname = %s AND username = %s ORDER BY minute DESC,seconds DESC',
              (session['questname'], session['username']))
    records = c.fetchall()
    c.execute('SELECT Quest.monster, W.weap,W.minute,W.sec FROM Quest INNER JOIN(SELECT TimeRecord.questname as qn,TimeRecord.weapon as weap,min(TimeRecord.minute) as minute ,min(TimeRecord.seconds) as sec FROM TimeRecord INNER JOIN(SELECT questname,weapon,min(minute) as ma FROM TimeRecord GROUP BY questname,weapon) AS S ON S.questname = TimeRecord.questname AND S.weapon = TimeRecord.weapon AND S.ma = TimeRecord.minute GROUP BY TimeRecord.questname, TimeRecord.weapon) AS W ON Quest.questname = W.qn WHERE Quest.questname= %s ORDER BY W.minute ASC, W.sec ASC  LIMIT 1;',
              (session['questname'],))
    fastest = c.fetchone()
    c.execute('SELECT TimeRecord.weapon as weap,min(TimeRecord.minute) as minute ,min(TimeRecord.seconds) as sec FROM TimeRecord INNER JOIN(SELECT questname,weapon,min(minute) as ma FROM TimeRecord GROUP BY questname,weapon) AS S ON S.questname = TimeRecord.questname AND S.weapon = TimeRecord.weapon AND S.ma = TimeRecord.minute GROUP BY TimeRecord.questname, TimeRecord.weapon HAVING questname = %s ORDER BY minute, sec;',
              (session['questname'],))
    x = []
    tick_label = []
    y = []
    i = 0
    colors = []
    graphrecords = c.fetchall()
    for s in graphrecords:
        i += 1
        x.append(i)
        tick_label.append(s['weap'])
        y.append(s['minute']*60+s['sec'])
        colors.append(colorDict[s['weap']])
    plt.bar(x, y, tick_label=tick_label, width=0.8, color=colors)
    plt.xlabel('武器')
    plt.ylabel('タイム　（秒）')
    plt.title('記録表')
    plt.xticks(rotation=270, fontsize=7)
    plt.savefig(app.config['UPLOAD_FOLDER']+session['questname'])
    plt.close()
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
        id = (int)(request.form['submit'])
        c.execute('SELECT * FROM ArmorSet WHERE id = %s', (id,))
        armor = c.fetchone()
        c.close()
        return render_template('armorset.html', armor=armor)
    c.close()
    return render_template('record.html', records=records, fastest=fastest)
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
            print(session['username'])
            c.execute('SELECT Quest.monster, W.weap,W.minute,W.sec FROM Quest INNER JOIN(SELECT TimeRecord.questname as qn,TimeRecord.weapon as weap,min(TimeRecord.minute) as minute ,min(TimeRecord.seconds) as sec FROM TimeRecord INNER JOIN(SELECT questname,weapon,min(minute) as ma FROM TimeRecord GROUP BY questname,weapon) AS S ON S.questname = TimeRecord.questname AND S.weapon = TimeRecord.weapon AND S.ma = TimeRecord.minute GROUP BY TimeRecord.questname, TimeRecord.weapon) AS W ON Quest.questname = W.qn WHERE Quest.questname= %s ORDER BY W.minute ASC, W.sec ASC  LIMIT 1;',
                      (session['questname'],))
            fastest = c.fetchone()
            c.close()
            return render_template('record.html', records=records, fastest=fastest)
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
    c.execute('SELECT Quest.questname, Quest.monster, W.weap,W.minute,W.seconds FROM Quest INNER JOIN (SELECT distinct weapon as weap ,questname,minute,seconds, COUNT(weapon) OVER(PARTITION BY weapon,questname ORDER BY minute, seconds) as countrank FROM TimeRecord) as W ON Quest.questname = W.questname WHERE W.countrank = 1;')
    weaprecords = c.fetchall()
    c.execute('SELECT Quest.questname, Quest.monster, W.weap,W.minute,W.seconds, Quest.questrank FROM Quest INNER JOIN (SELECT distinct weapon as weap ,questname,minute,seconds, COUNT(weapon) OVER(PARTITION BY questname,weapon ORDER BY minute, seconds) as countrank FROM TimeRecord) as W ON Quest.questname = W.questname WHERE W.countrank = 1 ORDER BY Quest.questrank;')
    questrecords = c.fetchall()
    c.close()
    if request.method == 'POST':
        if request.form['submit'] == 'prev':
            return render_template('dashboard.html')
    return render_template('viewrecord.html', records=records, weaprecords=weaprecords, questrecords=questrecords)


@app.route('/armorset', methods=['POST', 'GET'])
def armorset():

    if request.method == 'POST':
        if request.form['submit'] == 'prev':
            c = conn.cursor(dictionary=True)
            c.execute('SELECT * FROM TimeRecord WHERE questname = %s AND username = %s ORDER BY minute DESC,seconds DESC',
                      (session['questname'], session['username']))
            records = c.fetchall()
            c.execute('SELECT Quest.monster, W.weap,W.minute,W.sec FROM Quest INNER JOIN(SELECT TimeRecord.questname as qn,TimeRecord.weapon as weap,min(TimeRecord.minute) as minute ,min(TimeRecord.seconds) as sec FROM TimeRecord INNER JOIN(SELECT questname,weapon,min(minute) as ma FROM TimeRecord GROUP BY questname,weapon) AS S ON S.questname = TimeRecord.questname AND S.weapon = TimeRecord.weapon AND S.ma = TimeRecord.minute GROUP BY TimeRecord.questname, TimeRecord.weapon) AS W ON Quest.questname = W.qn WHERE Quest.questname= %s ORDER BY W.minute ASC, W.sec ASC  LIMIT 1;',
                      (session['questname'],))
            fastest = c.fetchone()
            c.close()
            return render_template('record.html', records=records, fastest=fastest)


@app.route('/addquest', methods=['POST', 'GET'])
def addque():
    if request.method == 'POST':
        if request.form['submit'] == 'submit':
            questname = request.form['questname']
            questmonster = request.form['questmonster']
            questrank = request.form['questrank']
            c = conn.cursor()
            c.execute('INSERT INTO Quest(questname,monster,questrank) VALUES (%s,%s,%s)',
                      (questname, questmonster, questrank))
            conn.commit()
            c.close()
            return redirect('/dashboard')
    return render_template('addquest.html')
# Route which allows the page to change its language setting


@app.route('/change', methods=['POST', 'GET'])
def changeLanguage():
    if session['language'] == 'Japanese':
        session['language'] = 'English'
    else:
        session['language'] = 'Japanese'
    return render_template('dashboard.html')


#app.run(host='0.0.0.0', port=8080)
if __name__ == '__main__':
    app.run()
