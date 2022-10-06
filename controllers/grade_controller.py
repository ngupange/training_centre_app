from flask import Blueprint, json, jsonify, request
from main import db
from sqlalchemy import text
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.student import Student
from models.enrollment import Enrollment
from schemas.enrollment_schema import enrollment_schema
from models.the_class import TheClass
from models.instructor import Instructor

grades = Blueprint('grades', __name__, url_prefix="/grades")


@grades.route("/student/<int:id>", methods=["GET"])
@jwt_required()
def get_student_grade(id):
    current_id = get_jwt_identity()
    student = Student.query.get(id)
    #Check if Id provided as parameter exist in Students Database
    if not student:
        return {"error": "student id not found"}, 404
    
    user_id = student.user_id

    # Boolean values
    admin = get_jwt_identity() == "Admin"
    user = str(user_id) == str(current_id)

     # Check if the signed in user is the teacher of that class so he or she can visualise class infos

    # Check if the signed in user is the teacher of that class so he or she can visualise class infos
    if admin or user:
        codesql = text('''SELECT usr.first_name, usr.last_name, sub.title as Subject, enr.grade 
        FROM subjects sub JOIN classes cl ON 
        cl.subject_id = sub.subject_id JOIN enrollments enr ON enr.class_id = cl.class_id 
        JOIN students std ON std.student_id = enr.student_id JOIN users usr ON 
        usr.user_id = std.user_id AND std.student_id = :val''')
        result = db.engine.execute(codesql, {"val": id})
        
        var = json.dumps([dict(r) for r in result], sort_keys=False, indent=2)
        if var == "[]":
            return {"error": "No Grade to show for this student"}, 404
        return var
    return {"error": "You don't have the right credentials to see this grade. SORRY!"}, 401
    

# Grade for all students

# Owners and Admin only

@grades.route("/student", methods=["GET"])
@jwt_required()
def get_students_grade():

    if get_jwt_identity() != "Admin":
        return {"error": "You don't have the right credentials to see this. SORRY!"}, 401
    
    codesql = text('''SELECT usr.first_name, usr.last_name, sub.title as Subject, enr.grade 
    FROM subjects sub JOIN classes cl ON 
    cl.subject_id = sub.subject_id JOIN enrollments enr ON enr.class_id = cl.class_id 
    JOIN students std ON std.student_id = enr.student_id JOIN users usr ON 
    usr.user_id = std.user_id''')
    result = db.engine.execute(codesql)
    var = json.dumps([dict(r) for r in result], sort_keys=False, indent=2)
    if var == "[]":
        return {"error": "No student has grade to display"}, 404
    return var

@grades.route("/students/<int:id>", methods=["POST"])
@jwt_required()
def update_student_grade(id):
    try:
        current_id = get_jwt_identity()

        instructor = Instructor.query.filter_by(user_id = current_id).first()
        if not instructor:
            return {"error": "You are not an instructor"}, 400
   
        # Check if Id provided as parameter enrolled in any course
        enrollment = Enrollment.query.filter_by(student_id = id, grade ='Not Yet').first()
        if not enrollment:
            return {"error": "This student has no grade to be updated please double check the ID"}, 400

        theclass = TheClass.query.filter_by(instructor_id = instructor.instructor_id).first()

        # check enrollment table if instructor has a ungraded course

        enrol_check = Enrollment.query.filter_by(class_id = theclass.class_id, grade ='Not Yet', student_id = id).first()
        if not enrol_check:
            return {"error": "You can't change any thing for this student"}, 400
        enrol = Enrollment.query.filter_by(student_id = enrol_check.student_id).first()
        if  enrol.student_id == id:  
            #upodate the Grade
            enroll_fields = enrollment_schema.load(request.json)
            enrol.grade = enroll_fields["grade"]
            enrol.status = False
            db.session.commit()
            return jsonify(message="You updated a record"), 202
        else:
            return jsonify(message="You can't update this student's grade please check ID"), 404
    except Exception:
        return jsonify(message='Check your input'), 400
