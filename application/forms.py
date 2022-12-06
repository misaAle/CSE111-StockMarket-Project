# import sqlite3
# from flask import g
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from application import db

# db = getattr(g, '_database', None)
# if db is None:
#     db = g._database = sqlite3.connect('main.sqlite')

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_username(self,username):
        cur = db.cursor()
        res = cur.execute("SELECT count() FROM users WHERE u_username = ?", [username.data]).fetchall()
        if res[0][0] != 0:
            raise ValidationError("Username is already in use.")
