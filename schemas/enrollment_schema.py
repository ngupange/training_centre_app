from main import ma
from marshmallow import fields
from schemas.classes_schema import ClassSchema
from schemas.student_schema import StudentSchema


class EnrollmentSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("enrollment_id", "theclass",
                  "student", "enrollment_date", "grade")
    theclass = fields.Nested(ClassSchema, only=("class_id", ))
    student = fields.Nested(StudentSchema, only=("student_id", ))


enrollment_schema = EnrollmentSchema()
enrollments_schema = EnrollmentSchema(many=True)
