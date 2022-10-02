from flask import Blueprint, jsonify, request
from main import db
from models.instructor import Instructor
from schemas.instructor_schema import instructor_schema, instructors_schema
from flask_jwt_extended import jwt_required

instructors = Blueprint('instructors', __name__, url_prefix="/instructors")


@instructors.route("/", methods=["GET"])
def get_instructors():
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

#DELETE an instructor
@instructors.route("/<int:id>", methods=["DELETE"])
# @jwt_required()
def delete_instructor(id):
    instructor = Instructor.query.get(id)
    if not instructor:
        return {"error": "instructor id not found"}

    db.session.delete(instructor)
    db.session.commit()

    return {"message": "Instructor removed successfully"}

# Create an instructor
@instructors.route("/", methods=["POST"])
# @jwt_required()
def create_instructor():
    instructor_fields = instructor_schema.load(request.json)
    instructor = Instructor(
        user_id = instructor_fields["user_id"],
        hire_date= instructor_fields["hire_date"],
        status= instructor_fields["status"]
    )

    db.session.add(instructor)
    db.session.commit()

    return jsonify(instructor_schema.dump(instructor))