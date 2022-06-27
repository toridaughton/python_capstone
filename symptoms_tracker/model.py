from datetime import datetime
from os import environ
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    
    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.DateTime)
    user_email = db.Column(db.String(50), unique=True, index=True, nullable=False)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    hash_password = db.Column(db.String(500), nullable=False)
    entries = db.relationship('Entry', backref='user', lazy=True)


    def __init__(self, first_name, last_name, dob, user_email, username, hash_password):
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.user_email = user_email
        self.username = username
        self.hash_password = generate_password_hash(hash_password)
    
    def check_password(self, password):
        return check_password_hash(self.hash_password, password)

    def __repr__(self):
        return f'User: user_id = {self.id}, username = {self.username}'


entry_symptoms = db.Table(
    "entry_symptoms", db.metadata,
    db.Column('entry_id', db.Integer, db.ForeignKey('entries.id')),
    db.Column('symptom_id', db.Integer, db.ForeignKey('symptoms.id'))
)


entry_categories = db.Table(
    "entry_categories", db.metadata,
    db.Column('entry_id', db.Integer, db.ForeignKey("entries.id")),
    db.Column('category_id', db.Integer, db.ForeignKey("categories.id"))
)

entry_diagnoses = db.Table(
    "entry_diagnoses", db.metadata,
    db.Column('entry_id', db.Integer, db.ForeignKey("entries.id")),
    db.Column('diagnosis_id', db.Integer, db.ForeignKey("diagnoses.id"))
)


class Entry(db.Model):
    __tablename__ = "entries"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    entry_details = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    symptoms = db.relationship("Symptoms", secondary=entry_symptoms,
                                backref="entry")
    categories = db.relationship("Categories",secondary=entry_categories,
                                  backref="entry")
    diagnoses = db.relationship("Diagnosis", secondary=entry_diagnoses,
                                 backref="entry")
    entry_date_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, entry_details, user_id):
        self.entry_details = entry_details
        self.user_id = user_id

    def __repr__(self):
        return f'Entry on {self.entry_date_time} for diagnosis: {self.diagnosis_name}, symptom: {self.symptom_name} with category: {self.category_name}'


class Symptoms(db.Model):
    __tablename__ = "symptoms"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    symptom_name = db.Column(db.String(80))
    entries = db.relationship('Entry', secondary="entry_symptoms",  lazy='subquery',
        backref=db.backref('entries_symptoms', lazy=True))


    def __init__(self, symptom_name):
        self.symptom_name = symptom_name

    def __repr__(self):
        return f'Symptom: {self.symptom_name}'


class Categories(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category_name = db.Column(db.String(80))
    entries = db.relationship('Entry', secondary="entry_categories",  lazy='subquery',
        backref=db.backref('entries_categories', lazy=True))

    def __init__(self, category_name):
        self.category_name = category_name

    def __repr__(self):
        return f'Category: {self.category_name}'


class Diagnosis(db.Model):
    __tablename__ = "diagnoses"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    diagnosis_name = db.Column(db.String(100))
    entries = db.relationship('Entry', secondary="entry_diagnoses",  lazy='subquery',
        backref=db.backref('entries_diagnoses', lazy=True))

    def __init__(self, diagnosis_name):
        self.diagnosis_name = diagnosis_name
    
    def __repr__(self):
        return f'Diagnosis: {self.diagnosis_name}'




def connect_to_database(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = environ["POSTGRES_URI"]
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    from server import app
    connect_to_database(app)
    print("Connected to database...")