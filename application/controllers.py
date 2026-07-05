from flask import redirect, request, render_template, url_for, session,current_app
from flask import current_app as app
from flask_security import hash_password, verify_password, login_user, logout_user,roles_required
from flask_login import login_required, current_user
from .models import *
from application.decorators import staff_required, user_required, admin_required
from datetime import date,timedelta
from sqlalchemy import or_
import uuid 

today=date.today()
max_date=date(2026,8,1)

def assignment(dt):
    book=Book.query.filter_by(booked_date=dt,status=1).all()
    staff=Staff.query.filter_by(active=1).all()
    trek=list(set([i.trek_id for i in book]))
    '''for i in trek:
        trek=Trek.query.filter_by(trek_id=i).first()
        already=Book.query.filter_by(trek_id=i,booked_date=dt,status=1).all()
        maxx=sum([j.no for j in already])
        assig_id = "A" + uuid.uuid4().hex[:8]
        while maxx>5:
            assign=Assignment(assig_id=assig_id,)
            db.session.add(assign)
            db.session.commit()
            db.session.flush()'''
    for i in book:
        if i.no>5:
            assig_id = "A" + uuid.uuid4().hex[:8]
            assig=Assignment(assig_id=assig_id,book_id=i.book_id,user_id=i.user_id,staff_id=staff[0].staff_id,assigned_date=dt)
            db.session.add(assign)
            db.session.commit()
            db.session.flush()
            staff.pop(0)

#assignment(date(2026,7,24))

@app.route("/")
def index():
    return redirect(url_for('login'))

@app.route("/admin/signin", methods=["GET", "POST"])
def admin_sin():
    if request.method == "GET":
        return render_template("user.html",title='Sign In',act='/admin/signin')
    elif request.method=="POST":
        name,mob,mail,passw,gen = request.form.get('name'),request.form.get('mob'),request.form.get('email'),request.form.get('pass'),request.form.get('choice')
        if Admin.query.filter_by(email=mail).first():
            return render_template("user_already.html",url='/admin/login')
        admin_id = "AD" + uuid.uuid4().hex[:8]
        new_staff = Admin(admin_id=admin_id, name=name, mobile_no=mob, email=mail,password=hash_password(passw), gender=gen,active=1, fs_uniquifier=uuid.uuid4().hex,)
        db.session.add(new_staff)
        db.session.commit()
        db.session.flush()  
        user_datastore = current_app.extensions['security'].datastore
        user_datastore.add_role_to_user(new_staff, 'Admin')
        db.session.commit()
        return render_template('error2.html.html',title='Welcome',id=admin_id, mail=mail,url='/admin/login')
    return render_template("error.html"), 400

@app.route("/admin/login", methods=["GET", "POST"])
def admin_lin():
    if request.method == "GET":
        return render_template("user.html",title='Login Page',act="/admin/login",sign='/admin/signin',forg='/forget/admin')
    elif request.method=="POST":
        staff_id = request.form.get('user_id')
        pasw = request.form.get('password')
        staff = (Admin.query.filter_by(email=staff_id).first() if '@' in staff_id
                else Admin.query.filter_by(staff_id=staff_id).first())
        if not staff or staff.active==0 :
            return render_template("error2.html",url='/admin/signin',title='Not Found')
        if not verify_password(pasw, staff.password):
            return render_template("error2.html",url='/admin/login',title='Wrong Credentials')
        login_user(staff)
        return redirect(url_for('dashboard', id=staff.admin_id))
    return render_template("error.html"), 400

