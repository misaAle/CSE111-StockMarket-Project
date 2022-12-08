import sqlite3
import random
from datetime import date
from application import app
from flask import render_template, g, request, url_for, redirect, session, flash
from application.forms import LoginForm, RegisterForm
from application import db


@app.route("/")
@app.route("/home", methods=['POST', 'GET'])
def home():
    funds=0
    if session.get('user_id'):
        funds = executeQuery("SELECT u_acctbal FROM users WHERE u_userid = ?", [session['user_id']])[0][0]
    if request.method == 'POST':
        sql = """UPDATE users
        SET u_acctbal = round(u_acctbal + ?, 2)
        WHERE u_userid = ?"""
        
        params = int(request.form['addCustom'])
        
        if params < 0:
            flash("Please enter a positive number", "danger")
            return redirect('/home')
        res = executeQuery(sql, [params, session['user_id']])
        return redirect('/home')

    
    return render_template("home.html", funds=funds, home=True)

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
            if username == 'admin' and password == 'admin':
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
        # print(request.form.items, request.form.get('buy-submission'))
        if request.form.get('buy-submission') != "":
            ticker = request.form.get("ticker")
            quantity = request.form.get("buy-submission")
            price = executeQuery("SELECT s_price FROM stocks WHERE s_ticker = ?", [ticker])[0][0]
            total = price * int(quantity)
            
            if checkBalance(session['user_id']) < total:
                flash(f"Unfortunately, you do not have at least ${total} in your balance.", "danger")
                return redirect('/stocks')
            else:
                today = date.today()
                today = today.strftime("%Y-%m-%d")
                sql1 = """INSERT INTO orders (o_userid, o_ticker, o_quantity, o_tickerprice, o_orderdate)
                VALUES
                    (?, ?, ?, ?, ?);"""
                params1 = [session['user_id'], ticker, quantity, price, today]

                res = executeQuery(sql1, params1)

                sql2 = """UPDATE users
                SET u_acctbal = round(u_acctbal - ?, 2)
                WHERE u_userid = ?;"""
                params2 = [total, session['user_id']]

                res = executeQuery(sql2, params2)

                checkUserInPortfolio = executeQuery("SELECT count(p_userid) FROM portfolio WHERE p_userid = ?", [session['user_id']])[0][0]
                checkTickerInPortfolio = executeQuery("SELECT count(p_ticker) FROM portfolio WHERE p_userid = ? AND p_ticker = ?", [session['user_id'], ticker])[0][0]
                if checkUserInPortfolio == 0 or checkTickerInPortfolio == 0:
                    res = executeQuery("""INSERT INTO portfolio
                    VALUES
                        (?,?,?);""", [session['user_id'], ticker, quantity])
                else:
                    sql3 = """UPDATE portfolio
                    SET p_quantity = p_quantity + ?
                    WHERE p_userid = ?"""
                    params3 = [quantity, session['user_id']]
                    res = executeQuery(sql3, params3)
                
                flash("Congrats", "success")
            return redirect('/portfolio')
        elif request.form.get('watchlist-submission') == 'Add to Watchlist':
            # print('Submitted')
            ticker = request.form.get("ticker")
            # print(ticker)
            sql = """INSERT INTO watchlist
                VALUES
                    (?, ?)"""
            params = [session['user_id'], ticker ]
            res = executeQuery(sql, params)
            return redirect('/watchlist')
        elif request.form.get('updateStocks') == 'Update Stocks':
            print('Stocks Updated!')
            for i in range(504):
                randomUpdate = random.uniform(-10.0, 10.0)
                res = executeQuery("""UPDATE stocks
                SET s_price = round(s_price*(1+?),2),
                s_cap = round(s_price * s_volume,2)
                WHERE s_ticker in 
                (SELECT s_ticker FROM stocks
                ORDER BY RANDOM()
                LIMIT 1);""", [randomUpdate/100])
            return redirect('/stocks')
        
    conn = db
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute("select * from stocks;")
    stock_rows = cur.fetchall()

    return render_template("stocks.html",stock_rows=stock_rows,stocks=True)

