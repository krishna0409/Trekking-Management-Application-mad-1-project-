'''from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
engine=None
Base=declarative_base()
db=SQLAlchemy()


from flask_security import UserMixin,RoleMixin

role_users=db.Table(
    'role_users',
    db.Column('user_id',db.String(),db.ForeignKey('user.user_id')),
    db.Column('role_id',db.String(),db.ForeignKey('role.id'))
)

class Role(db.Model,RoleMixin):
    __tablename__='role'
    id=db.Column(db.String(),primary_key=True)
    name=db.Column(db.String(),unique=True)
    description=db.Column(db.String())

class Staff(db.Model):
    __tablename__='staff'
    staff_id = db.Column(db.String,primary_key=True)
    name = db.Column(db.String, nullable=False)
    mobile_no = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String,nullable=False)
    gender =  db.Column(db.String, nullable=False)

class User(db.Model,UserMixin):
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

class Book(db.Model):
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
    assigned_date = 

class Pass(db.Model):
    __tablename__='password'
    seq_no= db.Column(db.Integer, autoincrement=True, primary_key=True)
    app_user_id = db.Column(db.String, unique=True, nullable=False)
    app_user_type = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    '''

import uuid
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()

role_users = db.Table(
    'role_users',
    db.Column('user_id', db.String(), db.ForeignKey('user.user_id')),
    db.Column('role_id', db.String(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.String(), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(), unique=True)
    description = db.Column(db.String())

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    mobile_no = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String, nullable=False)

    # Required by Flask-Security
    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False,
                               default=lambda: str(uuid.uuid4()))
    roles = db.relationship('Role', secondary=role_users,
                             backref=db.backref('users', lazy='dynamic'))

class Staff(db.Model, UserMixin):
    __tablename__ = 'staff'
    staff_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    mobile_no = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False,
                               default=lambda: str(uuid.uuid4()))

class Trek(db.Model):
    __tablename__ = 'trek'
    trek_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, unique=True)
    difficulty = db.Column(db.String, nullable=False)
    duration = db.Column(db.String, nullable=False)
    current_status = db.Column(db.String, nullable=False)
    slots = db.Column(db.Integer, nullable=False)
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False,
                               default=lambda: str(uuid.uuid4()))

class Book(db.Model):
    __tablename__ = 'booking'
    book_id = db.Column(db.String, primary_key=True)
    trek_id = db.Column(db.String, db.ForeignKey('trek.trek_id'), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('user.user_id'), nullable=False)
    booked_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String, nullable=False)

    trek = db.relationship('Trek', backref='bookings')
    user = db.relationship('User', backref='bookings')

class Assignment(db.Model):
    __tablename__ = 'assigned'
    assig_id = db.Column(db.String, primary_key=True)
    book_id = db.Column(db.String, db.ForeignKey('booking.book_id'), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('user.user_id'), nullable=False)
    staff_id = db.Column(db.String, db.ForeignKey('staff.staff_id'), nullable=False)
    assigned_date = db.Column(db.DateTime, nullable=False)