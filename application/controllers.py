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

u_img='/static/user.png'
timg='/static/img1.png'

today=date.today()
max_date=today+timedelta(days=30)

#Graph for User/Staff/Trek Active/Inactive
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

#Random Assignment Function 
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

# Admin Routes 
@app.route("/signin/admin", methods=["GET", "POST"])
def admin_sin():
    if request.method == "GET":
        return render_template("signin.html",act='/signin/admin',login='/login/admin')
    elif request.method=="POST":
        name,mob,mail,passw,gen = request.form.get('name'),request.form.get('mob'),request.form.get('email'),request.form.get('pass'),request.form.get('choice')
        if Admin.query.filter_by(email=mail,active=1).first():
            return render_template("user_already.html",url='/login/admin',forg='/forget/admin')
        admin_id = "AD" + uuid.uuid4().hex[:8]
        new_staff = Admin(admin_id=admin_id, name=name, mobile_no=mob, email=mail,password=hash_password(passw), gender=gen,active=1, fs_uniquifier=uuid.uuid4().hex,)
        db.session.add(new_staff)
        user_datastore = current_app.extensions['security'].datastore
        user_datastore.add_role_to_user(new_staff, 'Admin')
        db.session.commit()
        db.session.flush()  
        return redirect(url_for('profile',id=admin_id,name=name,type='admin',u_img=u_img))
    return render_template("error.html"), 400

@app.route("/login/admin", methods=["GET", "POST"])
def admin_lin():
    if request.method == "GET":
        return render_template("login.html",act="/login/admin",sign='/signin/admin',forg='/forget/admin')
    elif request.method=="POST":
        staff_id = request.form.get('user_id')
        pasw = request.form.get('password')
        staff = (Admin.query.filter_by(email=staff_id,active=1).first() if '@' in staff_id
                else Admin.query.filter_by(staff_id=staff_id,active=1).first())
        if not staff:
            return render_template("not_found.html",url='/signin/admin')
        if not verify_password(pasw, staff.password):
            return render_template("w_credentials.html",url='/login/admin',forg='/forget/admin')
        login_user(staff)
        return redirect(url_for('profile',id=staff.admin_id,name=staff.name,type='admin',u_img=u_img))
    return render_template("error.html"), 400

@app.route("/signin/staff", methods=["GET", "POST"])
def staff_sin():
    if request.method == "GET":
        return render_template("signin.html",act='/signin/staff',login='/login/staff')
    elif request.method=="POST":
        name,mob,mail,passw,gen = request.form.get('name'),request.form.get('mob'),request.form.get('email'),request.form.get('pass'),request.form.get('choice')
        if Staff.query.filter_by(email=mail,active=1).first():
            return render_template("user_already.html",url='/login/staff',forg='/forget/staff')
        new_staff = Staff_Det(name=name, mobile_no=mob, email=mail,password=passw, gender=gen,status=0,)
        db.session.add(new_staff)
        db.session.commit()
        db.session.flush()
        return render_template('wait.html')
    return render_template("error.html"), 400

@app.route("/login/staff", methods=["GET", "POST"])
def staff_lin():
    if request.method == "GET":
        return render_template("login.html",act="/login/staff",sign='/signin/staff',forg='/forget/staff')
    elif request.method=="POST":
        staff_id = request.form.get('user_id')
        pasw = request.form.get('password')
        staff = (Staff.query.filter_by(email=staff_id).first() if '@' in staff_id
                else Staff.query.filter_by(staff_id=staff_id).first())
        if not staff or staff.active==0 :
            return render_template("not_found.html",url='/signin/staff')
        if not verify_password(pasw, staff.password):
            return render_template("w_credentials.html",url='/login/staff',forg='/forget/staff')
        login_user(staff)
        return redirect(url_for('profile',id=staff.staff_id,name=staff.name,type='staff',u_img=u_img))
    return render_template("error.html"), 400

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        return render_template("signin.html",act='/signin',login='/login')
    elif request.method=="POST":
        name,mob,mail,passw,gen = request.form.get('name'),request.form.get('mob'),request.form.get('email'),request.form.get('pass'),request.form.get('choice')
        if User.query.filter_by(email=mail,active=1).first():
            return render_template("user_already.html",url='/login',forg='/forget/user')
        user_id = "U" + uuid.uuid4().hex[:8]
        new_user = User(user_id=user_id, name=name, mobile_no=mob, email=mail,password=hash_password(passw), gender=gen,active=1, fs_uniquifier=uuid.uuid4().hex,)
        db.session.add(new_user)
        user_datastore = current_app.extensions['security'].datastore
        user_datastore.add_role_to_user(new_user, 'User')
        db.session.commit()
        db.session.flush()  
        return redirect(url_for('profile',id=user_id,name=name,type='user',u_img=u_img))
    return render_template("error.html"), 400
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html",act="/login",sign='/signin',forg='/forget/user')
    elif request.method=="POST":
        user_id = request.form.get('user_id')
        pasw = request.form.get('password')
        user=(User.query.filter_by(email=user_id).first() if '@' in user_id
                else User.query.filter_by(user_id=user_id).first())
        if not user or user.active==0 :
            return render_template("not_found.html",url='/signin')
        if not verify_password(pasw, user.password):
                return render_template("w_credentials.html",url='/login',forg='/forget/user')
        login_user(user)
        return redirect(url_for('profile',id=user.user_id,name=user.name,type='user'))
    return render_template("error.html"), 400

