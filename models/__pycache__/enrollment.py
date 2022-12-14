from main import db
from sqlalchemy import Column, Integer, String, Date, ForeignKey


class Enrollment(db.Model):
    # Table name in database
    __tablename__ = 'enrollments'

    # Columns
    enrollment_id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey(
        'classes.class_id'), nullable=False, unique=True)
    student_id = Column(Integer, ForeignKey(
        'students.student_id'), nullable=False, unique=True)
    enrollment_date = Column(Date)
    Grade = Column(String)
