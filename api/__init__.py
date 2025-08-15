# Initialize Flask app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_basicauth import BasicAuth

app = Flask(__name__)
db = SQLAlchemy()
basic_auth = BasicAuth()