@app.route('/profile/<type>/<id>/<name>')
@login_required
def profile(id,name,type):
    if 'U' in id and type=='user':
        info=User.query.filter_by(user_id=id).first()
        return render_template("profile.html",id=id,name=name,type=type,i=info,u_img=u_img)
    elif 'S' in id and type=='staff':
        info=Staff.query.filter_by(staff_id=id).first()
        return render_template("profile.html",id=id,name=name,type=type,i=info,u_img=u_img)
    elif 'AD' in id:
        info=Admin.query.filter_by(admin_id=id).first()
        return render_template("profile.html",id=id,name=name,type=type,i=info,u_img=u_img)
    else:
        pass
    return render_template("error.html"),404

@app.route("/dashboard/<type>/<id>", methods=["GET"])
@login_required
def dashboard(id,type):
    current_id = getattr(current_user, 'user_id', None) or getattr(current_user, 'staff_id', None) or getattr(current_user, 'admin_id', None)
    if current_id != id:
        return render_template("error.html"), 403
    if id.startswith('U') and type=='user':
        user = User.query.filter_by(user_id=id).first()
        bookings = Book.query.filter(Book.user_id==id).all()#or_(Book.status==0,Book.status==1),
        books = [(b.book_id,b.user_id,b.trek_id,b.status,b.no,b.assigned_yet) for b in bookings]
        l=[]
        for i in books:  
            trekk=Trek.query.filter_by(trek_id=i[2]).first()
            l.append(trekk)
        return render_template("dashboard.html",name=user.name,u_img=u_img,type=type,id=id,list_used=l,book=books,timg=timg)
    elif id.startswith('S') and type=='staff':
        staff = Staff.query.filter_by(staff_id=id).first()
        book=Book.query.filter_by(booked_date=today,status=1,assigned_yet=1).all()
        l=[]
        for i in book:
            trek=Trek.query.filter_by(trek_id=i.trek_id).first()
            assign=Assignment.query.filter_by(book_id=i.book_id,staff_id=id).first()
            if assign:
                user=User.query.filter_by(user_id=assign.user_id).first()
                l.append([user.name,trek.name,i.no])
            else:
                pass
        return render_template("dashboard.html",name=staff.name,id=id,type='staff',u_img=u_img,l=l,dt=today)
    elif id.startswith('AD'):
        admin=Admin.query.filter_by(admin_id=id).first()
        return render_template("dashboard.html",id=id,name=admin.name,user_img=graphmaker('user'),s_img=graphmaker('staff'),t_img=graphmaker('trek'),dt=today,u_img=u_img,type='admin')
    return render_template("error.html"),404

@app.route("/update/<type>/<id>/<name>", methods=["GET","POST"])
@login_required
def update(id,name,type):
    if request.method=="GET":
        return render_template("acc_updation.html",id=id,name=name,type=type,u_img=u_img)
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

@app.route("/delete/<type>/<id>/<name>", methods=["GET","POST"])
@login_required
def delete(id,name,type):
    if request.method=="GET":
        return render_template("acc_deletion.html",name=name,id=id,type=type,u_img=u_img)
    elif request.method=="POST":
        if 'U' in id:
            user=User.query.filter_by(user_id=id).first()
            user.active= 0
        elif 'S' in id:
            staff = Staff.query.filter_by(staff_id=id).first()
            staff.active=0
        elif 'AD' in id:
            staff = Admin.query.filter_by(admin_id=id).first()
            staff.active=0
        db.session.commit()
        return redirect(url_for('signin'))
    return render_template("error.html"), 400

