from main import db
from sqlalchemy import Column, Integer, Boolean, Date, ForeignKey


class Instructor(db.Model):
    # Table name in database
    __tablename__ = 'instructors'

    # Columns
    instructor_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False, unique=True)
    hire_date = Column(Date)
    # Admin is the only user to validate if  user is an instructor
    status = Column(Boolean, default=False)
    
    # relationship
    classes = db.relationship(
        "TheClass",
        backref="instructor",
        cascade="all, delete"
    )
