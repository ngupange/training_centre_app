from flask import Blueprint, jsonify, request
from main import db
from models.enrollment import Enrollment
from schemas.enrollment_schema import enrollment_schema, enrollments_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.the_class import TheClass
from models.student import Student
from models.user import User
from datetime import date
from marshmallow.exceptions import ValidationError

enrollments = Blueprint('enrollments', __name__, url_prefix="/enrollments")


@enrollments.route("/", methods=["GET"])
def get_enrollments():
    enrollments_list = Enrollment.query.all()
    result = enrollments_schema.dump(enrollments_list)
    return jsonify(result), 200


@enrollments.route("/<int:id>", methods=["GET"])
def get_enrollment(id):
    enrollment = Enrollment.query.get(id)
    if not enrollment:
        return {"error": "enrollment id not found"}
    result = enrollment_schema.dump(enrollment)
    return jsonify(result), 200

@enrollments.route("/", methods=["POST"])
@jwt_required()
def add_enrollment(): 
    try: 
        if get_jwt_identity() == "Admin":
            return {"error": "You don't have the right credentials to see this. SORRY!"}, 401
        
        current_id = get_jwt_identity() 
        class_id = request.json['class_id']

        # Checking class you want to enroll into exists ...
        test = TheClass.query.filter_by(class_id = class_id).first()
        if not test:
            return jsonify("There is no class with that ID"), 409
        
        #Checking if the user trying to enroll is a student ...
        user = User.query.filter_by(user_id = current_id).first()
        student = Student.query.filter_by(user_id = user.user_id).first()
        test2 = Student.query.filter_by(student_id = student.student_id).first()
        if not test2:
            return jsonify("There is no student with that ID"), 409
        
        #Check if there is another active enrollment
        test3 = Enrollment.query.filter_by(student_id = test2.student_id, class_id = class_id , status = True).first()
        if test3 :            
            return {"error": "Sorry You are alredy enrolled in this class"}, 409
        new_enrollment = Enrollment(
            class_id = class_id,
            student_id = student.student_id,
            enrollment_date = date.today(),
            )
        db.session.add(new_enrollment)

        db.session.commit()
        return jsonify(message="You are Enrolled"), 201
    except KeyError:
        return jsonify(message='Check your input'), 400
        
@enrollments.errorhandler(ValidationError)
def register_validation_error(error):
    #print(error.messages)
    return error.messages, 400

@enrollments.errorhandler(500)
def handle_bad_request(error):
    return error.messages, 500
