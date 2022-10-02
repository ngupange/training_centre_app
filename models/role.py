from main import db
from sqlalchemy import Column, Integer, String, Float


class Role(db.Model):
    # define the tablename
    __tablename__ = "roles"
    
    # setting the columns
    role_id = db.Column(db.Integer, primary_key=True)
    # title
    role = db.Column(db.String())
    description = db.Column(db.String())
    # relationship
    users = db.relationship(
        "User",
        backref="role",
        cascade="all, delete"
    )
