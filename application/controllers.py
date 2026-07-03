from flask import redirect, request, render_template, url_for, session,current_app
from flask import current_app as app
from flask_security import hash_password, verify_password, login_user, logout_user, auth_required, current_user
from .models import db, User, Staff, Trek, Book
import uuid
from datetime import date,timedelta
from sqlalchemy import or_
today=date.today()

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
        db.session.flush()  
        user_datastore = current_app.extensions['security'].datastore
        user_datastore.add_role_to_user(new_user, 'User')
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
        db.session.flush()  
        user_datastore = current_app.extensions['security'].datastore
        user_datastore.add_role_to_user(new_staff, 'Staff')
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
        if user.active==0 or not user:
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
        if staff.active or not staff:
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
            user=User.query.filter_by(user_id=id).first()
            user.active=0
            db.session.commit()
        elif 'S' in id:
            staff = Staff.query.filter_by(staff_id=id).first()
            staff.active=0
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
    current_id = getattr(current_user, 'user_id', None) or getattr(current_user, 'staff_id', None)
    if current_id != id:
        return render_template("error.html"), 403
    if id.startswith('U'):
        user = User.query.filter_by(user_id=id).first()
        if not user:
            return render_template("not_found.html"), 404
        bookings = Book.query.filter(or_(Book.status==0,Book.status==1),Book.user_id==id).all()
        books = [(b.book_id,b.user_id,b.trek_id,b.status,b.no) for b in bookings]
        l=[]
        for i in books:  
            trekk=Trek.query.filter_by(trek_id=i[2]).first()
            l.append(trekk)
        return render_template("user.html",name=user.name,img='/static/img1.png',id=id,list_used=l,book=books)
    elif id.startswith('S'):
        user = Staff.query.filter_by(staff_id=id).first()
        if not user:
            return render_template("not_found.html"), 404
        bookings = Book.query.filter_by(staff_id=id).all()
        treks = [b.trek_id for b in bookings]
        return render_template("user.html", name=user.name, treks=treks)
    return render_template("error.html")

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
            trek_id=trek_id, name=name,location=loc,description=desc,difficulty=diff,duration=dur,current_status=status,slots=slots)
        db.session.add(new_trek)
        db.session.commit()
        return render_template("error.html")
    else:
        return render_template("error.html"), 400

@app.route("/trek/update/<id>", methods=["GET","POST"])
@auth_required()
def tupdate(id):
    if request.method=="GET":
        trek = Trek.query.filter_by(trek_id=id).first()
        return render_template("update_trek.html",id=id,list_used=trek)
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

@app.route("/trek/delete/<id>", methods=["GET","POST"])
@auth_required()
def tdelete(id):
    if request.method=="GET":
        return render_template("trek_delete.html",id=id,whc='Trek',url='/trek/delete/',m1='Did u want to delete this trek Permanently : ',m2='Delete Trek Permanently')
    elif request.method=="POST":
        trek=Trek.query.filter_by(trek_id=id).first()
        trek.current_status=0
        db.session.commit()
        return render_template("error.html")
    else:
        return render_template("error.html"), 400
    
@app.route("/trek/register/<id>",methods=["GET"])
@auth_required()
def trek_register(id):
    if request.method=="GET":
        trek=Trek.query.filter_by(current_status=1).all()
        l=[i for i in trek]
        return render_template("reg_trek.html",id=id,img='/static/img1.png',list_used=l)
    else:
        return render_template("error.html"), 404

@app.route("/trek/register/<id1>/<id2>", methods=["GET","POST"])
@auth_required()
def trek_regis_conf(id1,id2):
    if request.method=="GET":
        trek=Trek.query.filter_by(trek_id=id2).first()
        return render_template("reg_trek_con.html",id=id1,id2=id2,img='/static/img1.png',i=trek,act='/trek/register/',tomm=today+timedelta(days=1),maxx=date(2026,8,1))
    elif request.method=="POST":
        no=request.form.get('slots')
        pd=date.fromisoformat(request.form.get('date'))
        trek=Trek.query.filter_by(trek_id=id2).first()
        already=Book.query.filter_by(trek_id=id2,booked_date=pd,status=1).all()
        maxx=[j.no for j in already]
        if (sum(maxx)+int(no)<=trek.slots):
            book_id = "B" + uuid.uuid4().hex[:8]
            book = Book(book_id=book_id,trek_id=id2,user_id=id1,status=1,no=no,booked_date=pd)
            db.session.add(book)
            db.session.commit()
            return redirect(url_for('dashboard',id=id1))
        else:

            return render_template("slots.html",user=id1,slots=(trek.slots-sum(maxx)))
    else:
        return render_template("error.html"), 404

@app.route("/trek/cancel/<user>/<trekk>", methods=["GET","POST"])
@auth_required()
def trek_cancel(user,trekk):
    if request.method=="GET":
        trek=Trek.query.filter_by(trek_id=trekk).first()
        return render_template("can_trek_con.html",id1=user,id2=trekk,img='/static/img1.png',i=trek,url='/trek/cancel/')
    elif request.method=="POST":
        book = Book.query.filter_by(trek_id=trekk,user_id=user,status=1).first()
        book.status = -1
        db.session.commit()
        return redirect(url_for('dashboard',id=user))
    else:
        return render_template("error.html"), 404

@app.route("/trek/book/<user>/<trekk>/<book>", methods=["GET","POST"])
@auth_required()
def book(user,trekk,book):
    if request.method=='GET':
        trekkk=Trek.query.filter_by(trek_id=trekk).first()
        bookk = Book.query.filter_by(book_id=book).first()
        return render_template("book_details.html",user=user,trek=trekk,book=book,act="/trek/book/",i=trekkk,img='/static/img1.png',b=bookk)
    elif request.method=="POST":
        return redirect(url_for('dashboard',id=user))
    else:
        return render_template("error.html"), 404

@app.route("/forget", methods=["GET", "POST"])
def forget():
    if request.method == "GET":
        return render_template("forg.html")
    # TODO: implement password reset flow
    return render_template("error.html"), 501

@app.route("/logout")
@auth_required()
def logout():
    logout_user()
    return redirect(url_for('login'))
