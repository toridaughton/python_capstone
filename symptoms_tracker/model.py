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
        """ Check that the regular password matches the password stored after it has been hashed """
        return check_password_hash(self.hash_password, password)

    def __repr__(self):
        return f'<User: user_id = {self.id}>, <Username = {self.username}>'




class Entry(db.Model):
    """ Entries Table inheriting from db.Model"""
    __tablename__ = "entries"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    entry_details = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    entry_date_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, entry_details, user_id):
        self.entry_details = entry_details
        self.user_id = user_id

    def __repr__(self):
        return f'<Entry on {self.entry_date_time} for diagnosis: {self.diagnosis_name}, symptom: {self.symptom_name} with category: {self.category_name}>'

    def get_diagnosis_id(self, id):
        """ Queries through junction table to get Diagnosis class object through Entry class object's id"""
        entry = EntryDiagnoses.query.filter_by(entry_id=id).first()
        diagnosis = Diagnosis.query.filter_by(id=entry.diagnosis_id).first()
        return diagnosis
    
    def get_symptom_id(self, id):
        """ Queries through junction table to get Symptoms class object through Entry class object's id"""
        entry = EntrySymptoms.query.filter_by(entry_id=id).first()
        symptom = Symptoms.query.filter_by(id=entry.symptom_id).first()
        return symptom

    def get_category_id(self,id):
        """ Queries through junction table to get Categories class object through Entry class object's id"""
        entry = EntryCategories.query.filter_by(entry_id=id).first()
        category = Categories.query.filter_by(id=entry.category_id).first()
        return category


class Symptoms(db.Model):
    __tablename__ = "symptoms"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    symptom_name = db.Column(db.String(80))

    def __init__(self, symptom_name):
        self.symptom_name = symptom_name

    def __repr__(self):
        return f'<Symptom: {self.symptom_name}>'


class EntrySymptoms(db.Model):
    __tablename__ = "entry_symptoms"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey('entries.id'))
    symptom_id = db.Column(db.Integer, db.ForeignKey('symptoms.id'))

    def __repr__(self):
        return f'<Entry ID: {self.entry_id}>, <Symptom ID: {self.symptom_id}>'


class Categories(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category_name = db.Column(db.String(80))
   

    def __init__(self, category_name):
        self.category_name = category_name

    def __repr__(self):
        return f'<Category: {self.category_name}>'


class EntryCategories(db.Model):
    __tablename__ = "entry_categories"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey('entries.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def __repr__(self):
        return f'<Entry ID: {self.entry_id}>, <Category ID: {self.category_id}>'


class Diagnosis(db.Model):
    __tablename__ = "diagnoses"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    diagnosis_name = db.Column(db.String(100))

    def __init__(self, diagnosis_name):
        self.diagnosis_name = diagnosis_name
    
    def __repr__(self):
        return f'<Diagnosis: {self.diagnosis_name}>'


class EntryDiagnoses(db.Model):
    __tablename__ = "entry_diagnoses"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey('entries.id'))
    diagnosis_id = db.Column(db.Integer, db.ForeignKey('diagnoses.id'))

    def __repr__(self):
        return f'<Entry ID: {self.entry_id}>, <Diagnosis ID: {self.diagnosis_id}>'

def baseline_select_options():
    """ Creates the baseline options for select fields in EntryForm by adding names to each respective table """

    baseline_diagnoses = ["Cancer", "Celiac Disease", "Cohn's Disease", "Diabetes", "Diverticulitis", "Endometriosis", "Epilepsy", "Fibromyalgia", "Flu", "Irritable bowel syndrome (IBS)", "Kidney Stones", "Unknown"]
    baseline_symptoms = ["Congestion","Headache", "Lethargic", "Nausea", "Numbness", "Other", "Pain","Vertigo" ]
    baseline_categories = ["Cardiology (heart)", "Dermatology (skin)", "Endocrinology (hormone-related)", "ENT (ears, nose, throat)", "Gastroenterology (GI / Abdomen)", "Opthamology (eyes)", "Oncology (cancer)", "Other", "Unknown", "Urology (urinary)"]
    
    for diagnosis in baseline_diagnoses:
        db.session.add(Diagnosis(diagnosis_name=diagnosis))

    for symptom in baseline_symptoms:
        db.session.add(Symptoms(symptom_name=symptom))

    for category in baseline_categories:
        db.session.add(Categories(category_name=category))

    db.session.commit()


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