@app.route("/staff/signin", methods=["GET", "POST"])
def staff_sin():
    if request.method == "GET":
        return render_template("user.html",title='Sign In',act='/staff/signin')
    elif request.method=="POST":
        name,mob,mail,passw,gen = request.form.get('name'),request.form.get('mob'),request.form.get('email'),request.form.get('pass'),request.form.get('choice')
        if Staff.query.filter_by(email=mail).first():
            return render_template("user_already.html",url='/staff/login')
        staff_id = "S" + uuid.uuid4().hex[:8]
        new_staff = Staff(staff_id=staff_id, name=name, mobile_no=mob, email=mail,password=hash_password(passw), gender=gen,active=1, fs_uniquifier=uuid.uuid4().hex,)
        db.session.add(new_staff)
        db.session.commit()
        db.session.flush()  
        user_datastore = current_app.extensions['security'].datastore
        user_datastore.add_role_to_user(new_staff, 'Staff')
        db.session.commit()
        return render_template('error2.html.html',title='Welcome',mail=mail,id=staff_id,url='/staff/login')
    return render_template("error.html"), 400

@app.route("/staff/login", methods=["GET", "POST"])
def staff_lin():
    if request.method == "GET":
        return render_template("user.html",title='Login Page',act="/staff/login",sign='/staff/signin',forg='/forget/staff')
    elif request.method=="POST":
        staff_id = request.form.get('user_id')
        pasw = request.form.get('password')
        staff = (Staff.query.filter_by(email=staff_id).first() if '@' in staff_id
                else Staff.query.filter_by(staff_id=staff_id).first())
        if not staff or staff.active==0 :
            return render_template("error2.html",url='/staff/signin',title='Not Found')
        if not verify_password(pasw, staff.password):
            return render_template("error2.html",url='/staff/login',title='Wrong Credentials')
        login_user(staff)
        return redirect(url_for('dashboard', id=staff.staff_id))
    return render_template("error.html"), 400

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        return render_template("user.html",title='Sign In',act='/signin')
    elif request.method=="POST":
        name,mob,mail,passw,gen = request.form.get('name'),request.form.get('mob'),request.form.get('email'),request.form.get('pass'),request.form.get('choice')
        if User.query.filter_by(email=mail).first():
            return render_template("user_already.html",title='User Already Exist',url='/login')
        user_id = "U" + uuid.uuid4().hex[:8]
        new_user = User(user_id=user_id, name=name, mobile_no=mob, email=mail,password=hash_password(passw), gender=gen,active=1, fs_uniquifier=uuid.uuid4().hex,)
        db.session.add(new_user)
        db.session.commit()
        db.session.flush()  
        user_datastore = current_app.extensions['security'].datastore
        user_datastore.add_role_to_user(new_user, 'User')
        db.session.commit()
        return render_template('error2.html',title='Welcome', id=user_id, mail=mail,url='/login')
    return render_template("error.html"), 400
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("user.html",title='Login Page',act="/login",sign='/signin',forg='/forget/user')
    elif request.method=="POST":
        user_id = request.form.get('user_id')
        pasw = request.form.get('password')
        user = (User.query.filter_by(email=user_id).first() if '@' in user_id
                else User.query.filter_by(user_id=user_id).first())
        if not user or user.active==0 :
            return render_template("error2.html",url='/signin',title='Not Found')
        if not verify_password(pasw, user.password):
                return render_template("error2.html",url='/login',title='Wrong Credentials')
        login_user(user)
        return redirect(url_for('dashboard', id=user.user_id ))
    return render_template("error.html"), 400

@app.route("/forget", methods=["GET", "POST"])
def forget():
    if request.method == "GET":
        return render_template("user.html",title='Forget Password')
    # TODO: implement password reset flow
    return render_template("error.html"), 501

@app.route("/delete/<id>/<name>", methods=["GET","POST"])
@login_required
def delete(id,name):
    if request.method=="GET":
        return render_template("user.html",title='Account Deletion',name=name,id=id,url='/delete/',m1='Did u want to delete your account Permanently : ',m2='Delete Account Permanently')
    elif request.method=="POST":
        if 'U' in id:
            user=User.query.filter_by(user_id=id).first()
            user.active= 0
            db.session.commit()
        elif 'S' in id:
            staff = Staff.query.filter_by(staff_id=id).first()
            staff.active=0
            db.session.commit()
        elif 'AD' in id:
            staff = Admin.query.filter_by(admin_id=id).first()
            staff.active=0
            db.session.commit()
        return redirect(url_for('signin'))
    return render_template("error.html"), 400

