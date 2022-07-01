from os import environ
from forms import RegisterForm, LoginForm, EntryForm, DiagnosisForm, DeleteEntryForm
from flask_login import login_user, login_required, logout_user, LoginManager, current_user
from flask import Flask, render_template, request, redirect, url_for, flash, session
from model import User, EntrySymptoms, EntryCategories, EntryDiagnoses, Entry, Symptoms, Categories, Diagnosis
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

        # Because we have the __init__ for the users table we do not need **kwargs (keyword arguments, don't need to make anything equal)
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
    form.update_choices()

    if form.entry_submit.data:

        entry = Entry(form.entry_details.data, user.id)

        db.session.add(entry)
        db.session.commit()

        diagnosis_chosen = form.diagnosis.data

        if diagnosis_chosen:
            entry_diagnosis = EntryDiagnoses(entry_id=entry.id, diagnosis_id=form.diagnosis.data)
            db.session.add(entry_diagnosis)
        entry_symptoms = EntrySymptoms(entry_id=entry.id, symptom_id=form.symptom.data)
        entry_categories = EntryCategories(entry_id= entry.id, category_id=form.category.data)

        db.session.add_all([entry_symptoms, entry_categories])
        db.session.commit()

        flash('Entry has been submitted', 'success')
        return redirect('/past-entries')

    return render_template('entry_page.html', title='New Entry', form=form, diagnosis_form=diagnosis_form, answer=diagnosis_answer)


@app.route('/past-entries', methods=["GET", "POST"])
@login_required
def past_entries():
    if current_user.is_authenticated:
        form = EntryForm()
        form.update_choices()
        entries = Entry.query.filter_by(user_id=current_user.id).all()
        if entries: # If an entry exists:
            for entry in entries:
                try:
                    entry.diagnosis = entry.get_diagnosis_id(entry.id)
                except:
                    print('no diagnosis for diagnosis!')
                else:
                    entry.diagnosis = entry.get_diagnosis_id(entry.id)
                    entry.symptom = entry.get_symptom_id(entry.id)
                    entry.category = entry.get_category_id(entry.id)
                finally:
                    entry.symptom = entry.get_symptom_id(entry.id)
                    entry.category = entry.get_category_id(entry.id)


        else: # If no entries exist
            flash("You don't have any entries!", "danger")
            return redirect('/new-entry')

        return render_template('past_entries_log.html', title='Past Entries', entries=entries, user=current_user)


@app.route('/past-entries/edit/<int:entry_id>', methods=["GET", "POST"])
@login_required
def edit_entry(entry_id):
    if current_user.is_authenticated:
        form = EntryForm()
        form.update_choices()

        entry = Entry.query.filter_by(id=entry_id).first()

        entry_symptom = EntrySymptoms.query.filter_by(entry_id=entry_id).first()
        entry_diagnosis = EntryDiagnoses.query.filter_by(entry_id=entry_id).first()
        entry_category = EntryCategories.query.filter_by(entry_id=entry_id).first()

        if entry_diagnosis:
            diagnosis = entry.get_diagnosis_id(id=entry_id)
        else:
            diagnosis = None
        category = entry.get_category_id(id=entry_id)
        symptom = entry.get_symptom_id(id=entry_id)

        if request.method == "GET":
            if diagnosis:
                form.diagnosis.default = diagnosis.id
            else: 
                form.diagnosis.default = 12
            form.symptom.default = symptom.id
            form.category.default = category.id
            form.entry_details.default = entry.entry_details
            form.process()

        if form.entry_submit.data:
            if not diagnosis:
                new_diagnosis_id = EntryDiagnoses(entry_id=entry_id, diagnosis_id=form.diagnosis.data)
                db.session.add(new_diagnosis_id)
            else: 
                entry_diagnosis.diagnosis_id = form.diagnosis.data
                db.session.add(entry_diagnosis)
            entry_symptom.symptom_id = form.symptom.data
            entry.entry_details = form.entry_details.data
            entry_category.category_id = form.category.data
            db.session.commit()

            return redirect('/past-entries')

        return render_template('entry_edit.html', form=form, entry=entry)


@app.route('/past-entries/delete/<int:entry_id>', methods=["GET","POST"])
@login_required
def delete_entry(entry_id):
    if current_user.is_authenticated:
        submit = DeleteEntryForm()
        entry = Entry.query.filter_by(id=entry_id).first()
        print(entry)
        try:
            diagnosis = entry.get_diagnosis_id(id=entry_id)
            print(diagnosis)
        except:
            print('Diagnosis id does not exist!')
        else:
            diagnosis = entry.get_diagnosis_id(id=entry_id)
            category = entry.get_category_id(id=entry_id)
            symptom = entry.get_symptom_id(id=entry_id)
        finally:
            category = entry.get_category_id(id=entry_id)
            symptom = entry.get_symptom_id(id=entry_id)
            
        entry_symptom = EntrySymptoms.query.filter_by(entry_id=entry_id, symptom_id=symptom.id).first()
        entry_category = EntryCategories.query.filter_by(entry_id=entry_id, category_id=category.id).first()

        if submit.delete.data:
            try:
                entry_diagnosis = EntryDiagnoses.query.filter_by(entry_id=entry_id, diagnosis_id=diagnosis.id).first()
                db.session.delete(entry_diagnosis)
            except:
                print("No diagnosis to delete")
            else:
                entry_diagnosis = EntryDiagnoses.query.filter_by(entry_id=entry_id, diagnosis_id=diagnosis.id).first()
                db.session.delete(entry_symptom)
                db.session.delete(entry_category)
                db.session.delete(entry)
            finally:
                db.session.delete(entry_symptom)
                db.session.delete(entry_category)
                db.session.delete(entry)
            db.session.commit()
            return redirect('/past-entries')
        
        return render_template('delete_entry.html', submit=submit)


@app.route('/logout')
@login_required
def logout():
    if current_user.is_authenticated:
        flash('You have been logged out', 'info')
        logout_user()
        return redirect(url_for('homepage'))


if __name__ == '__main__':

    connect_to_database(app)

    app.run(port=4050, debug=True)
