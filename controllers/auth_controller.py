from flask import Blueprint, jsonify, request
from main import db
from models.user import User
from schemas.user_schema import user_schema, users_schema

auth = Blueprint('auth', __name__, url_prefix="/auth")

# To access this User routes you need to be System Admin


@auth.route("/", methods=["GET"])
def get_user():
    users_list = User.query.all()
    result = users_schema.dump(users_list)
    return jsonify(result)


@auth.route("/<int:id>", methods=["GET"])
def get_single_user(id):
    reg_user = User.query.get(id)
    if not reg_user:
        return {"error": "User id not found"}
    result = user_schema.dump(reg_user)
    return jsonify(result)

