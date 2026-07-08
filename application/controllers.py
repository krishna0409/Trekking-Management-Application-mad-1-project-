from flask import redirect, request, render_template, url_for, session,current_app
from flask import current_app as app
from flask_security import hash_password, verify_password, login_user, logout_user,roles_required
from flask_login import login_required, current_user
from .models import *
from application.decorators import staff_required, user_required, admin_required
from datetime import date,timedelta
from sqlalchemy import or_,select
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import uuid 

today=date.today()
max_date=today+timedelta(days=30)

def assignment(dt):
    b=Book.query.filter_by(booked_date=dt,status=1,assigned_yet=0).all()
    s=Staff.query.filter_by(active=1).all()
    d1,d2=dict(),dict()
    for i in s:
        d1[i],d2[i]=0,[]
    for j in b:
        if j.no>=5:
            for k in d1:
                if d1[k]==0:
                    d1[k]=j.no
                    d2[k].append(j.book_id)
                    j.assigned_yet=1
                    db.session.commit()
                    db.session.flush()
                    break
        else:
            for k in d1:
                if d1[k]<=(5-j.no):
                    d1[k]+=j.no
                    d2[k].append(j.book_id)
                    j.assigned_yet=1
                    db.session.commit()
                    db.session.flush()
                    break
    for id in d2:
        if len(d2[id])==0:
            pass
        elif len(d2[id])==1:
            assig_id = "ASG" + uuid.uuid4().hex[:8]
            book=Book.query.filter_by(book_id=d2[id][0]).first()
            assig=Assignment(assig_id=assig_id,book_id=book.book_id,user_id=book.user_id,staff_id=id.staff_id,assigned_date=book.booked_date,status=1)
            db.session.add(assig)
            db.session.commit()
        else:
            assig_id = "ASG" + uuid.uuid4().hex[:8]
            for n in d2[id]:
                book=Book.query.filter_by(book_id=n).first()
                assig=Assignment(assig_id=assig_id,book_id=book.book_id,user_id=book.user_id,staff_id=id.staff_id,assigned_date=book.booked_date,status=1)
                db.session.add(assig)
                db.session.commit()
                db.session.flush()

assignment(date(2026,7,10))
def graphmaker(l):   
    if l=='user':
        quer=select(User)
        users=db.session.scalars(quer).all()
        user=[i.active for i in users]
        data=[0]*user.count(0) + [1]*user.count(1)
        add=r"static/users.png"
        plt.hist(data,bins=[-0.5,0.5,1.5],rwidth=0.8,color='lightyellow',edgecolor='black')
        plt.title('Users data')
        plt.xlabel('1: Active 0: Deleted')
        plt.ylabel('No. of users')
        plt.xticks([0,1])
        plt.grid(axis='y',linestyle='--',alpha=0.7)
        plt.savefig(add)
        plt.clf()
    elif l=='staff':
        query=select(Staff)
        staf=db.session.scalars(query).all()
        staff=[i.active for i in staf]
        data=[0]*staff.count(0) + [1]*staff.count(1)
        add=r"static/staff.png"
        plt.hist(data,bins=[-0.5,0.5,1.5],rwidth=0.8,color='lightyellow',edgecolor='black')
        plt.title('Staff data')
        plt.xlabel('1: Active 0: Deleted')
        plt.ylabel('No. of working Members')
        plt.xticks([0,1])
        plt.grid(axis='y',linestyle='--',alpha=0.7)
        plt.savefig(add)
        plt.clf()
    else:
        que=select(Trek)
        trekk=db.session.scalars(que).all()
        trek=[i.current_status for i in trekk]
        data=[0]*trek.count(0) + [1]*trek.count(1) + [-1]*trek.count(-1)
        plt.hist(data,bins=[-1.5,-0.5,0.5,1.5],rwidth=0.8,color='lightyellow',edgecolor='black')
        plt.title('Trek Active data')
        plt.xlabel('1: Active 0: Inactive -1: Deleted')
        plt.ylabel('No. of Treks')
        plt.xticks([-1,0,1])
        plt.grid(axis='y',linestyle='--',alpha=0.7)
        add=r"static/trek.png"
        plt.savefig(add)
        plt.clf()
    return add
        
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
            return render_template("user_already.html",url='/admin/login',title='User Already Exist')
        admin_id = "AD" + uuid.uuid4().hex[:8]
        new_staff = Admin(admin_id=admin_id, name=name, mobile_no=mob, email=mail,password=hash_password(passw), gender=gen,active=1, fs_uniquifier=uuid.uuid4().hex,)
        db.session.add(new_staff)
        db.session.commit()
        db.session.flush()  
        user_datastore = current_app.extensions['security'].datastore
        user_datastore.add_role_to_user(new_staff, 'Admin')
        db.session.commit()
        return render_template('error2.html',title='Welcome',id=admin_id, mail=mail,url='/admin/login')
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
        return redirect(url_for('profile',id=staff.admin_id,aid='admin',name=staff.name,user='admin'))
    return render_template("error.html"), 400

