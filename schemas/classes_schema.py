from main import ma
from marshmallow import fields
from schemas.instructor_schema import InstructorSchema
from schemas.subject_schema import SubjectSchema


class ClassSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("class_id", "instructor", "subject",
                  "status", "delivery_mode", "detail")
    instructor = fields.Nested(InstructorSchema, only=("instructor_id",))
    subject = fields.Nested(SubjectSchema, only=("title",))


class_schema = ClassSchema()
classes_schema = ClassSchema(many=True)
