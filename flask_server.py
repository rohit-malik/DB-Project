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
import ast
import psycopg2
from datetime import datetime as dt
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




class Facultyprofile():
    name = ""
    department = ""
    email = ""
    phone = ""
    website = ""
    about_me = ""
    research_area = []
    len_ra = 0
    current_research_interest = []
    len_cri = 0
    education_work = []
    len_eaw = 0
    teaching_interests = ""
    projects = []
    len_pr = 0
    publications = []
    len_pu = 0
    awards = []
    len_a = 0
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
    fp = Facultyprofile()
    faculty = facultys.find_one({'Email': current_user.useremail})
    if faculty is None:
        return redirect(url_for('editinfo'))
    fp.name = faculty['Name']
    fp.email = faculty['Email']
    fp.department = faculty['Department']
    fp.phone_no =  faculty['Phone-No']
    fp.website = faculty['Website']
    fp.about_me = faculty['About-me']
    fp.research_area = list(faculty['Research-area'])
    fp.len_ra = len(fp.research_area)
    fp.current_research_interest = list(faculty['Current-Research-interest'])
    fp.len_cri = len(fp.current_research_interest)
    fp.education_work = list(faculty['Education-Work'])
    fp.len_eaw = len(fp.education_work)
    fp.teaching_interests = faculty['Teaching-interests']
    fp.projects = list(faculty['Projects'])
    fp.len_pr = len(fp.projects)
    fp.publications = list(faculty['Publications'])
    fp.len_pu = len(fp.publications)
    fp.awards = list(faculty['Awards'])
    fp.len_a = len(fp.awards)
    list_research_area = list(faculty['Research-area'])
    if facultys.find({'_id': faculty['_id'], 'profile_pic': {"$exists":True}}).count() > 0:
        ppic_binary = faculty['profile_pic']
        ppic = base64.b64encode(ppic_binary).decode("utf-8")
        #ppic = BSON.decode(ppic_binary)
        # ppic = ppic_binary
        #print(ppic)
        return render_template('index.html', name=faculty['Name'], Department=faculty['Department'],Email=faculty['Email'],Phone_No=faculty['Phone-No'],Website=faculty['Website'],About_me=faculty['About-me'],Research_area=list_research_area,len_research_area=len(list_research_area),profile_pic=ppic, form=form,fp=fp)
    else:
        return render_template('index.html', name=faculty['Name'], Department=faculty['Department'],Email=faculty['Email'],Phone_No=faculty['Phone-No'],Website=faculty['Website'],About_me=faculty['About-me'],Research_area=list_research_area,len_research_area=len(list_research_area), profile_pic="", form=form,fp=fp)

@app.route('/leaveapplication', methods=['GET', 'POST'])
@login_required
def leavapplication():
    fp = Facultyprofile()
    connect_str = "dbname='facultyportal' user='matt' host='localhost' " + \
                  "password='toor'"
    if request.method == 'POST':
        startdate = request.form['StartDate']
        enddate = request.form['EndDate']
        comments = request.form['Comments']
        print(startdate,enddate,comments,"HI in the leave application")
        try:
            connect_str = "dbname='facultyportal' user='matt' host='localhost' " + \
                  "password='toor'"
            sql = """select faculty_id,post from faculty where faculty.email = %s"""
            records = (current_user.useremail,)
            #print("inside the try")
            conn = psycopg2.connect(connect_str)

            cursor = conn.cursor()

            cursor.execute(sql,records)
            row = cursor.fetchone()
            faculty_id = int(row[0])
            post = row[1]
            sql = """INSERT INTO application(faculty_id,start_date,end_date) VALUES(%s,%s,%s) RETURNING application_id"""
            #print(row)
            records = (int(row[0]),startdate,enddate)
            cursor.execute(sql,records)

            application_id = int(cursor.fetchone()[0])

            sql = """INSERT INTO application_log(application_id,comment,post,date_of_comment,action_taken) VALUES(%s,%s,%s,%s,%s)"""
            #print(row)
            records = (application_id,comments,post,dt.now(),"submitted")
            cursor.execute(sql,records)
            '''
            sql = """INSERT INTO application_log(application_id,comment,post,date_of_comment,action_taken) VALUES(%s,%s,%s,%s,%s)"""
            #print(row)
            records = (application_id,comments,post,dt.now(),"submitted")
            cursor.execute(sql,records)'''

            conn.commit() # <--- makes sure the change is shown in the database
            cursor.close()
            conn.close()
        except Exception as e:
            print("Uh oh, can't connect. Invalid dbname, user or password?")
            print(e)
    return render_template('leaveapplication.html',fp=fp)
    '''if request.method == 'POST':
        startdate = request.form['StartDate']
        enddate = request.form['EndDate']
        comments = request.form['Comments']
        print(startdate,enddate,comments)
    return redirect(url_for('dashboard'))'''

