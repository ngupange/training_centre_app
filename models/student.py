from main import db
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean


# database models

class Student(db.Model):
    # Table name in database
    __tablename__ = 'students'

    # Columns
    student_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False, unique=True)
    level = Column(String)
    status = Column(Boolean, default = False) #When you create account your account
        
    #relationship
    enrollments = db.relationship(
        "Enrollment",
        backref = "student",
        cascade="all, delete"
    )