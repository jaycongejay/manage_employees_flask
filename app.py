from flask import Flask, render_template, request, make_response, redirect, url_for, flash, jsonify

# import bcrypt
from flask_bcrypt import Bcrypt  # For Python3

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from dotenv import load_dotenv
load_dotenv()

import os

from flask_jwt_extended import (
    JWTManager, jwt_required, jwt_optional, create_access_token,
    get_jwt_identity, get_raw_jwt, set_access_cookies, unset_jwt_cookies
)

######################################################################

app = Flask(__name__)
dev_uri = os.getenv('DEV_DATABASE_URI')
bcrypt = Bcrypt(app)
app.secret_key = os.getenv('SECRET_KEY')


ENV = 'proc'    # dev or prod

if ENV == 'dev':
    app.debug = True  # Dev mode
    app.config['SQLALCHEMY_DATABASE_URI'] = dev_uri
else:
    app.debug = False  # Production mode
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://atvjkeuggwajyb:1047e2ec0cb8f37bc90826535c4a1a648506867275f1864d06a46c17c03a3f70@ec2-52-86-116-94.compute-1.amazonaws.com:5432/d5sibnhlmor0b6'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_HEADER_TYPE'] = None

db = SQLAlchemy(app)


# Create Data Model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    hash = db.Column(db.Text, nullable=False)

    def __init__(self, email, hash):
        self.email = email
        self.hash = hash

        

# Setup the Flask-JWT-Extended extension
key = os.getenv('JWT_SECRET_KEY')
app.config['JWT_SECRET_KEY'] = key  
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
jwt = JWTManager(app)
        




# Routes
@app.route('/register', methods=['POST'])
def register():
    try:
        ########### TEST #############################
        # from Postman POST REQUEST
        # email = request.json.get('email', None)   
        # password = request.json.get('password', None)

        # if not email:
        #     return 'Missing email', 400
        # if not password:
        #     return 'Missing password', 400
        ########### TEST end #############################

        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

        # Encrypt password
        hashedPassword = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(email=email, hash=hashedPassword)

        # Add to DB
        db.session.add(user)
        db.session.commit()

        # JWT
        access_token = create_access_token(identity={"email": email})

        return redirect(url_for('home'))

    except IntegrityError:
        db.session.rollback()
        return render_template('userAlreadyExist.html')
    except AttributeError:
        return 'Provide an Email and Password in JSON format in the request body', 400 

@app.route('/logIn')
def login():
    return render_template('login.html')

@app.route('/logOut')
def logout():
    resp = jsonify({'logout': True})
    resp = make_response(redirect(url_for('home')))
    unset_jwt_cookies(resp)
    return resp


@app.route('/signUp')
def signUp():
    return render_template('signUp.html')


@app.route('/auth', methods=['POST'])
def auth():
    try:
        ####### TEST ###################################
            # email = request.json.get('email', None) # if there is no email, get None
            # password = request.json.get('password', None)

            # user = User.query.filter_by(email=email).first()

            # if bcrypt.checkpw(password.encode('utf-8'), user.hash.encode('utf-8')):
            #         access_token = create_access_token(identity={"email": email})
            #         return {"access_token": access_token}, 200
            # else:
            #     return 'The user NOT FOUND', 200

            # if not email:
            #     return 'Missing email', 400
            # if not password:
            #     return 'Missing password', 400
        ######## TEST end ###############################

        if request.method == 'POST':
            email = request.form['email'] # Data from login form
            password = request.form['password'] # Data from login form

            # Search by email from DB
            user = User.query.filter_by(email=email).first()

            if not user:
                return render_template('userNotExist.html'), 404

            if bcrypt.check_password_hash(user.hash, password):

                access_token = create_access_token(identity={"email": email})
                
                resp = make_response(redirect(url_for('home')))
                set_access_cookies(resp, access_token)

                return resp
            else:
                return redirect(url_for('login'))

            return render_template("home.html") 

    except AttributeError:
        return 'Provide an Email and Password in JSON format in the request body', 400

####### TEST ###################################
# Protect route using JWT
# @app.route('/test', methods =['GET'])
# @jwt_optional
# def test():
#     current_user = get_jwt_identity()
#     if current_user:
#         return jsonify(logged_in_as=current_user), 200
#     else:
#         return jsonify(logged_in_as='invalid user'), 200
######## TEST end ###############################



@app.route('/')
@jwt_optional
def home():
    user = get_jwt_identity()
    if user:
        isUserLoggedIn = True
        return render_template("home.html", isUserLoggedIn=isUserLoggedIn, username=user['email'])
    else:
        isUserLoggedIn = False
        return render_template("home.html", isUserLoggedIn=isUserLoggedIn)

@jwt.expired_token_loader
def my_expired_token():
    isUserLoggedIn = False
    return render_template("home.html", isUserLoggedIn=isUserLoggedIn)

@app.route('/employees', methods=['GET'])
@jwt_optional
def employees():
    user = get_jwt_identity() # Check if a token exist

    if user:
        all_data = Employee.query.all() # Retreive all data from DB
        return render_template("index.html", employees=all_data)
    else:
        return redirect(url_for('login'))
    


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        my_data = Employee(name=name, email=email, phone=phone)
        db.session.add(my_data) # Create
        db.session.commit()

        flash("Employee added successfully!!")

        return redirect(url_for('employees'))

@app.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
            my_data = Employee.query.get(request.form['id']) # get data by id from DB

            my_data.name = request.form['name']     # Set data from the form to the name of the id
            my_data.email = request.form['email']
            my_data.phone = request.form['phone']

            db.session.commit()  # Update

            flash("Employee updated successfully")

            return redirect(url_for('employees'))

@app.route('/delete/<id>', methods = ['GET', 'POST'])
def delete(id):
    my_data = Employee.query.get(id)
    db.session.delete(my_data)  # Delete
    db.session.commit()
    flash("Employee deleted successfully")

    return redirect(url_for('employees'))







# Run server
if __name__ == "__main__":
    app.run()  # debug=false for publish mode