@app.route("/staff/signin", methods=["GET", "POST"])
def staff_sin():
    if request.method == "GET":
        return render_template("user.html",title='Sign In',act='/staff/signin')
    elif request.method=="POST":
        name,mob,mail,passw,gen = request.form.get('name'),request.form.get('mob'),request.form.get('email'),request.form.get('pass'),request.form.get('choice')
        if Staff.query.filter_by(email=mail).first():
            return render_template("user_already.html",url='/staff/login',title='User Already Exist')
        staff_id = "S" + uuid.uuid4().hex[:8]
        new_staff = Staff(staff_id=staff_id, name=name, mobile_no=mob, email=mail,password=hash_password(passw), gender=gen,active=1, fs_uniquifier=uuid.uuid4().hex,)
        db.session.add(new_staff)
        db.session.commit()
        db.session.flush()  
        user_datastore = current_app.extensions['security'].datastore
        user_datastore.add_role_to_user(new_staff, 'Staff')
        db.session.commit()
        return render_template('error2.html',title='Welcome',mail=mail,id=staff_id,url='/staff/login')
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
        return redirect(url_for('profile',id=staff.staff_id,aid=staff.staff_id,name=staff.name,user='staff'))
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
        return redirect(url_for('profile',id=user.user_id,aid=user.user_id,name=user.name,user='user'))
    return render_template("error.html"), 400

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

@app.route("/update/<id>/<name>", methods=["GET","POST"])
@login_required
def update(id,name):
    if request.method=="GET":
        return render_template("user.html",title='Updation Page',id=id,name=name)
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

@app.route("/forget", methods=["GET", "POST"])
def forget():
    if request.method == "GET":
        return render_template("user.html",title='Forget Password')
    # TODO: implement password reset flow
    return render_template("error.html"), 501

@app.route("/trek/add/<admin>", methods=["GET","POST"])
@login_required
@admin_required
def trek_add(admin):
    if request.method == "GET":
        return render_template("trek.html",title='Add new trek',admin=admin)
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

@app.route("/trek/update/<admin>/<trekk>/<name>", methods=["GET","POST"])
@login_required
@admin_required
def tupdate(admin,trekk,name):
    if request.method=="GET":
        trek = Trek.query.filter_by(trek_id=trekk).first()
        return render_template("trek.html",title='Updation Page',id=trekk,admin=admin,list_used=trek,name=name)
    elif request.method=="POST":
        desc,diff,dur,status,slots = request.form.get('desc'),request.form.get('diff'),request.form.get('dur'),request.form.get('status'),request.form.get('slots')
        trek = Trek.query.filter_by(trek_id=trekk).first()
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
        trek=Trek.query.filter_by(trek_id=trek).first()
        trek.current_status = -1
        db.session.commit()
        return redirect(url_for('dashboard',id=admin))
    return render_template("error.html"), 400
    
@app.route("/trek/register/<id>/<name>",methods=["GET"])
@login_required
def trek_register(id,name):
    if request.method=="GET":
        if 'AD' in id:
            que=select(Trek)
            trekk=db.session.scalars(que).all()
            trek=[i for i in trekk]
            return render_template("trek.html",title='Trek Registration',id=id,name=name,img='/static/img1.png',list_used=trek)
        else:
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
            book = Book(book_id=book_id,trek_id=trekk,user_id=user,status=1,no=no,booked_date=pd,assigned_yet=0)
            db.session.add(book)
            db.session.commit()
            return redirect(url_for('dashboard',id=user))
        else:
            return render_template("user_already.html",title='Slots Information',user=user,name=name,trek=trekk,slots=(trek.slots-sum(maxx)))
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
        book.assigned_yet= -1
        if book.booked_date>today+timedelta(days=1):
            pass
        else:
            assign=Assignment.query.filter_by(book_id=book.book_id).first()
            assign.status=-1
        db.session.commit()
        return redirect(url_for('dashboard',id=user))
    return render_template("error.html"), 404

