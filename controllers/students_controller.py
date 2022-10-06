from flask import Blueprint, jsonify, request
from main import db
from models.student import Student
from schemas.student_schema import student_schema, students_schema
from flask_jwt_extended import jwt_required
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User

students = Blueprint('students', __name__, url_prefix="/students")


@students.route("/", methods=["GET"])
@jwt_required()
def get_students():
    if get_jwt_identity() != "Admin":
        return {"error": "You don't have the right credentials to see this. SORRY!"}, 401

    # get all Students from the database
    students_list = Student.query.all()
    result = students_schema.dump(students_list)
    return jsonify(result), 200

@students.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_student(id):
    current_id = get_jwt_identity()
    student = Student.query.get(id)
    #Check if Id provided as parameter exist in Students Database
    if not student:
        return {"error": "student id not found"}
    
    # Check if the signed in user is the owner of the record so he or she can visualise her data
    if str(student.user_id) == current_id:
        result = student_schema.dump(student)
        return jsonify(result), 200
    
    # Unless admin and owner of the course no one else can see details
    if get_jwt_identity() != "Admin":
        return {"error": "You don't have the right credentials to see this. SORRY!"}, 401
    result = student_schema.dump(student)
    return jsonify(result), 200



@students.route("/activate/<int:id>", methods=["POST"])
@jwt_required()
def get_activate_student(id):
    try:
        if get_jwt_identity() != "Admin":
            return {"error": "You don't have the right credentials to see this. SORRY!"}, 401
       
        user = User.query.filter_by(user_id=id, role_id = 4).first()
        if not user:
            test = Student.query.filter_by(user_id = id).first()
            if test:
                return {"error": "Already a student"}
            return {"error": "This User ID is not valid to be a student"}

        student_fields = student_schema.load(request.json)
        student = Student(
            # user_id = student_fields["user_id"],
            level = student_fields["level"]
        )
        student.user_id = id
        student.status = True
        db.session.add(student)
        user.role_id = 3
        db.session.commit()

        return jsonify(student_schema.dump(student)), 201
    except Exception as e:
        return jsonify(message='Check your input'), 400