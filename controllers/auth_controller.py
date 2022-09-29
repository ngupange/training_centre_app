from flask import Blueprint, jsonify, request
from main import db
from models.user import User
from schemas.user_schema import user_schema, users_schema

auth = Blueprint('auth', __name__, url_prefix="/auth")


@auth.route("/", methods=["GET"])
def get_user():
    # get all the books from the database
    users_list = User.query.all()
    result = users_schema.dump(users_list)
    return jsonify(result)