@app.route('/crypto', methods=['POST', 'GET'])
def crypto():

    if request.method == 'POST':
        if request.form.get('buy-crypto') != "":
                ticker = request.form.get("crypto-ticker")
                quantity = request.form.get("buy-crypto")
                price = executeQuery("SELECT c_price FROM crypto WHERE c_ticker = ?", [ticker])[0][0]
                total = price * int(quantity)
                
                if checkBalance(session['user_id']) < total:
                    flash(f"Unfortunately, you do not have at least ${total} in your balance.", "danger")
                    return redirect('/crypto')
                else:
                    today = date.today()
                    today = today.strftime("%Y-%m-%d")
                    sql1 = """INSERT INTO orders (o_userid, o_ticker, o_quantity, o_tickerprice, o_orderdate)
                    VALUES
                        (?, ?, ?, ?, ?);"""
                    params1 = [session['user_id'], ticker, quantity, price, today]

                    res = executeQuery(sql1, params1)

                    sql2 = """UPDATE users
                    SET u_acctbal = u_acctbal - ?
                    WHERE u_userid = ?;"""
                    params2 = [total, session['user_id']]

                    res = executeQuery(sql2, params2)

                    checkUserInPortfolio = executeQuery("SELECT count(p_userid) FROM portfolio WHERE p_userid = ?", [session['user_id']])[0][0]
                    checkTickerInPortfolio = executeQuery("SELECT count(p_ticker) FROM portfolio WHERE p_userid = ? AND p_ticker = ?", [session['user_id'], ticker])[0][0]
                    if checkUserInPortfolio == 0 or checkTickerInPortfolio == 0:
                        res = executeQuery("""INSERT INTO portfolio
                        VALUES
                            (?,?,?);""", [session['user_id'], ticker, quantity])
                    else:
                        sql3 = """UPDATE portfolio
                        SET p_quantity = p_quantity + ?
                        WHERE p_userid = ?"""
                        params3 = [quantity, session['user_id']]
                        res = executeQuery(sql3, params3)
                    flash("Congrats", "success")
                return redirect('/portfolio')
        elif request.form.get('crypto-watchlist-submission') == 'Add to Watchlist':
            # print('Submitted')
            ticker = request.form.get("ticker")
            # print(ticker)
            sql = """INSERT INTO watchlist
                VALUES
                    (?, ?)"""
            params = [session['user_id'], ticker ]
            res = executeQuery(sql, params)
            return redirect('/watchlist')
        elif request.form.get('updateCrypto') == 'Update Crypto':
            print('Crypto Updated!')
            for i in range(7):
                randomUpdate = random.uniform(-30.0, 30.0)
                res = executeQuery("""UPDATE crypto
                SET c_price = round(c_price*(1+?),2)
                WHERE c_ticker in 
                (SELECT c_ticker FROM crypto
                ORDER BY RANDOM()
                LIMIT 1);""", [randomUpdate/100])
            return redirect('/crypto')




    # if request.method == 'POST':
    #     if request.form.get('crypto-watchlist-submission') == 'Add to Watchlist':
    #         print('Submitted')
    #         ticker = request.form.get("crypto-ticker")
    #         print(ticker)
    #         sql = """INSERT INTO watchlist
    #             VALUES
    #                 (?, ?)"""
    #         params = [session['user_id'], ticker]
    #         res = executeQuery(sql, params)
    #         return redirect('/watchlist')
    
    conn = db
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute("select * from crypto;")
    crypto_rows = cur.fetchall()
    return render_template('crypto.html', crypto_rows=crypto_rows, crypto=True)

@app.route("/portfolio", methods=['POST', 'GET'])
def portfolio():
    
    if session.get('username'):

        if request.method == 'POST':
            if request.form.get('sell-stock-submission') == "Sell":
                print("bruh")
                ticker = request.form.get("portfolio-stock-ticker")
                sell_quantity = request.form.get("sell-stock-submission")
                price = executeQuery("SELECT s_price FROM stocks WHERE s_ticker = ?", [ticker])[0][0]
                total = price * int(quantity)
                user_quantity = executeQuery("SELECT p_quantity FROM portfolio WHERE p_userid = ? AND p_ticker = ?", \
                [session['user_id'], ticker])[0][0]
                if user_quantity > sell_quantity:
                    flash(f"You cannot sell more than what you own.")
                return redirect('/portfolio')
            pass

        conn = db
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.execute("""SELECT p_ticker, p_quantity FROM portfolio, users
        WHERE u_userid = p_userid
        AND p_ticker not in
        (SELECT c_ticker FROM crypto)
        AND u_userid = ?;""", [session['user_id']])
        stock_portfolio_rows = cur.fetchall()

        cur.execute("""SELECT DISTINCT p_ticker FROM portfolio, users, crypto
        WHERE u_userid = p_userid
        AND p_ticker in
        (SELECT c_ticker FROM crypto)
        AND u_userid = ?;""", [session['user_id']])
        crypto_portfolio_rows = cur.fetchall()

        return render_template("portfolio.html", stock_portfolio_rows=stock_portfolio_rows, crypto_portfolio_rows=crypto_portfolio_rows, portfolio=True)
    return render_template("portfolio.html", portfolio=True)

@app.route("/watchlist")
def watchlist():
    if session.get('username'):
        conn = db
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.execute("""SELECT w_ticker FROM watchlist, users
        WHERE u_userid = w_userid
        AND w_ticker not in
        (SELECT c_ticker FROM crypto)
        AND u_userid = ?;""", [session['user_id']])
        watchlist_stock_rows = cur.fetchall()

        cur.execute("""SELECT DISTINCT w_ticker FROM watchlist, users, crypto
        WHERE u_userid = w_userid
        AND w_ticker in
        (SELECT c_ticker FROM crypto)
        AND u_userid = ?;""", [session['user_id']])
        watchlist_crypto_rows = cur.fetchall()

        return render_template("watchlist.html", watchlist_stock_rows=watchlist_stock_rows, watchlist_crypto_rows=watchlist_crypto_rows,watchlist=True)
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

@app.route('/users', methods=['POST', 'GET'])
def users():
    if session.get('username') != 'admin':
        return redirect('/home')

    if request.method == 'POST':
        if request.form.get('deleteUser') == 'Remove User':
            user = request.form.get('user')
            sql = """DELETE FROM users
            WHERE u_username = ?"""
            res = executeQuery(sql, [user])
            return redirect('/users')
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

def checkBalance(user_id):
    res = executeQuery("SELECT u_acctbal FROM users WHERE u_userid = ?", [user_id])
    return res[0][0]

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()