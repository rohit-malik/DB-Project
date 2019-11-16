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

app = Flask(__name__)

# app.config['MONGODB_SETTINGS'] = {
#     'db': 'faculty_auth',
#     'host': 'mongodb://localhost:27017/faculty_auth'
# }

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
    #return "Hello World"
    #print(os.getcwd())
    return send_from_directory(os.getcwd(),"documentation.txt")
    #return send_from_directory("/home/rohit/DataBase_Project/","documentation.txt")

# class User(UserMixin, mongo.db.Document):
#     meta = {'collection': 'User_Auth'}
#     email = mongo.db.StringField(max_length=30)
#     password = mongo.db.StringField()

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
    # return User.objects(pk=user_id).first()


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
            # existing_user = User.objects(email=form.email.data).first()
            existing_user = users.find_one({'email': form.email.data})
            if existing_user is None:
                hashpass = generate_password_hash(form.password.data, method='sha256')
                # hey = User(form.email.data,hashpass).save()
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
            # check_user = User.objects(email=form.email.data).first()
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
        return "No Faculty Portal Found"
    return render_template('index.html', name=faculty['Name'], form=form)

@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# @app.route("/user/", methods = ['POST', 'OPTIONS'])
# def refactor():
#     if request.method == "OPTIONS":
#         return "Message: wait"
#     try:
#         data = request.get_json()
#         refactor_type = data["refactorType"]
#         project_name = data["project"]
#         codebase_url = data["codebaseURL"]
#         cmd_gitclone = ['git', '-C','./temp_codebase', 'clone', codebase_url, '--depth=1']
#         project_final = "temp_codebase/" + project_name
#         cmd_delete = ['rm','-r', project_final]
#         proc = subprocess.Popen(cmd_gitclone, stdout=PIPE, stderr=PIPE)
#         stdout,stderr = proc.communicate()
#         """
#         print(stdout)
#         print("-------------------------------------------------")
#         print(stderr)
#         if stderr.decode("utf-8") != "":
#             return "E:The project could not be cloned. Provide valid git URL."
#         """
#         result = globals()[refactor_type](data)
#         proc = subprocess.Popen(cmd_delete, stdout=PIPE, stderr=PIPE)
#         stdout,stderr = proc.communicate()
#     except Exception as ex:
#         return "E:Invalid refactorType"
#     return result

if __name__ == "__main__":
    app.run(host='127.0.0.1', port="8001")
