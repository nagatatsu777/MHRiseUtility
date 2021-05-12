from flask import Flask, session, redirect,render_template, request
import mysql.connector

app =  Flask('app')
app.secret_key = b'xx'

conn = mysql.connector.connect()

@app.route('/')

app.run(host = '0.0.0.0', port = 8080)