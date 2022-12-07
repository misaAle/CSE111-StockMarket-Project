import sqlite3
from application import app
from flask import render_template, g, request, url_for, redirect, session, flash
from application.forms import LoginForm, RegisterForm
from application import db


@app.route("/")
@app.route("/home")
def home():
    conn = db
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute("select * from users;")

    rows = cur.fetchall()
    
    return render_template("home.html", rows=rows,home=True)

@app.route("/logout")
def logout():
    session['user_id']=False
    session.pop('username',None)
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('username'):
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if checkUser(username, password):
            if username == 'admin' and password == 'admin1234':
                session['username'] = 'admin'
                return redirect('/admin')
            
            flash(f"{username}, you are successfully logged in!", "success")
            res = executeQuery("SELECT u_userid FROM users WHERE u_username = ?", [username])
            session['user_id'] = res[0][0]
            session['username'] = username
            return redirect('/home')
        else:
            flash("Sorry, either the username or password didn't match any records.", "danger")
            pass
        # conn = db
        # cur = conn.cursor()
        # sql = "SELECT 1, * FROM users WHERE u_username = ?"
        # res = executeQuery(sql, [username])
        # print('######',res)
        # if len(res) != 0 and res[0][0] == 1:
        #     password_sql = "SELECT u_password FROM users where u_username = ?"
        #     password_res = executeQuery(password_sql, [res[0][2]])
        #     print('*****',password_res)
        #     if password == password_res[0][0]:
        #         flash(f"{res[0][2]}, you are successfully logged in!", "success")
        #         session['user_id'] = res[0][1]
        #         session['username'] = res[0][2]
        #         return redirect("/home")
        #     else:
        #         flash("Sorry, the password entered didn't match any records.", "danger")
        # else:
        #     flash("Sorry, either the username or password didn't match any records.", "danger")
    
    # if request.method == 'POST':
    #     _conn = get_db()
    #     username = request.form["username"]
    #     password = request.form["password"]
        
    #     if username == 'admin' and password == 'admin':
    #         #logic for admin interface
    #         pass
    #     else:
    #         if checkUser(username,password):
    #             sql = "SELECT * from users WHERE u_username = ? and u_password = ?"
    #             params = [username, password]
    #             res = executeQuery(sql, params)
                
    #             return redirect("/home")
            
    return render_template("login.html", form=form, login=True)

@app.route('/register', methods=['POST','GET'])
def register():
    if session.get('username'):
        return redirect('/home')
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        print("@@@@@@@",username, password)
        confirm_password = form.confirm_password.data
        if password == confirm_password:
            flash(f"{username}, you are successfully registered!", "success")
            sql ="""INSERT INTO users (u_username,u_password,u_acctbal) 
                    VALUES
                        (?,?,0);"""
            params = [username, password]
            res = executeQuery(sql, params)
            return redirect('/login')
        else:
            flash("Passwords did not match", "danger")
            
        # if checkUser(username, password):
        #     flash(f"{username}, you are successfully logged in!", "success")
        #     res = executeQuery("SELECT u_userid FROM users WHERE u_username = ?", [username])
        #     session['user_id'] = res[0][0]
        #     session['username'] = username
        #     return redirect('/home')
        # else:
        #     flash("Sorry, either the username or password didn't match any records.", "danger")
            
    return render_template('register.html', form=form,register=True)

@app.route("/stocks", methods=['POST', 'GET'])
def stocks():
    
    if request.method == 'POST':
        if request.form.get('watchlist-submission') == 'Add to Watchlist':
            print('Submitted')
            ticker = request.form.get("ticker")
            print(ticker)
            sql = """INSERT INTO watchlist
                VALUES
                    (?, ?)"""
            params = [session['user_id'], ticker ]
            res = executeQuery(sql, params)
            return redirect('/watchlist')
        
    conn = db
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute("select * from stocks;")
    stock_rows = cur.fetchall()

    return render_template("stocks.html",stock_rows=stock_rows,stocks=True)

@app.route("/portfolio")
def portfolio():
    
    if session.get('username'):
        conn = db
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.execute("""SELECT p_ticker, p_quantity FROM portfolio, users
WHERE u_userid = p_userid
AND u_userid = ?;""", [session['user_id']])
        portfolio_rows = cur.fetchall()
        return render_template("portfolio.html", portfolio_rows=portfolio_rows, portfolio=True)
    return render_template("portfolio.html",portfolio=True)

@app.route("/watchlist")
def watchlist():
    if session.get('username'):
        conn = db
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.execute("""SELECT w_ticker FROM watchlist, users
WHERE u_userid = w_userid
AND u_userid = ?;""", [session['user_id']])
        watchlist_rows = cur.fetchall()
        return render_template("watchlist.html", watchlist_rows=watchlist_rows, watchlist=True)
    return render_template("watchlist.html",watchlist=True)

@app.route('/admin')
def admin():
    if session.get('username') != 'admin':
        return redirect('/home')
    return render_template('admin.html', admin=True)

@app.route('/transactions')
def transactions():
    if session.get('username') != 'admin':
        return redirect('/home')
    conn = db
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute("SELECT * FROM orders;")
    transaction_rows = cur.fetchall()
    return render_template('transactions.html', transaction_rows=transaction_rows, transactions=True)

@app.route('/users')
def users():
    if session.get('username') != 'admin':
        return redirect('/home')
    conn = db
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute("SELECT * FROM users;")
    user_rows = cur.fetchall()
    return render_template('users.html', user_rows=user_rows, users=True)


# @app.route('/button', methods=['GET', 'POST'])
# def button():
#     if request.method == 'POST':
#         sql = """INSERT INTO users (u_username, u_password, u_acctbal)
#             VALUES
#                 ('another_test', ?, 0);"""
#         var = 'asdfghjkl'
#         res = executeQuery(sql, [var])
#         flash("Successful", "success")
#         return redirect('/button')
#     flash("test", "danger")    
#     return render_template('test.html')

# def get_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect('main.sqlite')
#     return db

def executeQuery(query, params):
	conn = db
	cursor = conn.cursor()
	results = cursor.execute(query, params).fetchall()
	conn.commit()
	# conn.close()
	return results

def availableUsername(username):
    # check if username available when registering
    res = executeQuery("select count() from users where u_username = ?", [username])
    return res[0][0] == 0

def insertUser(username, password):
    # function to insert user when registering
    conn = db
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