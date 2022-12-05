import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '0iL6q4m6fHWrmz2_4m0KYw'