from flask import Flask,render_template,request,session,redirect,url_for,flash,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import null
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
from flask_cors import CORS 
import json

app = Flask(__name__, template_folder='templates')
app.secret_key='kusumachandashwini'

# enable cors
CORS(app)

# this is for getting unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# TO DO:
app.config['SQLALCHEMY_DATABASE_URI']='mysql://Alex:CloudComp10!@localhost/restaurant'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))
    rollno=db.Column(db.String(50))

class Ospatar(db.Model):
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    oname=db.Column(db.String(50))
    email=db.Column(db.String(50))
    password=db.Column(db.String(1000))

class Client(db.Model):
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    cname=db.Column(db.String(50))
    email=db.Column(db.String(50))
    password=db.Column(db.String(1000))

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100)) # image path

@app.route('/')
def firstPage():
    return render_template('firstpage.html')

# @app.route('/menu')
# def menu():
    # todo


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/administrator')
@login_required
def administrator():
    return render_template('administrator.html')

@app.route('/client')
@login_required
def client():
    return render_template('client.html')  

@app.route('/ospatar')
@login_required
def ospatar():
    return render_template('ospatar.html')  

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        encpassword=generate_password_hash(password)

        if user and check_password_hash(user.password,password):
            global loggedUserName
            loggedUserName = user.username
            global loggedUserRoll
            loggedUserRoll = user.rollno
            login_user(user)
            # flash("Login Success","primary")
            if user.rollno == "admin":
                return redirect(url_for('administrator'))
            elif user.rollno == "client":
                return redirect(url_for('client'))
            elif user.rollno == "ospatar":
                return redirect(url_for('ospatar'))
            
        else:
            flash("invalid credentials","danger")
            return render_template('login.html')    

    return render_template('login.html')

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == "POST":
        cname=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        rollno = "client"
        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist","warning")
            return render_template('/signup.html')
        else:
            encpassword=generate_password_hash(password)
            new_user = User(username=cname, email=email, password=encpassword, rollno=rollno)
            db.session.add(new_user)

            new_client = Client(cname=cname, email=email, password=encpassword)
            db.session.add(new_client)

            db.session.commit()
        flash("Signup Succes Please Login","success")
        return render_template('login.html')

          

    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    # session.pop('_flashes', None)
    # flash("Logout SuccessFul","primary")
    return redirect(url_for('login'))

app.run(debug=True, port=5000)
