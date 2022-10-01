from main import ma
from marshmallow.validate import Length


class UserSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("user_id", "first_name", "last_name", "dob",
                  "email", "mobile", "username", "password", "role_id")
    # Password length validation
    password = ma.String(validate=Length(min=8))


user_schema = UserSchema()
users_schema = UserSchema(many=True)
