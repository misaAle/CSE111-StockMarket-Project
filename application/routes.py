import sqlite3
from application import app
from flask import render_template, g, request, url_for, redirect

@app.route("/")
@app.route("/home")
def home():
    db = get_db()
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute("select * from users")

    rows = cur.fetchall()
    
    return render_template("home.html", rows=rows,home=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            #logic for admin interface
            pass
        
    return render_template("login.html")

@app.route("/stocks")
def stocks():
    return render_template("home.html",stocks=True)

@app.route("/portfolio")
def portfolio():
    return render_template("home.html",portfolio=True)

@app.route("/watchlist")
def watchlist():
    return render_template("home.html",watchlist=True)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('main.sqlite')
    
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()