import sqlite3
from flask import Flask
from flask_session import Session
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
session = Session(app)

db = sqlite3.connect('main.sqlite', check_same_thread=False)

from application import routes