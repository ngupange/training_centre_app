from flask import Blueprint, jsonify, request
from main import db
from models.subject import Subject
from schemas.subject_schema import subject_schema, subjects_schema
from flask_jwt_extended import jwt_required

subjects = Blueprint('subjects', __name__, url_prefix="/subjects")


@subjects.route("/", methods=["GET"])
def get_subjects():
    # get all the books from the database
    subjects_list = Subject.query.all()
    result = subjects_schema.dump(subjects_list)
    return jsonify(result)


@subjects.route("/<int:id>", methods=["GET"])
def get_subject(id):
    subject = Subject.query.get(id)
    if not subject:
        return {"error": "subject id not found"}
    result = subject_schema.dump(subject)
    return jsonify(result)
