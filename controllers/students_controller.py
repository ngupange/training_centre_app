from flask import Blueprint, jsonify, request
from main import db
from models.student import Student
from schemas.student_schema import student_schema, students_schema
from flask_jwt_extended import jwt_required

students = Blueprint('students', __name__, url_prefix="/students")


@students.route("/", methods=["GET"])
def get_students():
    # get all the books from the database
    students_list = Student.query.all()
    result = students_schema.dump(students_list)
    return jsonify(result)

@students.route("/<int:id>", methods=["GET"])
def get_student(id):
    student = Student.query.get(id)
    if not student:
        return {"error": "student id not found"}
    result = student_schema.dump(student)
    return jsonify(result) 