@app.route("/update/<id>", methods=["GET","POST"])
@login_required
def update(id):
    if request.method=="GET":
        return render_template("user.html",title='Updation Page',id=id)
    elif request.method=="POST":
        name,mob,gen = request.form.get('name'),request.form.get('mob'),request.form.get('choice')
        if 'U' in id:
            user=User.query.filter_by(user_id=id).first()
            user.name,user.mobile_no,user.gender=name,mob,gen
            db.session.commit()
            return redirect(url_for('login'))
        elif 'S' in id:
            user = Staff.query.filter_by(staff_id=id).first()
            user.name,user.mobile_no,user.gender=name,mob,gen
            db.session.commit()
            return redirect(url_for('staff_lin'))
        elif 'AD' in id:
            user = Admin.query.filter_by(admin_id=id).first()
            user.name,user.mobile_no,user.gender=name,mob,gen
            db.session.commit()
            return redirect(url_for('admin_lin'))
    return render_template("error.html"), 400

@app.route("/trek/add/<admin>", methods=["GET","POST"])
@login_required
@admin_required
def trek_add(admin):
    if request.method == "GET":
        return render_template("trek.html",title='Add new trek')
    elif request.method=="POST":
        name,desc,loc,diff,dur,status,slots = request.form.get('name'),request.form.get('desc'),request.form.get('loc'),request.form.get('diff'),request.form.get('dur'),request.form.get('status'),request.form.get('slots')
        if Trek.query.filter_by(name=name).first():
            return render_template("user_already.html")
        trek_id = "T" + uuid.uuid4().hex[:8]
        new_trek = Trek(trek_id=trek_id, name=name,location=loc,description=desc,difficulty=diff,duration=dur,current_status=status,slots=slots)
        db.session.add(new_trek)
        db.session.commit()
        return redirect(url_for('dashboard',id=admin))
    return render_template("error.html")

@app.route("/trek/update/<admin>/<trek>", methods=["GET","POST"])
@login_required
@admin_required
def tupdate(admin,trek):
    if request.method=="GET":
        trek = Trek.query.filter_by(trek_id=trek).first()
        return render_template("update.html",title='Updation Page',id=trek,list_used=trek)
    elif request.method=="POST":
        desc,diff,dur,status,slots = request.form.get('desc'),request.form.get('diff'),request.form.get('dur'),request.form.get('status'),request.form.get('slots')
        trek = Trek.query.filter_by(trek_id=trek).first()
        trek.description,trek.difficulty,trek.duration,trek.current_status,trek.slots=desc,diff,dur ,status,slots
        db.session.commit()
        return redirect(url_for('dashboard',id=admin))
    return render_template("error.html"), 400

@app.route("/trek/delete/<admin>/<trek>/<name>", methods=["GET","POST"])
@login_required
@admin_required
def tdelete(admin,trek,name):
    if request.method=="GET":
        return render_template("user.html",title='Trek Deletion',name=name,id=trek,admin=admin,url='/trek/delete/',m1='Did u want to delete this trek Permanently : ',m2='Delete Trek Permanently')
    elif request.method=="POST":
        trek=Trek.query.filter_by(trek_id=id).first()
        trek.current_status = -1
        db.session.commit()
        return redirect(url_for('dashboard',id=admin))
    return render_template("error.html"), 400
    
@app.route("/trek/register/<id>/<name>",methods=["GET"])
@login_required
def trek_register(id,name):
    if request.method=="GET":
        trek=Trek.query.filter_by(current_status=1).all()
        l=[i for i in trek]
        return render_template("trek.html",title='Trek Registration',id=id,name=name,img='/static/img1.png',list_used=l)
    return render_template("error.html"), 404

