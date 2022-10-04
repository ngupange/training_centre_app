from pstats import SortKey
from flask import Blueprint, json
from main import db
from sqlalchemy import text

grades = Blueprint('grades', __name__, url_prefix="/grades")


@grades.route("/student/<int:id>", methods=["GET"])
def get_student_grade(id):
    codesql = text('''SELECT usr.first_name, usr.last_name, sub.title as Subject, enr.grade 
    FROM subjects sub JOIN classes cl ON 
    cl.subject_id = sub.subject_id JOIN enrollments enr ON enr.class_id = cl.class_id 
    JOIN students std ON std.student_id = enr.student_id JOIN users usr ON 
    usr.user_id = std.user_id AND std.student_id = :val''')
    result = db.engine.execute(codesql, {"val": id})
    var = json.dumps([dict(r) for r in result], sort_keys=False, indent=2)
    if var == "[]":
        return {"error": "No for this student"}, 404
    return var

# Grade for all students

# Owners and Admin only (FIX !!!!!!!!!!!!!!)

@grades.route("/student", methods=["GET"])
def get_students_grade():
    codesql = text('''SELECT usr.first_name, usr.last_name, sub.title as Subject, enr.grade 
    FROM subjects sub JOIN classes cl ON 
    cl.subject_id = sub.subject_id JOIN enrollments enr ON enr.class_id = cl.class_id 
    JOIN students std ON std.student_id = enr.student_id JOIN users usr ON 
    usr.user_id = std.user_id''')
    ordered = True
    result = db.engine.execute(codesql)
    var = json.dumps([dict(r) for r in result], sort_keys=False, indent=2)
    if var == "[]":
        return {"error": "No student has grade to display"}, 404
    return var
