from main import db
from sqlalchemy import Column, Integer, String, Date, ForeignKey, UniqueConstraint


class Enrollment(db.Model):
    # Table name in database
    __tablename__ = 'enrollments'

    # Columns
    enrollment_id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey('classes.class_id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.student_id'), nullable=False)
    enrollment_date = Column(Date)
    grade = Column(String)
    UniqueConstraint('class_id', 'student_id', "enrollment_date", name='enrollment_unique_key')