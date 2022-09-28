from main import db
from sqlalchemy import Column, Integer, String, Date, ForeignKey

# database models


class User(db.Model):
    # Table name in database
    __tablename__ = 'users'

    # Columns
    user_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    dob = Column(Date)
    email = Column(String, nullable=False, unique=True)
    mobile = Column(String)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey('roles.role_id'))

    # relationship
    students = db.relationship(
        "Student",
        backref="user"
    )
    instructors = db.relationship(
        "Instructor",
        backref = "user"
    )
