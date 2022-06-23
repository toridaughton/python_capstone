from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateTimeField, SubmitField, ValidatorError
from wtforms.validators import DataRequired, Email, EqualTo
from model import User

# inherit from FlaskForm with newly created form class 
class RegisterForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[ DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords must match!')])
    pass_confirm = PasswordField('Comfirm Password', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    dob = DateTimeField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already in use!')

    def check_username(self, field):
        if User.query.filter_by(username=field).first():
            raise ValidatorError('Username is taken!')
        

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validatoris=[DataRequired()])
    submit = SubmitField('Log In')