@app.route("/trek/add/<admin>/<name>", methods=["GET","POST"])
@login_required
@admin_required
def trek_add(admin,name):
    if request.method == "GET":
        return render_template("trek.html",title='Add new trek',u_img=u_img,id=admin,type='admin',name=name)
    elif request.method=="POST":
        name,desc,loc,diff,dur,status,slots = request.form.get('name'),request.form.get('desc'),request.form.get('loc'),request.form.get('diff'),request.form.get('dur'),request.form.get('status'),request.form.get('slots')
        if Trek.query.filter_by(name=name).first():
            return render_template("user_already.html")
        trek_id = "T" + uuid.uuid4().hex[:8]
        new_trek = Trek(trek_id=trek_id, name=name,location=loc,description=desc,difficulty=diff,duration=dur,current_status=status,slots=slots)
        db.session.add(new_trek)
        db.session.commit()
        return redirect(url_for('dashboard',id=admin,type='admin'))
    return render_template("error.html")

@app.route("/trek/details/<type>/<admin>/<name>", methods=["GET"])
@login_required
def rtrek(admin,name,type):
    if 'AD' in admin:
        quer=select(Trek)
        users=db.session.scalars(quer).all()
        user=[i for i in users]
        return render_template("trek.html",title='Trek Details',u_img=u_img,id=admin,type=type,name=name,table_used=user)
    elif 'S' in admin:
        trek=Trek.query.filter_by(current_status=1).all()
        return render_template('opened_trek.html',name=name,type=type,id=admin,list_used=trek,u_img=u_img,timg=timg)
    return render_template("error.html"),404

@app.route("/trek/details/<type>/<id>/<name>/<tid>/<tname>", methods=["GET"])
@login_required
@admin_required
def tdetails(id,name,tid,tname,type):
    trekk=Trek.query.filter_by(trek_id=tid).first()
    return render_template('t_details.html',id=id,name=name,type=type,trek=tid,tname=tname,i=trekk,u_img=u_img,timg=timg)

@app.route("/trek/register/<type>/<id>/<name>", methods=["GET"])
@login_required
def trek_register(type,id,name):
    if request.method=="GET":
        if 'U' in id:
            trek=Trek.query.filter_by(current_status=1).all()
            return render_template("register.html",id=id,name=name,timg=timg,u_img=u_img,list_used=trek,type=type)
        else:
            pass  
    return render_template("error.html"), 404

@app.route("/trek/register/<type>/<id>/<name>/<tid>/<tname>", methods=["GET","POST"])
@login_required
def trek_reg(type,id,name,tid,tname):
    if request.method=='GET':
        trek=Trek.query.filter_by(trek_id=tid).first()
        return render_template('tregister.html',type=type,name=name,id=id,i=trek,timg=timg,u_img=u_img,mx=trek.slots,tid=tid,tname=tname,minn=today+timedelta(days=3),maxx=today+timedelta(days=30))
    elif request.method=="POST":
        dt=date.fromisoformat(request.form.get('date'))
        no=request.form.get('slots')
        trek=Trek.query.filter_by(trek_id=tid).first()
        already=Book.query.filter_by(trek_id=tid,booked_date=dt,status=1).all()
        maxx=sum([j.no for j in already])
        if (maxx+int(no)<=trek.slots):
            book_id = "B" + uuid.uuid4().hex[:8]
            new_book = Book(book_id=book_id,trek_id=tid,user_id=id,booked_date=dt,status=1,no=no,assigned_yet=0)
            db.session.add(new_book)
            db.session.commit()
            db.session.flush() 
            return redirect(url_for('dashboard',id=id,type=type))
        else:
            return render_template("sorry.html",id=id,type=type,name=name,trek=trek,slots=(trek.slots-maxx))
    return render_template("error.html"),404

@app.route("/trek/cancel/<type>/<id>/<name>/<tid>/<tname>/<bid>", methods=["GET","POST"])
@login_required
def cancel(type,id,name,tid,tname,bid):
    if request.method=="GET":
        trek=Trek.query.filter_by(trek_id=tid).first()
        bookk=Book.query.filter_by(book_id=bid).first()
        return render_template("cancel.html",id=id,tid=tid,bid=bid,type=type,name=name,u_img=u_img,timg=timg,i=trek,slots=bookk.no,tname=tname)
    elif request.method=="POST":
        book = Book.query.filter_by(trek_id=tid,user_id=id,status=1).first()
        assign=Assignment.query.filter_by(book_id=book.book_id).first()
        if book.assigned_yet==1:
            assign.status=-1
        book.status = -1
        book.assigned_yet= -1
        db.session.commit()
        return redirect(url_for('dashboard',id=id,type=type))
    return render_template("error.html"), 404

