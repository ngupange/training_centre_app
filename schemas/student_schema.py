from main import ma
from marshmallow import fields
from schemas.user_schema import UserSchema


class StudentSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("student_id", "user", "level", "status")
    user = fields.Nested(UserSchema, only=(
        "first_name", "last_name", "dob", "mobile"))


student_schema = StudentSchema()
students_schema = StudentSchema(many=True)
