from main import db
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey

class Class(db.Model):
		#Table name in database
    __tablename__ = 'classes'

	#Columns
    class_id = Column(Integer, primary_key=True)
    instructor_id = Column(Integer, ForeignKey('instructors.instructor_id'), 
            nullable = False, unique = True)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'), 
            nullable = False, unique = True)
    status = Column(Boolean, default = True)
    delivery_mode = Column(String)
    detail = Column(String)
	
    #relationship
    enrollments = db.relationship(
        "Enrollment",
        backref = "class"
    )