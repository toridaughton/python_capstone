from os import environ
from forms import RegisterForm, LoginForm, EntryForm, DiagnosisForm
from flask_login import login_user, login_required, logout_user, LoginManager, current_user
from flask import Flask, render_template, request, redirect, url_for, flash, session
from model import User, entry_symptoms, entry_categories, entry_diagnoses, Entry, Symptoms, Categories, Diagnosis
from model import connect_to_database, db
from flask_migrate import Migrate

# Must create an instance of flask. Convention is to name variable app
app = Flask(__name__)

# Migrate allows for db edits, prevents need for dropping db.
migrate = Migrate(app, db)

# Flask requires secrete key to protect stored sessions in server
app.secret_key = environ["SERVER_SECRET_KEY"]

# Module that provides session management
login_manager = LoginManager()

# Initiate Login manager and passing in the flask app variable
login_manager.init_app(app)

# View name
login_manager.login_view = 'login'


# Keeps track of the current logged in user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/register', methods=["GET","POST"])
def registration():
    # Calling an instance of the Register form and setting to variable
    form = RegisterForm()
    if form.validate_on_submit():

        # because we have the __init__ for the users table we do not need **kwargs (keyword arguments, don't need to make anything equal)
        user = User(form.first_name.data,
                    form.last_name.data,
                    form.dob.data,
                    form.email.data,
                    form.username.data,
                    form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Registration Successful. Welcome!', 'success')
        return redirect('/login')
    
    return render_template('registration.html', form=form, title='Sign-Up')
    

@app.route('/login', methods=[ "GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.email.data).first()
        
        if user.check_password(form.password.data) and user is not None:

            login_user(user)

            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next = url_for('homepage')

            flash('Login Success', 'success')
            return redirect(next)
    return render_template('login.html', form=form, title='Login')

@app.route('/new-entry', methods=["GET", "POST"])
@login_required
def entry():

    # Utilize flask-login to get current user logged in. Be sure to import current_user.
    # This will give you the current_user (User table) that you can drill into for specific info (i.e id)
    if current_user.is_authenticated:
        user = current_user

    # Calling the DiagnosisForm and setting to variable to access data from.
    diagnosis_form = DiagnosisForm()
    diagnosis_answer = diagnosis_form.associated_diagnosis.data
    form = EntryForm()

    if form.submit2.data:
        symptom = Symptoms(form.symptom.data)
        diagnosis = Diagnosis(form.diagnosis.data)
        category = Categories(form.category.data)
        entry = Entry(form.entry_details.data, user.id)

        db.session.add_all([entry, diagnosis, symptom, category])
        db.session.commit()

        entry.symptoms.append(symptom)
        entry.diagnoses.append(diagnosis)
        entry.categories.append(category)
        db.session.commit()

        flash('Entry has been submitted', 'success')
        return redirect('/past-entries')

    return render_template('entry_page.html', title='New Entry', form=form, diagnosis_form=diagnosis_form, answer=diagnosis_answer)


@app.route('/past-entries', methods=["GET", "POST"])
@login_required
def past_entries():
    return render_template('past_entries_log.html', title='Past Entries')


@app.route('/logout')
@login_required
def logout():
    flash('You have been logged out', 'info')
    logout_user()
    return redirect(url_for('homepage'))


if __name__ == '__main__':

    connect_to_database(app)

    app.run(port=4050, debug=True)
