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
    if get_jwt_identity() != "Admin":
        return {"error": "You don't have the right credentials to see this. SORRY!"}, 401
    #A list of Pending users waitting to be approved by admin 
    pending_list = User.query.filter_by(role_id = 4)
    if not pending_list:
        return {"error": "User id not found there is no pending User to display."}
    
    user = User.query.filter_by(user_id=id).first()
    # if not user:
    #     return {"error": "This user is already a student"}

    student_fields = student_schema.load(request.json)
    student = Student(
        # user_id = student_fields["user_id"],
        level = student_fields["level"],
        status = student_fields["status"],
    )
    student.user_id = id
    db.session.add(student)
    user.role_id = 3
    db.session.commit()

    return jsonify(student_schema.dump(student)), 201