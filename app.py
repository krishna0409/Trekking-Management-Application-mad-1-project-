import sqlalchemy, os
from flask import Flask, request, render_template, redirect
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
    trek_id = db.Column(db.String, unique=True, nullable=False)
    user_id = db.Column(db.String, unique=True, nullable=False)
    booked_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String, nullable=False)

class Assignment(db.Model):
    __tablename__='assigned'
    seq_no= db.Column(db.Integer, autoincrement=True, primary_key=True)
    book_id = db.Column(db.String, unique=True, nullable=False)
    user_id = db.Column(db.String, unique=True, nullable=False)
    staff_id = db.Column(db.String, unique=True, nullable=False)
    assigned_date = db.Column(db.Date, nullable=False)

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
        return render_template('welcome.html',id=user__id) 
    else:
        return render_template("error.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="GET":
        return render_template("log_in.html")
    elif request.method=="POST":
        user_id= request.form.get('user_id')
        if '@' in user_id:
            user = User.query.filter_by(email=user_id).first()
            
        else:
            user = User.query.filter_by(user_id=user_id).first()
            return render_template("forg.html")
    else:
        return render_template("error.html")
        

@app.route("/forget",methods=["GET","POST"])
def forget():
    if request.method=="GET":
        return render_template("forg.html")
    else:
        return render_template("user.html")
    
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
        id="U000"+str(total+1)
        new_user = Staff(staff_id=id,name=name,mobile_no=mob,email=mail,password=passw,gender=gen)
        db.session.add(new_user)
        db.session.commit()
        return render_template('welcome.html',id=id) 
    else:
        return render_template("error.html")

@app.route("/staff/login",methods=["GET","POST"])
def staff_lin():
    if request.method=="GET":
        return render_template("staff_lin.html")
    elif request.method=="POST":
        id= request.form.get('staff_id')
        if '@' in id:
            user = User.query.filter_by(email=id).first()
        else:
            user = User.query.filter_by(user_id=id).first()
            return render_template("forg.html")
    else:
        return render_template("error.html")
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