@app.route('/editinfo', methods=['GET', 'POST'])
@login_required
def editinfo():
    form = FacultyDetails()
    dep_dic = {"CSE":1,"ME":2,"EE":3}
    if request.method == 'POST':
        name = request.form['Name']
        dept = request.form['Department']
        email = request.form['Email']
        ph = request.form['Phone_No']
        website = request.form['Website']
        about_me = request.form['About_me']
        research_area = ast.literal_eval(request.form['Research_area'])
        current_research_interest = ast.literal_eval(request.form['Current_Research_interest'])
        education_work = ast.literal_eval(request.form['Education_Work'])
        teaching_interests = request.form['Teaching_interests']
        projects = ast.literal_eval(request.form['Projects'])
        publications = ast.literal_eval(request.form['Publications'])
        awards = ast.literal_eval(request.form['Awards'])


        profile_pic = request.files['profile_pic'].read()
        binary_profile_pic = Binary(profile_pic)
        faculty = facultys.find_one({'Email': current_user.useremail})
        if faculty is None:
            facultys.insert({
                'Name': name,
                'Department': dept,
                'Email': current_user.useremail,
                'Phone-No': ph,
                'Website': website,
                'About-me': about_me,
                'Research-area': research_area,
                'profile_pic': binary_profile_pic,
                'Current-Research-interest' : current_research_interest,
                'Education-Work' : education_work,
                'Teaching-interests' : teaching_interests,
                'Projects' : projects,
                'Publications' : publications,
                'Awards' : awards
            })
            try:
                connect_str = "dbname='facultyportal' user='matt' host='localhost' " + \
                  "password='toor'"
                sql = """INSERT INTO faculty(name,email,department_id,post,leaves_remaining,leaves_can_be_borrowed)
             VALUES(%s,%s,%s,%s,%s,%s)"""
                records = (name,str(current_user.useremail),dep_dic[dept],'Faculty',10,10)

                conn = psycopg2.connect(connect_str)

                cursor = conn.cursor()

                cursor.execute(sql,records)

                conn.commit() # <--- makes sure the change is shown in the database
                cursor.close()
                conn.close()
            except Exception as e:
                print("Uh oh, can't connect. Invalid dbname, user or password?")
                print(e)
        else:
            facultys.update({'_id': faculty['_id']}, {
                'Name': name,
                'Department': dept,
                'Email': current_user.useremail,
                'Phone-No': ph,
                'Website': website,
                'About-me': about_me,
                'Research-area': research_area,
                'profile_pic': binary_profile_pic,
                'Current-Research-interest' : current_research_interest,
                'Education-Work' : education_work,
                'Teaching-interests' : teaching_interests,
                'Projects' : projects,
                'Publications' : publications,
                'Awards' : awards
            })
            try:
                connect_str = "dbname='facultyportal' user='matt' host='localhost' " + \
                  "password='toor'"
                dep_dic = {"CSE":1,"ME":2,"EE":3}
                sql = """UPDATE faculty SET department_id = %s WHERE email = %s"""
                records = (dep_dic[dept],current_user.useremail)
                conn = psycopg2.connect(connect_str)

                cursor = conn.cursor()

                cursor.execute(sql,records)

                conn.commit() # <--- makes sure the change is shown in the database
                cursor.close()
                conn.close()
            except Exception as e:
                print("Uh oh, can't connect. Invalid dbname, user or password?")
                print(e)
        return redirect(url_for('dashboard'))
    faculty = facultys.find_one({'Email': current_user.useremail})
    fp = Facultyprofile()
    if faculty is None:
        return render_template('editinfo.html',fp=fp)
    fp.name = faculty['Name']
    fp.email = faculty['Email']
    fp.department = faculty['Department']
    fp.phone_no =  faculty['Phone-No']
    fp.website = faculty['Website']
    fp.about_me = faculty['About-me']
    fp.research_area = list(faculty['Research-area'])
    fp.len_ra = len(fp.research_area)
    fp.current_research_interest = list(faculty['Current-Research-interest'])
    fp.len_cri = len(fp.current_research_interest)
    fp.education_work = list(faculty['Education-Work'])
    fp.len_eaw = len(fp.education_work)
    fp.teaching_interests = faculty['Teaching-interests']
    fp.projects = list(faculty['Projects'])
    fp.len_pr = len(fp.projects)
    fp.publications = list(faculty['Publications'])
    fp.len_pu = len(fp.publications)
    fp.awards = list(faculty['Awards'])
    fp.len_a = len(fp.awards)
    return render_template('editinfo.html', name=faculty['Name'], Department=faculty['Department'],Email=faculty['Email'],Phone_No=faculty['Phone-No'],Website=faculty['Website'],About_me=faculty['About-me'],Research_area=faculty['Research-area'],fp=fp,form=form)

@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/frontpage', methods = ['GET', 'POST'])
def front_page():
    if request.method == 'POST':
        email_id = request.form['faculty_email']
        print(email_id.strip())
        print(type(email_id))
        email_id = email_id.strip()
        faculty = facultys.find_one({'Email': email_id})
        fp = Facultyprofile()
        fp.name = faculty['Name']
        fp.email = faculty['Email']
        fp.department = faculty['Department']
        fp.phone_no =  faculty['Phone-No']
        fp.website = faculty['Website']
        fp.about_me = faculty['About-me']
        fp.research_area = list(faculty['Research-area'])
        fp.len_ra = len(fp.research_area)
        fp.current_research_interest = list(faculty['Current-Research-interest'])
        fp.len_cri = len(fp.current_research_interest)
        fp.education_work = list(faculty['Education-Work'])
        fp.len_eaw = len(fp.education_work)
        fp.teaching_interests = faculty['Teaching-interests']
        fp.projects = list(faculty['Projects'])
        fp.len_pr = len(fp.projects)
        fp.publications = list(faculty['Publications'])
        fp.len_pu = len(fp.publications)
        fp.awards = list(faculty['Awards'])
        fp.len_a = len(fp.awards)
        return render_template('front_index.html',fp=fp)
    else:
        try:
            connect_str = "dbname='facultyportal' user='matt' host='localhost' " + \
                  "password='toor'"
            sql = """select name,email from faculty"""
            # records = (current_user.useremail,)
            #print("inside the try")
            conn = psycopg2.connect(connect_str)

            cursor = conn.cursor()

            cursor.execute(sql)
            row = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as e:
            print("Uh oh, can't connect. Invalid dbname, user or password?")
            print(e)
        return render_template('front_page.html',len_faculty = len(row), faculty_list=row)




if __name__ == "__main__":
    app.run(host='127.0.0.1', port="8001")
