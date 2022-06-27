from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, RadioField, SubmitField, TextAreaField, SelectField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, optional, length
from model import User

# inherit from FlaskForm with newly created form class 
class RegisterForm(FlaskForm):

    first_name = StringField('First Name ', validators=[DataRequired()])
    last_name = StringField('Last Name ', validators=[DataRequired()])
    dob = DateField('Date of Birth ', format='%Y-%m-%d', validators=[DataRequired()])
    email = StringField('Email ', validators=[DataRequired(), Email(message='Must input valid email')])
    username = StringField('Username ', validators=[DataRequired()])
    password = PasswordField('Password ', validators=[length(min=10), DataRequired(), EqualTo('confirm_pass', message='Passwords must match!')])
    confirm_pass = PasswordField('Confirm Password ', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def check_email(self, field):
        if User.query.filter_by(user_email=field.data).first():
            raise ValidationError('Email already in use!')

    def check_username(self, field):
            raise ValidationError('Username is taken!')
        

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class DiagnosisForm(FlaskForm):
    associated_diagnosis = RadioField('Is there an associated Diagnosis?', choices=['yes', 'no'])
    submit1 = SubmitField('Submit')

class EntryForm(FlaskForm):
    diagnosis = SelectField('Diagnosis', validators=[DataRequired()], choices=["Cancer", "Celiac Disease", "Cohn's Disease", "Diabetes", "Diverticulitis", "Endometriosis", "Epilepsy", "Fibromyalgia", "Flu", "Irritable bowel syndrome (IBS)", "Kidney Stones", "Unknown"])
    other_diagnosis = StringField('Other Diagnosis', validators=[optional()])
    symptom = SelectField('Symptom', validators=[DataRequired()], choices=["Congestion","Headache", "Lethargic", "Nausea", "Numbness", "Other", "Pain","Vertigo" ])
    entry_details = TextAreaField('Details', validators=[DataRequired()])  
    category = SelectField('What specialty is this related to?', validators=[DataRequired()], choices=["Cardiology (heart)", "Dermatology (skin)", "Endocrinology (hormone-related)", "ENT (ears, nose, throat)", "Gastroenterology (GI / Abdomen)", "Opthamology (eyes)", "Oncology (cancer)", "Other", "Unknown", "Urology (urinary)"])
    other_category = StringField('Other Category', validators=[optional()])
    submit2 = SubmitField('Submit')    