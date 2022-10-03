from flask import Blueprint, jsonify, request
from main import db
from models.subject import Subject
from schemas.subject_schema import subject_schema, subjects_schema
from flask_jwt_extended import jwt_required, get_jwt_identity

subjects = Blueprint('subjects', __name__, url_prefix="/subjects")


# Admin is the only user who can view these endpoints

@subjects.route("/", methods=["GET"])
@jwt_required()
def get_subjects():

    # Checking admin credential

    if get_jwt_identity() != "Admin":
        return {"error": "You don't have the right credentials to see this. SORRY!"}, 401
    
    # get all the books from the database
    subjects_list = Subject.query.all()
    result = subjects_schema.dump(subjects_list)
    return jsonify(result), 200


@subjects.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_subject(id):

    # Checking admin credential

    if get_jwt_identity() != "Admin":
        return {"error": "You don't have the right credentials to see this. SORRY!"}, 401
    
    subject = Subject.query.get(id)
    if not subject:
        return {"error": "subject id not found"}
    result = subject_schema.dump(subject)
    return jsonify(result), 200

#POST a subject
@subjects.route("/", methods=["POST"])
@jwt_required()
def create_subject():

    # Checking admin credential

    if get_jwt_identity() != "Admin":
        return {"error": "You don't have the right credentials to see this. SORRY!"}, 401
    
    #get the values from the request and load them with the single schema
    subject_fields = subject_schema.load(request.json)
    #create a new subject object
    subject = Subject(
        title = subject_fields["title"],
        credits= subject_fields["credits"],
        description= subject_fields["description"]
    )

    db.session.add(subject)
    #store in the database and save the changes
    db.session.commit()

    return jsonify(subject_schema.dump(subject))