@app.route("/trek/details/<user>/<trekk>/<book>", methods=["GET","POST"])
@login_required
def book(user,trekk,book):
    if request.method=='GET':
        trekkk=Trek.query.filter_by(trek_id=trekk).first()
        bookk = Book.query.filter_by(book_id=book).first()
        bdt=bookk.booked_date>today+timedelta(days=2)
        dt=-1
        if bdt:
            dt=0
        else:
            dt=1
        name=User.query.filter_by(user_id=user).first()
        return render_template("book.html",user=user,trek=trekk,book=book,act="/trek/details/",i=trekkk,img='/static/img1.png',b=bookk,name=name.name,t_name=trekkk.name,st=dt)
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
        bookings = Book.query.filter(Book.user_id==id).all()#or_(Book.status==0,Book.status==1),
        books = [(b.book_id,b.user_id,b.trek_id,b.status,b.no) for b in bookings]
        l=[]
        for i in books:  
            trekk=Trek.query.filter_by(trek_id=i[2]).first()
            l.append(trekk)
        return render_template("dashboard.html",name=user.name,img='/static/img1.png',id=id,list_used=l,book=books)
    elif id.startswith('S'):
        staff = Staff.query.filter_by(staff_id=id).first()
        return render_template("dashboard.html",name=staff.name,id=id)
    elif id.startswith('AD'):
        admin=Admin.query.filter_by(admin_id=id).first()
        return render_template("dashboard.html",id=id,name=admin.name,u_img=graphmaker('user'),s_img=graphmaker('staff'),t_img=graphmaker('trek'),dt=today)
    return render_template("error.html")

@app.route("/admin/details/user/<id>" , methods=["GET"])
@login_required
@admin_required
def show(id):
    quer=select(User)
    users=db.session.scalars(quer).all()
    user=[i for i in users]
    return render_template("admin.html",parameter='user',user=user,id=id)

@app.route("/admin/details/staff/<id>" , methods=["GET"])
@login_required
@admin_required
def show1(id):
    quer=select(Staff)
    users=db.session.scalars(quer).all()
    user=[i for i in users]
    return render_template("admin.html",parameter='staff',user=user,id=id)

@app.route('/profile/<user>/<id>/<name>/<aid>')
@login_required
def profile(user,id,name,aid):
    if 'U' in aid or ('AD' in aid and 'U' in id):
        info=User.query.filter_by(user_id=id).first()
        return render_template("profile.html",id=id,name=name,aid=aid,i=info)
    elif 'S' in aid or ('AD' in aid and 'S' in id):
        info=Staff.query.filter_by(staff_id=id).first()
        return render_template("profile.html",id=id,name=name,aid=aid,i=info)
    elif 'AD' in id:
        info=Admin.query.filter_by(admin_id=id).first()
        return render_template("profile.html",id=id,name=name,aid=aid,i=info)
    return render_template("error.html"),404

@app.route('/booking/<admin>/<dt>',methods=["GET","POST"])
@login_required
@admin_required
def infor(admin,dt):
    if request.method=="GET":
        book=Book.query.filter_by(booked_date=dt).all()
        return render_template("booking.html",info='booking',dt=dt,list_used=book,id=admin,minn=today,maxx=max_date)
    elif request.method=="POST":
        pd=date.fromisoformat(request.form.get('date'))
        book=Book.query.filter_by(booked_date=pd).all()
        return render_template("booking.html",info='booking',dt=pd,list_used=book,id=admin,minn=today,maxx=max_date)
    return render_template("error.html"),404

@app.route('/booking/assignment/<admin>/<dt>',methods=["GET","POST"])
@login_required
@admin_required
def assignment1(admin,dt):
    if request.method=="GET":
        book=Assignment.query.filter_by(assigned_date=dt).all()
        return render_template("booking.html",info='assignment',dt=dt,list_used=book,id=admin,minn=today,maxx=today+timedelta(days=30))
    elif request.method=="POST":
        pd=date.fromisoformat(request.form.get('date'))
        book=Assignment.query.filter_by(assigned_date=pd).all()
        return render_template("booking.html",info='assignment',dt=pd,list_used=book,id=admin,minn=today,maxx=today+timedelta(days=30))
    return render_template("error.html"),404

@app.route('/booking/assignment/<user>/<name>/<book>',methods=["GET","POST"])
@login_required
def find(name,user,book):
    b=Book.query.filter_by(book_id=book).first()
    t=Trek.query.filter_by(trek_id=b.trek_id).first()
    a=Assignment.query.filter_by(book_id=b.book_id).first()
    s=Staff.query.filter_by(staff_id=a.staff_id).first()
    return render_template('booking.html',info='assignment',name=name,t=t,b=b,s=s,id=user)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404