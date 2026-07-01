'''from flask import Flask,redirect,request,render_template,url_for
from flask import current_app as app
from .models import *

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

'''
from flask import redirect, request, render_template, url_for, session
from flask import current_app as app
from flask_security import hash_password, verify_password, login_user, logout_user, auth_required, current_user
from .models import db, User, Staff, Trek, Book
import uuid

@app.route("/trek/add", methods=["GET","POST"])
@auth_required()
def trek_add():
    if request.method == "GET":
        return render_template("trek_add.html")
    elif request.method=="POST":
        name,desc,loc,diff,dur,status,slots = request.form.get('name'),request.form.get('desc'),request.form.get('loc'),request.form.get('diff'),request.form.get('dur'),request.form.get('status'),request.form.get('slots')
        if Trek.query.filter_by(name=name).first():
            return render_template("user_already.html")
        trek_id = "T" + uuid.uuid4().hex[:8]
        new_trek = Trek(
            trek_id=trek_id, name=name,location=loc,difficulty=diff,duration=dur,current_status=status,slots=slots, fs_uniquifier=uuid.uuid4().hex,)
        db.session.add(new_trek)
        db.session.commit()
        return render_template("error.html")
    else:
        return render_template("error.html"), 400

@app.route("/trek/delete/<id>", methods=["GET","POST"])
@auth_required()
def tdelete(id):
    if request.method=="GET":
        return render_template("trek_delete.html",id=id,whc='Trek',url='/trek/delete/',m1='Did u want to delete this trek Permanently : ',m2='Delete Trek Permanently')
    elif request.method=="POST":
        Trek.query.filter_by(trek_id=id).delete()
        db.session.commit()
        return render_template("error.html")
    else:
        return render_template("error.html"), 400
    
@app.route("/trek/update/<id>", methods=["GET","POST"])
@auth_required()
def tupdate(id):
    if request.method=="GET":
        return render_template("update_trek.html",id=id)
    elif request.method=="POST":
        desc,diff,dur,status,slots = request.form.get('desc'),request.form.get('diff'),request.form.get('dur'),request.form.get('status'),request.form.get('slots')
        trek = Trek.query.filter_by(trek_id=id).first()
        trek.description=desc
        trek.difficulty=diff
        trek.duration = dur 
        trek.current_status=status
        trek.slots=slots
        db.session.commit()
        return render_template("error.html")
    else:
        return render_template("error.html"), 400

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        return render_template("signin.html",act='/signin')
    elif request.method=="POST":
        name,mob,mail,passw,gen = request.form.get('name'),request.form.get('mob'),request.form.get('email'),request.form.get('pass'),request.form.get('choice')
        if User.query.filter_by(email=mail).first():
            return render_template("user_already.html",url='/login')
        user_id = "U" + uuid.uuid4().hex[:8]
        new_user = User(
            user_id=user_id, name=name, mobile_no=mob, email=mail,
            password=hash_password(passw), gender=gen,
            active=True, fs_uniquifier=uuid.uuid4().hex,)
        db.session.add(new_user)
        db.session.commit()
        return render_template('welcome.html', id=user_id, mail=mail,url='/login')
    else:
        return render_template("error.html"), 400

@app.route("/staff/signin", methods=["GET", "POST"])
def staff_sin():
    if request.method == "GET":
        return render_template("signin.html",act='/staff/signin')
    elif request.method=="POST":
        name,mob,mail,passw,gen = request.form.get('name'),request.form.get('mob'),request.form.get('email'),request.form.get('pass'),request.form.get('choice')
        if Staff.query.filter_by(email=mail).first():
            return render_template("user_already.html",url='/staff/login')
        staff_id = "S" + uuid.uuid4().hex[:8]
        new_staff = Staff(staff_id=staff_id, name=name, mobile_no=mob, email=mail,password=hash_password(passw), gender=gen,active=True, fs_uniquifier=uuid.uuid4().hex,)
        db.session.add(new_staff)
        db.session.commit()
        return render_template('welcome.html', id=staff_id, mail=mail,url='/staff/login')
    else:
        return render_template("error.html"), 400

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html",act="/login",sign='/signin',forg='/forget')
    elif request.method=="POST":
        user_id = request.form.get('user_id')
        pasw = request.form.get('password')
        user = (User.query.filter_by(email=user_id).first() if '@' in user_id
                else User.query.filter_by(user_id=user_id).first())
        if not user:
             return render_template("not_found.html",url='/signin')
        if not verify_password(pasw, user.password):
                return render_template("error2.html",url1='/login')
        login_user(user)
        return redirect(url_for('dashboard', id=user.user_id ))
    else:
        return render_template("error.html"), 400

