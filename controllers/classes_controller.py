from pstats import SortKey
from flask import Blueprint, json, jsonify, request
from main import db
from sqlalchemy import text, Boolean
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.the_class import TheClass
from schemas.classes_schema import class_schema, classes_schema
from models.instructor import Instructor

classes = Blueprint('classes', __name__, url_prefix="/classes")


@classes.route("/", methods=["GET"])
@jwt_required()
def subjects_class():
    if get_jwt_identity() != "Admin":
        return {"error": "You don't have the right credentials to see this. SORRY!"}, 401

    codesql = text('''SELECT sub.title as Subject, usr.first_name || ' ' || usr.last_name as Instructor, cl.delivery_mode as DeliveryMode, cl.detail as Details, sub.description as Descriptions, sub.credits as Credits, cl.status as Status,  COUNT(DISTINCT enr.student_id) AS Enrolled_Students
		FROM classes cl 
    JOIN subjects sub ON cl.subject_id = sub.subject_id 
    JOIN instructors ins ON ins.instructor_id = cl.instructor_id 
    JOIN users usr ON usr.user_id = ins.user_id 
		JOIN enrollments enr ON enr.class_id = cl.class_id
    WHERE cl.status = True
		GROUP BY sub.title, usr.first_name, usr.last_name, cl.delivery_mode, cl.detail, sub.description, sub.credits, cl.status;''')
    result = db.engine.execute(codesql)
    var = json.dumps([dict(r) for r in result], sort_keys=False, indent=2)
    if var == "[]":
        return {"error": "No Class at this momement"}, 404
    return var

# To access this endpoint you need to be admin or you need to be the instructor of this class

@classes.route("/<int:id>", methods=["GET"])
@jwt_required()
def subject_class(id):
    current_id = get_jwt_identity()    
    theclass = TheClass.query.get(id)
    # Check if Id provided as parameter exist in Classes table
    if not theclass:
        return {"error": "Class id not found"}
    ID = theclass.instructor_id
    instructor = Instructor.query.get(ID)
    user_id = instructor.user_id

    # Boolean values
    admin = get_jwt_identity() == "Admin"
    user = str(user_id) == str(current_id)

     # Check if the signed in user is the teacher of that class so he or she can visualise class infos

    # Check if the signed in user is the teacher of that class so he or she can visualise class infos
    if admin or user:
        codesql = text('''SELECT sub.title as Subject, usr.first_name || ' ' || usr.last_name as Instructor, cl.delivery_mode as DeliveryMode, cl.detail as Details, sub.description as Descriptions, sub.credits as Credits, cl.status as Status,  COUNT(DISTINCT enr.student_id) AS Enrolled_Students
            FROM classes cl 
        JOIN subjects sub ON cl.subject_id = sub.subject_id 
        JOIN instructors ins ON ins.instructor_id = cl.instructor_id 
        JOIN users usr ON usr.user_id = ins.user_id 
            JOIN enrollments enr ON enr.class_id = cl.class_id
        WHERE cl.class_id = :val
            GROUP BY sub.title, usr.first_name, usr.last_name, cl.delivery_mode, cl.detail, sub.description, sub.credits, cl.status;''')
        result = db.engine.execute(codesql, {"val": id})
        var = json.dumps([dict(r) for r in result], sort_keys=False, indent=2)
        if var == "[]":
            return {"error": "No Class at this momement"}, 404
        return var

    return {"error": "You don't have the right credentials to see this. SORRY!"}, 401

@classes.route("/", methods=["POST"])
@jwt_required()
def add_class():
    if get_jwt_identity() != "Admin":
        return {"error": "You don't have the right credentials to see this. SORRY!"}, 401
    
    subject_id = request.json['subject_id']
    test = TheClass.query.filter_by(subject_id=subject_id).first()
    if test:
        return jsonify("There is already a class for that subject"), 409
    else:
        instructor_id = request.json['instructor_id']
        delivery_mode = request.json['delivery_mode']
        detail = request.json['detail']

        new_class = TheClass(subject_id = subject_id,
            instructor_id = instructor_id,
            delivery_mode = delivery_mode,
            detail = detail)

        db.session.add(new_class)
        db.session.commit()
        return jsonify(message="You added a class"), 201

@classes.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_class(id):
    if get_jwt_identity() != "Admin":
        return {"error": "You don't have the right credentials to see this. SORRY!"}, 401
        
    aclass = TheClass.query.filter_by(class_id = id).first()
    if aclass:
        aclass.subject_id = request.json['subject_id']
        aclass.instructor_id = request.json['instructor_id']
        aclass.delivery_mode = request.json['delivery_mode']
        aclass.detail = request.json['detail']
        aclass.status = request.json['status']
        db.session.commit()
        return jsonify(message="You updated a class"), 202
    else:
        return jsonify(message="That class does not exist"), 404
