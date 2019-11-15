import json
from flask import Flask, render_template, request, redirect, url_for , send_from_directory
from flask_mongoengine import MongoEngine, Document
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, Length, InputRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'faculty_auth',
    'host': 'mongodb://localhost:27017/faculty_auth'
}

app.config['SECRET_KEY'] = 'hello'

db = MongoEngine(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@app.route("/")
def documentation():
    #return "Hello World"
    return send_from_directory("/home/rohit/DataBase_Project/","documentation.txt")

class User(UserMixin, db.Document):
    meta = {'collection': 'User_Auth'}
    email = db.StringField(max_length=30)
    password = db.StringField()

@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()


class RegForm(FlaskForm):
    email = StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=20)])

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if request.method == 'POST':
        if form.validate():
            existing_user = User.objects(email=form.email.data).first()
            if existing_user is None:
                hashpass = generate_password_hash(form.password.data, method='sha256')
                hey = User(form.email.data,hashpass).save()
                login_user(hey)
                return redirect(url_for('dashboard'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated == True:
        return redirect(url_for('dashboard'))
    form = RegForm()
    if request.method == 'POST':
        if form.validate():
            check_user = User.objects(email=form.email.data).first()
            if check_user:
                if check_password_hash(check_user['password'], form.password.data):
                    login_user(check_user)
                    return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.email)

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
