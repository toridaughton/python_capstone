from os import environ

from flask import Flask

from model import User, Symptom, Categories, Diagnosis, Entry

app = Flask(__name__)

app.secret_key = environ["SERVER_SECRET_KEY"]