from datetime import timedelta
from flask import Blueprint, jsonify, request
from main import db
from main import bcrypt
from flask_jwt_extended import create_access_token
from models.user import User
from schemas.user_schema import user_schema


auth = Blueprint('auth', __name__, url_prefix="/auth")

@auth.route("/register", methods=["POST"])
def register_user():
    #get the user details from the request
    user_fields = user_schema.load(request.json)
    #find user by username to check if they are already in the database
    user = User.query.filter_by(username=user_fields["username"]).first()
    if user:
        return {"error": "Username already exists in the database"}

    #find user by email to check if they are already in the database
    user = User.query.filter_by(email=user_fields["email"]).first()
    if user:
        return {"error": "Email already exists in the database"}
    #create user Object
    user = User(
        first_name = user_fields["first_name"],
        last_name = user_fields["last_name"],
        dob = user_fields["dob"],
        mobile = user_fields["mobile"],
        username = user_fields["username"],
        email = user_fields["email"],
        password =  bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")
    )

    #add the user to the database
    db.session.add(user)
    #save the changes in the database
    db.session.commit()
    token = create_access_token(identity=str(user.user_id), expires_delta=timedelta(days=1)) 

    return {"username": user.username, "token": token}

#Login user POST
@auth.route("/login",methods = ["POST"])
def login_user():
    # Get username and password fron the request
    user_fields = user_schema.load(request.json)
    # Check username and password. User needs to exist, and password needs to match
    user = User.query.filter_by(username=user_fields["username"]).first()
    if not user:
        return {"error": "username is not valid"}
    
    if not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return {"error": "wrong password"}
    # Credentials are valid, so generate token and return it to the user
    if user.role_id == 1:
         token = create_access_token(identity="Admin", expires_delta=timedelta(days=1)) 
    else:
        token = create_access_token(identity=str(user.user_id), expires_delta=timedelta(days=1)) 

    return {"username": user.username, "token": token}
