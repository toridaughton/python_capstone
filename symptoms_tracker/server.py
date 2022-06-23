from os import environ
from flask import Flask, render_template, request, redirect
from model import User, Entry, Symptom, EntrySymptom, Categories, EntryCategory, Diagnosis, EntryDiagnosis 
from forms import RegisterForm, login



app = Flask(__name__)

app.secret_key = environ["SERVER_SECRET_KEY"]


@app.route('/')
def homepage():
    pass


@app.route('/', methods=["POST"])
def registration():
    form = RegisterForm()

    if form.validate_on_submit():
       username = form.username.data
       email = form.email.data
       password = form.password.data
       first_name = form.first_name.data
       last_name = form.last_name.data
       dob = form.dob.data

    return redirect('/')


@app.route('/login', methods=["POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.email.data

    redirect('entry_page.html')