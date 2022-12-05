import sqlite3
from application import app
from flask import render_template, g, request, url_for, redirect, session


@app.route("/")
@app.route("/home")
def home():
    db = get_db()
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute("select * from users;")

    rows = cur.fetchall()
    
    return render_template("home.html", rows=rows,home=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        _conn = get_db()
        username = request.form["username"]
        password = request.form["password"]
        
        if username == 'admin' and password == 'admin':
            #logic for admin interface
            pass
        else:
            if checkUser(username,password):
                sql = "SELECT * from users WHERE u_username = ? and u_password = ?"
                params = [username, password]
                res = executeQuery(sql, params)
                
                return redirect("/home")
            
    return render_template("login.html")

@app.route('/register')
def register():

    return render_template('register.html')

@app.route("/stocks")
def stocks():
    db = get_db()
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute("select * from stocks;")
    stock_rows = cur.fetchall()

    return render_template("stocks.html",stock_rows=stock_rows,stocks=True)

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

def executeQuery(query, params):
	conn = get_db()
	cursor = conn.cursor()
	results = cursor.execute(query, params).fetchall()
	conn.commit()
	conn.close()
	return results

def availableUsername(username):
    # check if username available when registering
    res = executeQuery("select count() from users where u_username = ?", [username])
    return res[0][0] == 0

def insertUser(username, password):
    # function to insert user when registering
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (u_username, u_password) VALUES (?,?)", [username,password])
    conn.commit()
    conn.close()

def checkUser(username, password):
    # validate if user in database
    # username and password must match
    res = executeQuery("SELECT count() from users where u_username = ? AND u_password = ?", [username, password])
    return res[0][0] == 1

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()