from flask import Blueprint, jsonify, request
from main import db
from models.student import Student
from schemas.student_schema import student_schema, students_schema
from flask_jwt_extended import jwt_required
from flask_jwt_extended import jwt_required, get_jwt_identity

students = Blueprint('students', __name__, url_prefix="/students")


@students.route("/", methods=["GET"])
@jwt_required()
def get_students():
    if get_jwt_identity() != "Admin":
        return {"error": "You don't have the right credentials to see this. SORRY!"}, 401

    # get all Students from the database
    students_list = Student.query.all()
    result = students_schema.dump(students_list)
    return jsonify(result)


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
        return jsonify(result)
    
    # Unless admin and owner of the course no one else can see details
    if get_jwt_identity() != "Admin":
        return {"error": "You don't have the right credentials to see this. SORRY!"}, 401
    result = student_schema.dump(student)
    return jsonify(result)
