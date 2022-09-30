from pstats import SortKey
from flask import Blueprint, json
from main import db
from sqlalchemy import text

classes = Blueprint('classes', __name__, url_prefix="/classes")


@classes.route("/", methods=["GET"])
def subjects_class():
    codesql = text('''SELECT sub.title as Subject, usr.first_name || ' ' || usr.last_name as Instructor, cl.delivery_mode as DeliveryMode, cl.detail as Details, sub.description as Descriptions, sub.credits as Credits, cl.status as Status FROM classes cl right JOIN subjects sub ON cl.subject_id = sub.subject_id JOIN instructors ins ON ins.instructor_id = cl.instructor_id JOIN users usr ON usr.user_id = ins.user_id WHERE cl.status = True''')
    result = db.engine.execute(codesql)
    var = json.dumps([dict(r) for r in result], sort_keys=False, indent=2)
    if var == "[]":
        return {"error": "No Class at this momement"}, 404
    return var
