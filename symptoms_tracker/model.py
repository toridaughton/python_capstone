from datetime import datetime
from os import environ
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager

db = SQLAlchemy()

login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    
    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.DateTime)
    user_email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    hash_password = db.Column(db.String(500), nullable=False)

    def __init__(self, email, username, password):
        self.user_email
        self.username
        self.hash_password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.hash_password, password)

    def __repr__(self):
        return f'User: user_id = {self.user_id}, username = {self.username}'


class Entry(db.Model):
    __tablename__ = "entries"

    entry_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    entry_details = db.Column(db.String(500), nullable=False)
    entry_date_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Entry on {self.entry_date_time} for diagnosis: {self.diagnosis_name}, symptom: {self.symptom_name} with category: {self.category_name}'


class Symptom(db.Model):
    __tablename__ = "symptoms"

    symptom_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    symptom_name = db.Column(db.String(80))

    def __repr__(self):
        return f'Symptom: {self.symptom_name}'


class EntrySymptom(db.Model):
    __tablename__ = "entry_symptoms"

    entry_symptom_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey("entries.entry_id"))
    symptom_id = db.Column(db.Integer, db.ForeignKey("symptoms.symptom_id"))


class Categories(db.Model):
    __tablename__ = "categories"

    category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category_name = db.Column(db.String(80))

    def __repr__(self):
        return f'Category: {self.category_name}'


class EntryCategory(db.Model):
    __tablename__ = "entry_categories"

    entry_category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey("entries.entry_id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id"))


class Diagnosis(db.Model):
    __tablename__ = "diagnoses"

    diagnosis_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    diagnosis_name = db.Column(db.String(100))
    
    def __repr__(self):
        return f'Diagnosis: {self.diagnosis_name}'


class EntryDiagnosis(db.Model):
    __tablename__ = "entry_diagnoses"

    entry_diagnosis_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey("entries.entry_id"))
    diagnosis_id = db.Column(db.Integer, db.ForeignKey("diagnoses.diagnosis_id"))



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