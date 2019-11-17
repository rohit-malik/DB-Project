import json
import os
from flask import Flask, render_template, request, redirect, url_for , send_from_directory
from flask_mongoengine import MongoEngine, Document
from flask_wtf import FlaskForm
from wtforms import TextField
from wtforms import StringField, PasswordField , DateField
from wtforms.validators import Email, Length, InputRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_pymongo import PyMongo
from bson.binary import Binary
import base64
from bson import BSON

app = Flask(__name__)


app.config['MONGO_DBNAME'] = 'faculty_auth'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/faculty_auth'
app.config['SECRET_KEY'] = 'hello'

mongo = PyMongo(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

users = mongo.db.User_Auth
facultys = mongo.db.Faculty_profile

@app.route("/")
def documentation():
    return send_from_directory(os.getcwd(),"documentation.txt")


class User():

    def __init__(self, useremail):
        self.useremail = useremail

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.useremail

@login_manager.user_loader
def load_user(user_id):
    user = users.find_one({'email': user_id})
    if not user:
        return None
    return User(user['email'])


class RegForm(FlaskForm):
    email = StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=20)])


class FacultyDetails(FlaskForm):
    #name = TextField("Name")
    name = StringField('name', validators=[InputRequired(), Length(max=30)])
    email = StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    dob = DateField('dob', validators=[InputRequired(), Length(max=30)])
    publications = StringField('publications', validators=[InputRequired(), Length(max=30)])
    biography = StringField('biography', validators=[InputRequired(), Length(max=30)])
    about = StringField('about', validators=[InputRequired(), Length(max=30)])
    teachinginterest = StringField('name', validators=[InputRequired(), Length(max=30)])
    projects = StringField('projects', validators=[InputRequired(), Length(max=30)])
    biography = StringField('biography', validators=[InputRequired(), Length(max=30)])
    researchkeywords = StringField('researchkeywords', validators=[InputRequired(), Length(max=30)])
    researchwork = StringField('researchwork', validators=[InputRequired(), Length(max=30)])
    awards = StringField('awards', validators=[InputRequired(), Length(max=30)])



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if request.method == 'POST':
        if form.validate():
            existing_user = users.find_one({'email': form.email.data})
            if existing_user is None:
                hashpass = generate_password_hash(form.password.data, method='sha256')
                user_id = users.insert({
                    'email': form.email.data,
                    'password': hashpass
                })
                hey = users.find_one({'_id': user_id})
                user = User(hey['email'])
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated == True:
        return redirect(url_for('dashboard'))
    form = RegForm()
    if request.method == 'POST':
        if form.validate():
            check_user = users.find_one({'email': form.email.data})
            if check_user:
                if check_password_hash(check_user['password'], form.password.data):
                    login_user(User(check_user['email']))
                    return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    form = FacultyDetails()
    faculty = facultys.find_one({'Email': current_user.useremail})
    if faculty is None:
        return redirect(url_for('editinfo'))
    if facultys.find({'_id': faculty['_id'], 'profile_pic': {"$exists":True}}).count() > 0:
        ppic_binary = faculty['profile_pic']
        ppic = base64.b64encode(ppic_binary).decode("utf-8")
        #ppic = BSON.decode(ppic_binary)
        # ppic = ppic_binary
        #print(ppic)
        return render_template('index.html', name=faculty['Name'], Department=faculty['Department'],Email=faculty['Email'],Phone_No=faculty['Phone-No'],Website=faculty['Website'],About_me=faculty['About-me'],Research_area=faculty['Research-area'], profile_pic=ppic, form=form)
    else:
        return render_template('index.html', name=faculty['Name'], Department=faculty['Department'],Email=faculty['Email'],Phone_No=faculty['Phone-No'],Website=faculty['Website'],About_me=faculty['About-me'],Research_area=faculty['Research-area'], profile_pic="", form=form)

@app.route('/editinfo', methods=['GET', 'POST'])
@login_required
def editinfo():
    form = FacultyDetails()
    if request.method == 'POST':
        name = request.form['Name']
        dept = request.form['Department']
        email = request.form['Email']
        ph = request.form['Phone_No']
        website = request.form['Website']
        about_me = request.form['About_me']
        research_area = request.form['Research_area']
        profile_pic = request.files['profile_pic'].read()
        binary_profile_pic = Binary(profile_pic)
        faculty = facultys.find_one({'Email': current_user.useremail})
        if faculty is None:
            facultys.insert({
                'Name': name,
                'Department': dept,
                'Email': email,
                'Phone-No': ph,
                'Website': website,
                'About-me': about_me,
                'Research-area': research_area,
                'profile_pic': binary_profile_pic
            })
        else:
            facultys.update({'_id': faculty['_id']}, {
                'Name': name,
                'Department': dept,
                'Email': email,
                'Phone-No': ph,
                'Website': website,
                'About-me': about_me,
                'Research-area': research_area,
                'profile_pic': binary_profile_pic
            })
        return redirect(url_for('dashboard'))
    faculty = facultys.find_one({'Email': current_user.useremail})
    if faculty is None:
        return render_template('editinfo.html')
    return render_template('editinfo.html', name=faculty['Name'], Department=faculty['Department'],Email=faculty['Email'],Phone_No=faculty['Phone-No'],Website=faculty['Website'],About_me=faculty['About-me'],Research_area=faculty['Research-area'],form=form)

@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



if __name__ == "__main__":
    app.run(host='127.0.0.1', port="8001")
