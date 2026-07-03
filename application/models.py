import uuid
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
db = SQLAlchemy()

role_users = db.Table('role_users',
    db.Column('user_id', db.String(), db.ForeignKey('user.user_id')),
    db.Column('role_id', db.String(), db.ForeignKey('role.id')))

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
    active = db.Column(db.Integer,nullable=False)
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
    active = db.Column(db.Integer,nullable=False)
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False,
                               default=lambda: str(uuid.uuid4()))

class Trek(db.Model):
    __tablename__ = 'trek'
    trek_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, unique=True)
    description = db.Column(db.String , nullable= False)
    difficulty = db.Column(db.String, nullable=False)
    duration = db.Column(db.String, nullable=False)
    current_status = db.Column(db.Integer,nullable=False)
    slots = db.Column(db.Integer, nullable=False)

class Book(db.Model):
    __tablename__ = 'booking'
    book_id = db.Column(db.String, primary_key=True)
    trek_id = db.Column(db.String, db.ForeignKey('trek.trek_id'), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('user.user_id'), nullable=False)
    booked_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Integer,nullable=False)
    no = db.Column(db.Integer,nullable=False)
    trek = db.relationship('Trek', backref='bookings')
    user = db.relationship('User', backref='bookings')

class Assignment(db.Model):
    __tablename__ = 'assigned'
    assig_id = db.Column(db.String, primary_key=True)
    book_id = db.Column(db.String, db.ForeignKey('booking.book_id'), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('user.user_id'), nullable=False)
    staff_id = db.Column(db.String, db.ForeignKey('staff.staff_id'), nullable=False)
    assigned_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Integer,nullable=False)