from flask import Flask,render_template,request,session,redirect,url_for,flash,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import null
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
import json

# MY db connection
local_server= True
app = Flask(__name__, template_folder="templates")
app.secret_key='kusumachandashwini'

# TO DO:
app.config['SQLALCHEMY_DATABASE_URI']='mysql://Alex:CloudComp10!@db-app/restaurant'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))
    rollno=db.Column(db.String(50))

class Client(db.Model):
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    cname=db.Column(db.String(50))
    email=db.Column(db.String(50))
    password=db.Column(db.String(1000))

class Ospatar(db.Model):
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    oname=db.Column(db.String(50))
    email=db.Column(db.String(50))
    password=db.Column(db.String(1000))

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100)) # image path

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)  # Se presupune că acesta este id-ul clientului
    product_name = db.Column(db.String(100), nullable=False)  # Numele produsului
    quantity = db.Column(db.Integer, nullable=False)

@app.route('/place_order', methods=['POST'])
def place_order():
    data = request.get_json()

    if not data:
        return jsonify({'message': 'Nu au fost trimise date.'}), 400

    for item in data:
        user_id = item.get('user_id')
        user_name = item.get('user_name')
        product_name = item.get('product_name')
        quantity = item.get('quantity')

        if user_id is None or user_name is None or product_name is None or quantity is None:
            return jsonify({'message': 'Lipsește una sau mai multe valori.'}), 400

        orders = Orders(user_id=user_id, user_name=user_name, product_name=product_name, quantity=quantity)
        db.session.add(orders)

    db.session.commit()

    return jsonify({'message': 'Comanda a fost plasată cu succes.'})

@app.route('/addmenu', methods=['POST', 'GET'])
def addmenu():
    if request.method == "POST":
        name=request.form.get('name')
        description=request.form.get('description')
        price=request.form.get('price')
        image = request.form.get('image')

        new_menu = Menu(name=name, description=description, price=price, image=image)
        db.session.add(new_menu)
        db.session.commit()
        flash("Menu added successfully", "info")
    return render_template('addmenu.html')


@app.route('/addclient',methods=['POST','GET'])
def addclient():
    if request.method=="POST":
        cname=request.form.get('cname')
        email=request.form.get('email')
        password=request.form.get('password')
        rollno = "client"
        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist","warning")
        else:
            encpassword=generate_password_hash(password)
            new_user = User(username=cname, email=email, password=encpassword, rollno=rollno)
            db.session.add(new_user)

            new_client = Client(cname=cname, email=email, password=encpassword)
            db.session.add(new_client)

            db.session.commit()
            flash("User added successfully","info")
    return render_template('addclient.html')


@app.route('/addospatar',methods=['POST','GET'])
def addospatar():
    if request.method=="POST":
        oname=request.form.get('oname')
        email=request.form.get('email')
        password=request.form.get('password')
        rollno = "ospatar"
        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist","warning")
        else:
            encpassword=generate_password_hash(password)
            new_user = User(username=oname, email=email, password=encpassword, rollno=rollno)
            db.session.add(new_user)

            new_ospatar = Ospatar(oname=oname, email=email, password=encpassword)
            db.session.add(new_ospatar)

            db.session.commit()
            flash("User added successfully","info")
    return render_template('addospatar.html')

@app.route("/deleteospatar/<string:email>",methods=['POST','GET'])
def deleteospatar(email):
    ospatar = Ospatar.query.filter_by(email=email).first()
    user = User.query.filter_by(email=email).first()
    
    if ospatar is not None:
        db.session.delete(ospatar)
    
    if user is not None:
        db.session.delete(user)
    
    db.session.commit()
    flash("Slot Deleted Successful","danger")
    return redirect('/ospataridetails')

@app.route("/deleteclient/<string:email>",methods=['POST','GET'])
def deleteclient(email):
    client = Client.query.filter_by(email=email).first()
    user = User.query.filter_by(email=email).first()
    
    if client is not None:
        client_name = client.cname
        orders = Orders.query.filter_by(user_name=client_name).all()
        for order in orders:
            db.session.delete(order)
        db.session.delete(client)
    
    if user is not None:
        db.session.delete(user)
    
    db.session.commit()
    flash("Slot Deleted Successful","danger")
    return redirect('/clientidetails')

@app.route("/deleteproduct/<string:id>",methods=['POST','GET'])
def deleteproduct(id):
    product = Menu.query.filter_by(id=id).first()
    if product is not None:
        productName = product.name
        orders = Orders.query.filter_by(product_name=productName).all()
        for order in orders:
            db.session.delete(order)
        db.session.delete(product)
    
    db.session.commit()
    flash("Slot Deleted Successful","danger")
    return redirect('/menu')

@app.route("/deletecomanda/<string:id>",methods=['POST','GET'])
def deletecomanda(id):
    order = Orders.query.filter_by(id=id).first()
    if order is not None:
        db.session.delete(order)
    
    db.session.commit()
    flash("Slot Deleted Successful","danger")
    return redirect('/comenzi')

@app.route('/clientidetails')
def clientidetails():
    query=Client.query.all() 
    return render_template('clientidetails.html',query=query)

@app.route('/ospataridetails')
def ospataridetails():    
    query=Ospatar.query.all() 
    return render_template('ospataridetails.html',query=query)

@app.route('/comenzi')
def comenzi():    
    query=Orders.query.all() 
    return render_template('comenzi.html',query=query)

app.run(host='0.0.0.0', debug=True, port=5001)    
