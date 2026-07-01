'''import sqlalchemy, os
from flask import Flask, request, render_template, redirect ,url_for
from flask_sqlalchemy import SQLAlchemy
#from application.models import *

app = Flask(__name__)
current_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(current_dir, "database.sqlite3")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Staff(db.Model):
    __tablename__='staff'
    staff_id = db.Column(db.String,primary_key=True)
    name = db.Column(db.String, nullable=False)
    mobile_no = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String,nullable=False)
    gender =  db.Column(db.String, nullable=False)

class User(db.Model):
    __tablename__='user'
    user_id = db.Column(db.String,primary_key=True)
    name = db.Column(db.String, nullable=False)
    mobile_no = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String,nullable=False)
    gender =  db.Column(db.String, nullable=False)

class Trek(db.Model):
    __tablename__='trek'
    trek_id = db.Column(db.String,primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, unique=True)
    difficulty =  db.Column(db.String, nullable=False)
    duration =  db.Column(db.String, nullable=False)
    current_status =  db.Column(db.String, nullable=False)

class Book(db.Model):
    __tablename__='booking'
    book_id = db.Column(db.String,primary_key=True)
    trek_id = db.Column(db.String,nullable=False)
    user_id = db.Column(db.String, nullable=False)
    booked_date = db.Column(db.String, nullable=False) 
    status = db.Column(db.String, nullable=False)

class Assignment(db.Model):
    __tablename__='assigned'
    assig_id = db.Column(db.String,primary_key=True)
    book_id = db.Column(db.String, nullable=False)
    user_id = db.Column(db.String,  nullable=False)
    staff_id = db.Column(db.String, nullable=False)
    assigned_date = db.Column(db.String, nullable=False)

@app.route("/",methods=["GET","POST"])
def signin():
    if request.method=="GET":
        return render_template("sign_in.html")
    elif request.method=="POST":
        name=request.form.get('name')
        mob=request.form.get('mob')
        mail=request.form.get('email')  
        passw=request.form.get('pass')
        gen=request.form.get('choice')
        existing = User.query.filter_by(email=mail).first()
        if existing:
            return render_template("user_already.html") 
        total=User.query.count()
        user__id="U000"+str(total+1)
        new_user = User(user_id=user__id,name=name,mobile_no=mob,email=mail,password=passw,gender=gen)
        db.session.add(new_user)
        db.session.commit()
        return render_template('welcome.html',id=user__id,mail=mail) 
    else:
        return render_template("error.html")
    
@app.route("/staff/signin",methods=["GET","POST"])
def staff_sin():
    if request.method=="GET":
        return render_template("staff_sin.html")
    elif request.method=="POST":
        name=request.form.get('name')
        mob=request.form.get('mob')
        mail=request.form.get('email')  
        passw=request.form.get('pass')
        gen=request.form.get('choice')
        existing = Staff.query.filter_by(email=mail).first()
        if existing:
            return render_template("staff_already.html") 
        total=Staff.query.count()
        id="S000"+str(total+1)
        new_user = Staff(staff_id=id,name=name,mobile_no=mob,email=mail,password=passw,gender=gen)
        db.session.add(new_user)
        db.session.commit()
        return render_template('welcome.html',id=id,mail=mail) 
    else:
        return render_template("error.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="GET":
        return render_template("log_in.html")
    elif request.method=="POST":
        user_id= request.form.get('user_id')
        pasw=request.form.get('password')
        if '@' in user_id:
            user = User.query.filter_by(email=user_id).first()
            if user:
                if user.password==pasw:
                    return redirect(url_for('dashboard',id=user.user_id))
                else:
                    return render_template("error2.html")
            else:
                return render_template("not_found.html")
        else:
            user = User.query.filter_by(user_id=user_id).first()
            if user:
                if user.password==pasw:
                    return redirect(url_for('dashboard',id=user.user_id))
                else:
                    return render_template("error2.html")
            else:
                return render_template("not_found.html")
    else:
        return render_template("error.html")    

@app.route("/staff/login",methods=["GET","POST"])
def staff_lin():
    if request.method=="GET":
        return render_template("staff_lin.html")
    elif request.method=="POST":
        id= request.form.get('staff_id')
        pasw=request.form.get('password')
        if '@' in id:
            user = Staff.query.filter_by(email=id).first()
            if user:
                if user.password==pasw:
                    return redirect(url_for('dashboard',id=user.staff_id))
                else:
                    return render_template("error2.html")
            else:
                return render_template("not_found.html")
        else:
            user = Staff.query.filter_by(staff_id=id).first()
            if user:
                if user.password==pasw:
                    return redirect(url_for('dashboard',id=user.staff_id))
                else:
                    return render_template("error2.html")
            else:
                return render_template("not_found.html")
    else:
        return render_template("error.html")
    
@app.route("/dashboard/<id>",methods=["GET","POST"])
def dashboard(id):
    l,m=[],[]
    if 'U' in id:
        if request.method=="GET":
            user=User.query.filter_by(user_id=id).first()
            trek=Book.query.filter_by(user_id=id).all()
            for i in range(len(trek)):
                l.append(trek[i].__dict__.copy()["trek_id"])
            for j in l:
                m.append(Trek.query.filter_by(trek_id=j).first())
            print(l,m[0].duration)
            return render_template("user.html",name=user.name)
        else:
            pass
    elif 'S' in id:
        return render_template("error.html")
    elif 'D' in id:
        return render_template("error.html")
    else:
        return render_template("error.html")
    
@app.route("/dashboard/delete/<id>",methods=["GET","POST","DELETE"])
def delete(id):

@app.route("/dashboard/details/<id>",methods=["GET","POST"])
def details(id):

@app.route("/dashboard/update/<id>",methods=["GET","POST"])
def update(id):

@app.route("/dashboard/cancel/<id>",methods=["GET","POST"])
def cancel(id):

@app.route("/forget",methods=["GET","POST"])
def forget():                                # Not Completed
    if request.method=="GET":
        return render_template("forg.html")
    elif request.method=="POST":
        pass # work on it
    else:
        return render_template("error.html")

    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

    

import os
from flask import Flask
from application import config
from application.config import LocalDevelopmentConfig
from application.models import db
from flask_security import Security,SQLAlchemySessionUserDatastore,SQLAlchemyUserDatastore
from application.models import User,Role
app=None
def create_app():
    app=Flask(__name__,template_folder="templates")
    if os.getenv('ENV',"development")=="production":
        raise Exception("Currently no production config is setup.")
    else:
        print("Starting Local Development")
        app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    with app.app_context():
        from application import controllers
    #app.app_context().push()
        user_datastore=SQLAlchemySessionUserDatastore(db.session,User,Role)
        security=Security(app,user_datastore)

    return app
app=create_app()

from application.controllers import *
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)'''
import os
from flask import Flask
from application.config import LocalDevelopmentConfig
from application.models import db, User, Role
from flask_security import Security, SQLAlchemyUserDatastore, hash_password

def create_app():
    app = Flask(__name__, template_folder="templates")

    if os.getenv('ENV', "development") == "production":
        raise Exception("Currently no production config is setup.")
    print("Starting Local Development")
    app.config.from_object(LocalDevelopmentConfig)
    db_dir = app.config.get("SQLITE_DB_DIR")
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

    db.init_app(app)

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, user_datastore)

    with app.app_context():
        db.create_all()
        from application import controllers  # noqa: registers routes
    return app
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)