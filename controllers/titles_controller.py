from flask import Blueprint, jsonify, request, json
from main import db
from models.student import Student
from schemas.student_schema import student_schema, students_schema
from flask_jwt_extended import jwt_required
from sqlalchemy import text

trials = Blueprint('trials', __name__, url_prefix="/trials")


@trials.route("/", methods=["GET"])
def get_join_subject():
    codesql = text('''SELECT sub.title FROM subjects sub JOIN classes cl ON cl.subject_id = sub.subject_id JOIN enrollments enr ON enr.class_id = cl.class_id JOIN students std ON std.student_id = enr.student_id JOIN users usr ON usr.user_id = std.user_id''')
    result = db.engine.execute(codesql)
    var = json.dumps([dict(r) for r in result])
    if var == "[]":
        return {"error": "No ......."}, 404
    return var


    