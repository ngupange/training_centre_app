from flask import Blueprint, jsonify
from models.user import User
from schemas.user_schema import user_schema, users_schema
from flask_jwt_extended import jwt_required, get_jwt_identity

users = Blueprint('users', __name__, url_prefix="/users")

# List of users management
# #Admin is the only user who can view these endpoints

@users.route("/", methods=["GET"])
@jwt_required()
def get_user():

    # Checking admin credential

    if get_jwt_identity() != "Admin":
        return {"error": "You don't have the right credentials to see this. SORRY!"}, 401
    
    users_list = User.query.all()
    result = users_schema.dump(users_list)
    return jsonify(result), 200


@users.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_single_user(id):

    # Checking admin credential

    if get_jwt_identity() != "Admin":
        return {"error": "You don't have the right credentials to see this. SORRY!"}, 401
    reg_user = User.query.get(id)
    if not reg_user:
        return {"error": "User id not found"}
    result = user_schema.dump(reg_user)
    return jsonify(result), 200

# List of users who are waitting to be approved as instructors or Students
@users.route("/pending", methods=["GET"])
@jwt_required()
def get_pending_user():
    if get_jwt_identity() != "Admin":
        return {"error": "You don't have the right credentials to see this. SORRY!"}, 401
    #A list of Pending users waitting to be approved by admin 
    pending_list = User.query.filter_by(role_id = 4)
    result = users_schema.dump(pending_list)
    return jsonify(result), 200