@app.route("/trek/book/details/<type>/<id>/<name>/<bid>", methods=["GET","POST"])
@login_required
def book(type,id,name,bid):
    if request.method=='GET':
        bookk = Book.query.filter_by(book_id=bid).first()
        trek=Trek.query.filter_by(trek_id=bookk.trek_id).first()
        bdt=bookk.booked_date>today+timedelta(days=2)
        dt=-1
        if bdt:
            dt=0
        else:
            dt=1
        return render_template("b_details.html",id=id,type=type,name=name,timg=timg,u_img=u_img,i=trek,b=bookk)
    elif request.method=="POST":
        return redirect(url_for('dashboard',id=id,type=type))
    return render_template("error.html"), 404

@app.route("/trek/update/<admin>/<name>/<trekk>", methods=["GET","POST"])
@login_required
@admin_required
def tupdate(admin,trekk,name):
    if request.method=="GET":
        trek = Trek.query.filter_by(trek_id=trekk).first()
        return render_template("trek.html",title='Trek Updation Page',id=admin,name=name,trek=trekk,list_used=trek,type='admin',u_img=u_img)
    elif request.method=="POST":
        desc,diff,dur,status,slots = request.form.get('desc'),request.form.get('diff'),request.form.get('dur'),request.form.get('status'),request.form.get('slots')
        trek = Trek.query.filter_by(trek_id=trekk).first()
        trek.description,trek.difficulty,trek.duration,trek.current_status,trek.slots=desc,diff,dur ,status,slots
        db.session.commit()
        return redirect(url_for('dashboard',id=admin,type='admin'))
    return render_template("error.html"), 400

@app.route("/trek/delete/<admin>/<name>/<trek>/<tname>", methods=["GET","POST"])
@login_required
@admin_required
def tdelete(admin,trek,name,tname):
    if request.method=="GET":
        return render_template("trek.html",title='Trek Deletion',id=admin,name=name,trek=trek,tname=tname,type='admin',u_img=u_img)
    elif request.method=="POST":
        trek=Trek.query.filter_by(trek_id=trek).first()
        trek.current_status = - 1
        db.session.commit()
        return redirect(url_for('dashboard',id=admin,type='admin'))
    return render_template("error.html"), 400

@app.route("/details/user/<type>/<id>/<name>" , methods=["GET"])
@login_required
@admin_required
def show(id,type,name):
    quer=select(User)
    users=db.session.scalars(quer).all()
    user=[i for i in users]
    return render_template("details.html",parameter='user',user=user,id=id,type=type,name=name,u_img=u_img)

@app.route("/details/staff/<type>/<id>/<name>",methods=["GET"])
@login_required
@admin_required
def show1(id,type,name):
    quer=select(Staff)
    users=db.session.scalars(quer).all()
    user=[i for i in users]
    return render_template("details.html",parameter='staff',user=user,id=id,type=type,name=name,u_img=u_img)

@app.route('/booking/details/<type>/<admin>/<name>/<dt>',methods=["GET","POST"])
@login_required
@admin_required
def infor(admin,dt,type,name):
    if request.method=="GET":
        book=Book.query.filter_by(booked_date=dt).all()
        return render_template("booking.html",info='booking',dt=dt,list_used=book,id=admin,minn=today,maxx=max_date,type=type,u_img=u_img,name=name)
    elif request.method=="POST":
        pd=date.fromisoformat(request.form.get('date'))
        book=Book.query.filter_by(booked_date=pd).all()
        return render_template("booking.html",info='booking',dt=pd,list_used=book,id=admin,minn=today,maxx=max_date,type=type,u_img=u_img,name=name)
    return render_template("error.html"),404

@app.route('/booking/assignment/details/<type>/<id>/<name>/<tid>/<tname>/<book>',methods=["GET","POST"])
@login_required
def find(name,id,book,type,tid,tname):
    b=Book.query.filter_by(book_id=book).first()
    t=Trek.query.filter_by(trek_id=tid).first()
    a=Assignment.query.filter_by(book_id=book).first()
    s=Staff.query.filter_by(staff_id=a.staff_id).first()
    return render_template('assign.html',t=t,b=b,s=s,name=name,id=id,type=type,u_img=u_img)

@app.route('/assignment/details/<type>/<admin>/<name>/<dt>',methods=["GET","POST"])
@login_required
@admin_required
def assignment1(admin,dt,type,name):
    if request.method=="GET":
        book=Assignment.query.filter_by(assigned_date=dt).all()
        return render_template("booking.html",info='assignment',dt=dt,list_used=book,id=admin,minn=today,maxx=max_date,type=type,u_img=u_img,name=name)
    elif request.method=="POST":
        pd=date.fromisoformat(request.form.get('date'))
        book=Assignment.query.filter_by(assigned_date=pd).all()
        return render_template("booking.html",info='assignment',dt=pd,list_used=book,id=admin,minn=today,maxx=max_date,type=type,u_img=u_img,name=name)
    return render_template("error.html"),404

