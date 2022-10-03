from flask import Blueprint, jsonify, request
from main import db
from models.instructor import Instructor
from schemas.instructor_schema import instructor_schema, instructors_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from datetime import date, datetime


instructors = Blueprint('instructors', __name__, url_prefix="/instructors")


@instructors.route("/", methods=["GET"])
@jwt_required()
def get_instructors():
    # Must be admin to access this
    if get_jwt_identity() != "Admin":
        return {"error": "You don't have the right credentials to see this. SORRY!"}, 401

    # get all Instructors from the database
    instructors_list = Instructor.query.all()
    result = instructors_schema.dump(instructors_list)
    return jsonify(result), 200

@instructors.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_instructor(id):
    instructor = Instructor.query.get(id)
    if not instructor:
        return {"error": "instructor id not found"}
    result = instructor_schema.dump(instructor)
    return jsonify(result), 200 

# DELETE an instructor
# @instructors.route("/<int:id>", methods=["DELETE"])
# @jwt_required()
# # @jwt_required()
# def delete_instructor(id):
#     instructor = Instructor.query.get(id)
#     if not instructor:
#         return {"error": "instructor id not found"}

#     db.session.delete(instructor)
#     db.session.commit()

#     return {"message": "Instructor removed successfully"}

# Create an instructor
@instructors.route("/activate/<int:id>", methods=["POST"])
@jwt_required()
def get_activate_instructor(id):
    if get_jwt_identity() != "Admin":
        return {"error": "You don't have the right credentials to see this. SORRY!"}, 401
    
    #A list of Pending users waitting to be approved by admin 
    pending_list = User.query.filter_by(role_id = 4)
    if not pending_list:
        return {"error": "User id not found there is no pending User to display."}
    
    user = User.query.filter_by(user_id=id).first()
    # if not user:
    #     return {"error": "This user is already a instructor"}

    instructor_fields = instructor_schema.load(request.json)
    instructor = Instructor(
        status = instructor_fields["status"]
    )
    instructor.user_id = id
    hire_date = (datetime.date(datetime.now()))
    db.session.add(instructor)
    user.role_id = 2
    db.session.commit()

    return jsonify(instructor_schema.dump(instructor)), 201