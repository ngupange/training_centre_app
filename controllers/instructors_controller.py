from flask import Blueprint, jsonify, request
from main import db
from models.instructor import Instructor
from schemas.instructor_schema import instructor_schema, instructors_schema
from flask_jwt_extended import jwt_required

instructors = Blueprint('instructors', __name__, url_prefix="/instructors")


@instructors.route("/", methods=["GET"])
def get_instructors():
    # get all the books from the database
    instructors_list = Instructor.query.all()
    result = instructors_schema.dump(instructors_list)
    return jsonify(result)

@instructors.route("/<int:id>", methods=["GET"])
def get_instructor(id):
    instructor = Instructor.query.get(id)
    if not instructor:
        return {"error": "instructor id not found"}
    result = instructor_schema.dump(instructor)
    return jsonify(result) 