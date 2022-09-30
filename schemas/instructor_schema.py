from main import ma
from marshmallow import fields
from schemas.user_schema import UserSchema

class InstructorSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("instructor_id", "user", "hire_date", "status")
    user = fields.Nested("UserSchema", only=("first_name", "last_name", "dob", "mobile"))


instructor_schema = InstructorSchema()
instructors_schema = InstructorSchema(many=True)