@app.route("/staff/login", methods=["GET", "POST"])
def staff_lin():
    if request.method == "GET":
        return render_template("login.html",act="/staff/login",sign='/staff/signin',forg='/forget')
    elif request.method=="POST":
        staff_id = request.form.get('staff_id')
        pasw = request.form.get('password')
        staff = (Staff.query.filter_by(email=staff_id).first() if '@' in staff_id
                else Staff.query.filter_by(staff_id=staff_id).first())
        if not staff:
            return render_template("not_found.html",url='staff/signin')
        if not verify_password(pasw, staff.password):
            return render_template("error2.html",url1='/staff/login')
        login_user(staff)
        return redirect(url_for('dashboard', id=staff.staff_id))
    else:
        return render_template("error.html"), 400
    
@app.route("/delete/<id>", methods=["GET","POST"])
@auth_required()
def delete(id):
    if request.method=="GET":
        return render_template("delete.html",id=id,url='/delete/',whc='Account',m1='Did u want to delete your account Permanently : ',m2='Delete Account Permanently')
    elif request.method=="POST":
        if 'U' in id:
            User.query.filter_by(user_id=id).delete()
            db.session.commit()
        elif 'S' in id:
            staff = Staff.query.filter_by(staff_id=id).delete()
            db.session.commit()
        return redirect(url_for('signin'))
    else:
        return render_template("error.html"), 400

@app.route("/update/<id>", methods=["GET","POST"])
@auth_required()
def update(id):
    if request.method=="GET":
        return render_template("update.html",id=id)
    elif request.method=="POST":
        if 'U' in id:
            name,mob,gen = request.form.get('name'),request.form.get('mob'),request.form.get('choice')
            user=User.query.filter_by(user_id=id).first()
            user.name=name
            user.mobile_no=mob
            user.gender=gen
            db.session.commit()
            return redirect(url_for('login'))
        elif 'S' in id:
            user = Staff.query.filter_by(staff_id=id).first()
            user.name=name
            user.mobile_no=mob
            user.gender=gen
            db.session.commit()
            return redirect(url_for('staff_lin'))
    else:
        return render_template("error.html"), 400

@app.route("/dashboard/<id>", methods=["GET"])
@auth_required()
def dashboard(id):
    # Only allow a logged-in user/staff to view their own dashboard
    current_id = getattr(current_user, 'user_id', None) or getattr(current_user, 'staff_id', None)
    if current_id != id:
        return render_template("error.html"), 403

    if id.startswith('U'):
        user = User.query.filter_by(user_id=id).first()
        if not user:
            return render_template("not_found.html"), 404
        bookings = Book.query.filter_by(user_id=id).all()
        treks = [b.trek for b in bookings]  # uses the relationship, no manual loop-join
        return render_template("user.html", name=user.name, treks=treks ,id=id)
    elif id.startswith('S'):
        user = Staff.query.filter_by(staff_id=id).first()
        if not user:
            return render_template("not_found.html"), 404
        bookings = Book.query.filter_by(staff_id=id).all()
        treks = [b.trek for b in bookings]  # uses the relationship, no manual loop-join
        return render_template("user.html", name=user.name, treks=treks)
    return render_template("error.html")


@app.route("/logout")
@auth_required()
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/forget", methods=["GET", "POST"])
def forget():
    if request.method == "GET":
        return render_template("forg.html")
    # TODO: implement password reset flow
    return render_template("error.html"), 501