@app.route('/booking/assignment/task/<type>/<admin>/<name>/<dt>',methods=["GET","POST"])
@login_required
@admin_required
def details(type,name,admin,dt):
    if request.method=="GET":
        return render_template("task_assig.html",minn=today,maxx=today+timedelta(days=3),id=admin,dt=dt,name=name,type=type,u_img=u_img)
    elif request.method=="POST":
        pd=date.fromisoformat(request.form.get('date'))
        assignment(pd)
        return redirect(url_for('assignment1',admin=admin,dt=pd,type='admin',name=name))
    return render_template("error.html"),404

@app.route('/staff/verify/<type>/<admin>/<name>',methods=["GET","POST"])
@login_required
@admin_required
def verify(admin,type,name):
    if request.method=="GET":
        staff=Staff_Det.query.filter_by(status=0).all()
        return render_template("verify.html",id=admin,name=name,type=type,u_img=u_img,l=staff)
    elif request.method=="POST":
        if 'approve' in request.form:
            email=request.form.get('approve')
            staff=Staff_Det.query.filter_by(email=email).first()
            staff.status=1
            staff_id = "S" + uuid.uuid4().hex[:8]
            new_staff = Staff(staff_id=staff_id, name=staff.name, mobile_no=staff.mobile_no, email=staff.email,password=hash_password(staff.password), gender=staff.gender,active=1,fs_uniquifier=uuid.uuid4().hex,)
            db.session.add(new_staff)
            user_datastore = current_app.extensions['security'].datastore
            user_datastore.add_role_to_user(new_staff, 'Staff')
            db.session.commit()
            db.session.flush() 
            return redirect(url_for('verify',type=type,admin=admin,name=name)) 
        else:
            email=request.form.get('disapprove')
            staff=Staff_Det.query.filter_by(email=email).first()
            staff.status=-1
            db.session.commit()
            return redirect(url_for('verify',type=type,admin=admin,name=name))
    
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login')) 

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

@app.route("/")
def index():
    return redirect(url_for('login'))

@app.route("/forget/<type>", methods=["GET", "POST"])
def forget(type):
    if request.method == "GET":
        if type=='user':
            return render_template("forget.html",forg='/forget/user',login='/login',sign='/signin')
        elif type=='staff':
            return render_template("forget.html",forg='/forget/staff',login='/login/staff',sign='/signin/staff')
        else:
            return render_template("forget.html",forg='/forget/admoin',login='/login/admin',sign='/signin/admin')
    elif request.method=="POST":
        mail = request.form.get('email')
        if type=='user':
           s=User.query.filter_by(email=mail,active=1).first()
           if s:
               return redirect(url_for('forget1',type=type,mail=mail))
           else:
               return render_template("not_found.html",url='/signin')
        elif type=='staff':
            s=Staff.query.filter_by(email=mail,active=1).first()
            if s:
                return redirect(url_for('forget1',type=type,mail=mail))
            else:
               return render_template("not_found.html",url='/signin/staff')
        else:
            s=Admin.query.filter_by(email=mail,active=1).first()
            if s:
               return redirect(url_for('forget1',type=type,mail=mail))
            else:
               return render_template("not_found.html",url='/signin/admin')
    return render_template("error.html"), 404

@app.route("/forget/<type>/<mail>", methods=["GET", "POST"])
def forget1(type,mail):
    if request.method == "GET":
        return render_template('otp.html',mail=mail,type=type)
    if request.method == "POST":
        otp=request.form.get('otp')
        if int(otp)==1234:
            passw = "LcQm#c86"
            if type=='user':
                s=User.query.filter_by(email=mail,active=1).first()
                s.password=hash_password(passw)
                db.session.commit()
                return render_template('wrong.html',title='Success',log='/login',passw=passw,name=s.name)
            elif type=='staff':
                s=Staff.query.filter_by(email=mail,active=1).first()
                s.password=hash_password(passw)
                db.session.commit()
                return render_template('wrong.html',title='Success',log='/login/staff',passw=passw,name=s.name)
            else:
                s=Admin.query.filter_by(email=mail,active=1).first()
                s.password=hash_password(passw)
                db.session.commit()
                return render_template('wrong.html',title='Success',log='/login/admin',passw=passw,name=s.name)
        else:
            return render_template('wrong.html',title='Wrong OTP',type=type)
    return render_template("error.html"), 404