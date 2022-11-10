from application import app
from flask import render_template

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", home=True)

@app.route("/stocks")
def stocks():
    return render_template("home.html",stocks=True)

@app.route("/portfolio")
def portfolio():
    return render_template("home.html",portfolio=True)

@app.route("/watchlist")
def watchlist():
    return render_template("home.html",watchlist=True)
