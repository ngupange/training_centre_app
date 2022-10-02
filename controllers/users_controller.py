from queue import Empty
from flask import Blueprint, jsonify, request
from main import db
from models.user import User
from schemas.user_schema import user_schema, users_schema
from main import bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity

users = Blueprint('users', __name__, url_prefix="/users")

# To access this User routes you need to be System Admin


@users.route("/", methods=["GET"])
@jwt_required()
def get_user():
    if get_jwt_identity() != "Admin":
        return {"error": "You don't have the right credentials to see this. SORRY!"}, 401
    users_list = User.query.all()
    result = users_schema.dump(users_list)
    return jsonify(result)


@users.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_single_user(id):
    if get_jwt_identity() != "Admin":
        return {"error": "You don't have the right credentials to see this. SORRY!"}, 401
    reg_user = User.query.get(id)
    if not reg_user:
        return {"error": "User id not found"}
    result = user_schema.dump(reg_user)
    return jsonify(result)

#Admin is the user who can view these endpoints

@users.route("/pending", methods=["GET"])
@jwt_required()
def get_pending_user():
    if get_jwt_identity() != "Admin":
        return {"error": "You don't have the right credentials to see this. SORRY!"}, 401
    #A list of Pending users waitting to be approved by admin 
    pending_list = User.query.filter_by(role_id = 4)
    result = users_schema.dump(pending_list)
    return jsonify(result), 200

