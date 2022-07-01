from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, RadioField, SubmitField, TextAreaField, SelectField, ValidationError, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, optional, length
from model import User, Diagnosis, Symptoms, Categories

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
    submit = SubmitField('Submit')


class EntryForm(FlaskForm):
    diagnosis = SelectField('Diagnosis', validators=[DataRequired()], default=None)
    other_diagnosis = StringField('Other Diagnosis', validators=[optional()])
    symptom = SelectField('Symptom', validators=[DataRequired()], default=None)
    entry_details = TextAreaField('Details', validators=[DataRequired()], default=None)  
    category = SelectField('What specialty is this related to?', validators=[DataRequired()], default=None)
    other_category = StringField('Other Category', validators=[optional()], default=None)
    # hidden_id = HiddenField()
    entry_submit = SubmitField('Submit')

    def update_choices(self):
        self.diagnosis.choices = [(d.id, d.diagnosis_name) for d in Diagnosis.query.all()]
        self.symptom.choices = [(s.id, s.symptom_name) for s in Symptoms.query.all()]
        self.category.choices = [(c.id, c.category_name) for c in Categories.query.all()]


# class EditEntryForm(FlaskForm):
#     diagnosis = SelectField('Diagnosis', validators=[DataRequired()])
#     other_diagnosis = StringField('Other Diagnosis', validators=[optional()])
#     symptom = SelectField('Symptom', validators=[DataRequired()])
#     entry_details = TextAreaField('Details', validators=[DataRequired()])  
#     category = SelectField('What specialty is this related to?', validators=[DataRequired()])
#     other_category = StringField('Other Category', validators=[optional()])
#     update = SubmitField("Update")


# class ConfirmDelete(FlaskForm):
#     confirm = RadioField('Are you sure you want to delete this entry?', choices=['Yes', 'No'])

class DeleteEntryForm(FlaskForm):
    hidden = HiddenField()
    delete = SubmitField("DELETE")
