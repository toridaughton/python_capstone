from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateTimeField, SubmitField 

# inherit from FlaskForm with newly created form class 
class RegisterForm(FlaskForm):

    username = StringField("Username: ")
    email = StringField("Email: ")
    password = PasswordField("Password: ", [])
    first_name = StringField("First Name: ")
    last_name = StringField("Last Name: ")
    dob = DateTimeField("Date of Birth: ", format='%Y-%m-%d')
    submit = SubmitField("Submit")


class LoginForm()