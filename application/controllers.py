from flask import Flask,redirect,render_template,request
from models import *
app = Flask(__name__)
@app.route("/",methods=["GET"])
def home():
    return render_template("Log_in.html")
if __name__ == '__main__':
    #with app.app_context():
    #    db.create_all()
    app.run(debug=True)
