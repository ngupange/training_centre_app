from main import db
from sqlalchemy import Column, Integer, String


class Subject(db.Model):
    # Table name in database
    __tablename__ = 'subjects'

    # Columns
    subject_id = Column(Integer, primary_key=True)
    title = Column(String)
    credits = Column(Integer)
    description = Column(String)
    # relationship
    classes = db.relationship(
        "TheClass",
        backref="subject",
        cascade="all, delete"
    )