@app.route("/trek/register/<user>/<name>/<trekk>", methods=["GET","POST"])
@login_required
def trek_regis_conf(user,name,trekk):
    if request.method=="GET":
        trek=Trek.query.filter_by(trek_id=trekk).first()
        return render_template("trek.html",title='Registration Confirmation',id=user,id2=trekk,name=name,img='/static/img1.png',i=trek,act='/trek/register/',tomm=today+timedelta(days=2),maxx=max_date)
    elif request.method=="POST":
        no=request.form.get('slots')
        pd=date.fromisoformat(request.form.get('date'))
        trek=Trek.query.filter_by(trek_id=trekk).first()
        already=Book.query.filter_by(trek_id=trekk,booked_date=pd,status=1).all()
        maxx=[j.no for j in already]
        if (sum(maxx)+int(no)<=trek.slots):
            book_id = "B" + uuid.uuid4().hex[:8]
            book = Book(book_id=book_id,trek_id=trekk,user_id=user,status=1,no=no,booked_date=pd)
            db.session.add(book)
            db.session.commit()
            return redirect(url_for('dashboard',id=user))
        else:
            return render_template("user_already.html",title='Slots Information',user=user,slots=(trek.slots-sum(maxx)))
    return render_template("error.html"), 404

@app.route("/trek/cancel/<user>/<trekk>/<book>", methods=["GET","POST"])
@login_required
def trek_cancel(user,trekk,book):
    if request.method=="GET":
        trek=Trek.query.filter_by(trek_id=trekk).first()
        bookk=Book.query.filter_by(book_id=book).first()
        return render_template("trek.html",title='Booking Cancellation',id1=user,id2=trekk,id3=book,img='/static/img1.png',i=trek,url='/trek/cancel/',slots=bookk.no,book_dt=bookk.booked_date)
    elif request.method=="POST":
        book = Book.query.filter_by(trek_id=trekk,user_id=user,status=1).first()
        book.status = -1
        db.session.commit()
        return redirect(url_for('dashboard',id=user))
    return render_template("error.html"), 404

@app.route("/trek/details/<user>/<trekk>/<book>", methods=["GET","POST"])
@login_required
def book(user,trekk,book):
    if request.method=='GET':
        trekkk=Trek.query.filter_by(trek_id=trekk).first()
        bookk = Book.query.filter_by(book_id=book).first()
        return render_template("book.html",user=user,trek=trekk,book=book,act="/trek/details/",i=trekkk,img='/static/img1.png',b=bookk)
    elif request.method=="POST":
        return redirect(url_for('dashboard',id=user))
    return render_template("error.html"), 404

@app.route("/dashboard/<id>", methods=["GET"])
@login_required
def dashboard(id):
    current_id = getattr(current_user, 'user_id', None) or getattr(current_user, 'staff_id', None) or getattr(current_user, 'admin_id', None)
    if current_id != id:
        return render_template("error.html"), 403
    if id.startswith('U'):
        user = User.query.filter_by(user_id=id).first()
        bookings = Book.query.filter(or_(Book.status==0,Book.status==1),Book.user_id==id).all()
        books = [(b.book_id,b.user_id,b.trek_id,b.status,b.no) for b in bookings]
        l=[]
        for i in books:  
            trekk=Trek.query.filter_by(trek_id=i[2]).first()
            l.append(trekk)
        return render_template("dashboard.html",name=user.name,img='/static/img1.png',id=id,list_used=l,book=books)
    elif id.startswith('S'):
        staff = Staff.query.filter_by(staff_id=id).first()
        return render_template("user.html",name=staff.name)
    elif id.startswith('AD'):
        admin=Admin.query.filter_by(admin_id=id)
        return render_template("user.html",name=staff.name)
    return render_template("error.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404