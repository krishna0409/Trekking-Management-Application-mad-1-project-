from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()
class Staff(db.Model):
    __tablename__='staff'
    seq_no= db.Column(db.Integer, autoincrement=True, primary_key=True)
    staff_id = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    mobile_no = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, unique=True)
    status =  db.Column(db.String, nullable=False)
    gender =  db.Column(db.String, nullable=False)

class User(db.Model):
    __tablename__='user'
    seq_no= db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    mobile_no = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, unique=True)
    gender =  db.Column(db.String, nullable=False)

class Trek(db.Model):
    __tablename__='trek'
    seq_no= db.Column(db.Integer, autoincrement=True, primary_key=True)
    trek_id = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, unique=True)
    difficulty =  db.Column(db.String, nullable=False)
    duration =  db.Column(db.String, nullable=False)
    current_status =  db.Column(db.String, nullable=False)

'''class Book(db.Model):
    __tablename__='booking'
    seq_no= db.Column(db.Integer, autoincrement=True, primary_key=True)
    book_id = db.Column(db.String, unique=True, nullable=False)
    trek_id = 
    user_id = 
    booked_date = 
    status = 

class Assignment(db.Model):
    __tablename__='assigned'
    seq_no= db.Column(db.Integer, autoincrement=True, primary_key=True)
    book_id = 
    user_id = 
    staff_id = 
    assigned_date = '''

class Pass(db.Model):
    __tablename__='password'
    seq_no= db.Column(db.Integer, autoincrement=True, primary_key=True)
    app_user_id = db.Column(db.String, unique=True, nullable=False)
    app_user_type = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)