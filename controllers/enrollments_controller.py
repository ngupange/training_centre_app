from flask import Blueprint, jsonify, request
from main import db
from models.enrollment import Enrollment
from schemas.enrollment_schema import enrollment_schema, enrollments_schema
from flask_jwt_extended import jwt_required

enrollments = Blueprint('enrollments', __name__, url_prefix="/enrollments")


@enrollments.route("/", methods=["GET"])
def get_enrollments():
    enrollments_list = Enrollment.query.all()
    result = enrollments_schema.dump(enrollments_list)
    return jsonify(result), 200


@enrollments.route("/<int:id>", methods=["GET"])
def get_enrollment(id):
    enrollment = Enrollment.query.get(id)
    if not enrollment:
        return {"error": "enrollment id not found"}
    result = enrollment_schema.dump(enrollment)
    return jsonify(result), 200
