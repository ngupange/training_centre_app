from flask import Blueprint
from main import db
from main import bcrypt
from models.role import Role
from models.student import Student
from models.user import User
from models.the_class import TheClass
from models.instructor import Instructor
from models.subject import Subject
from models.enrollment import Enrollment
from datetime import date, datetime

db_commands = Blueprint("db", __name__)


@db_commands.cli.command('create')
def create_db():
    # Tell SQLAlchemy to create all tables for all models in the physical DB
    db.create_all()
    print('Tables created')


@db_commands.cli.command('drop')
def drop_db():
    # Tell SQLAlchemy to drop all tables
    db.drop_all()
    print('Tables dropped')


@db_commands.cli.command('seed')
def seed_db():

    role1 = Role(
        role="Admin",
		description="System Administrator"
    )
    db.session.add(role1)
    
    role2 = Role(
        role = "Instructor",
		description = "An Instructor, Teacher"
    )
    db.session.add(role2)

    role3 = Role(
        role = "Student",
		description = "A student"
    )
    db.session.add(role3)

    role4 = Role(
        role = "User",
		description = "Just a User"
    )

    db.session.add(role4)  
    db.session.commit()

    
    user1 = User(
		first_name = "Pamela",
		last_name = "Manzi",
		dob = date(day = 20, month = 1, year = 1985 ),
        email = "mail@email.com",
        mobile = "0422334433",
		username = "pam",
        password = bcrypt.generate_password_hash("12345678").decode("utf-8"),
		role = role1
    )
    db.session.add(user1) 
    
    user2 = User(
		first_name = "Ado",
		last_name = "Jabana",
		dob = date(day = 12, month = 8, year = 1977 ),
        email = "jabana@email.com",
		username = "Jabanado",
        password = bcrypt.generate_password_hash("12345678").decode("utf-8"),
		role = role4,
        mobile = "0422334432"
    )

    db.session.add(user2) 

    user3 = User(
		first_name = "Olivier",
		last_name = "Bitama",
		dob = date(day = 30, month = 9, year = 1980 ),
        email = "bitamao@email.com",
		username = "Bita",
        password = bcrypt.generate_password_hash("12345678").decode("utf-8"),
		role = role2,
        mobile = "0422355633"
    )

    db.session.add(user3)

    user4 = User(
		first_name = "Titi",
		last_name = "Kamara",
		dob = date(day = 15, month = 12, year = 2005 ),
        email = "katiti@email.com",
		username = "Titika",
        password = bcrypt.generate_password_hash("12345678").decode("utf-8"),
		role = role3,
        mobile = "0478834433"
    )

    db.session.add(user4)
		
    user5 = User(
		first_name = "Cadeaux",
		last_name = "Padesi",
		dob = date(day = 25, month = 10, year = 2001 ),
        email = "kapedesi@email.com",
		username = "Kapedesi",
        password = bcrypt.generate_password_hash("12345678").decode("utf-8"),
		role = role3,
        mobile = "0422388995"
    )

    db.session.add(user5)

    user6 = User(
		first_name = "Pappy",
		last_name = "Sangoma",
		dob = date(day = 12, month = 1, year = 1999 ),
        email = "sangomawa@email.com",
		username = "Sangoma",
        password = bcrypt.generate_password_hash("12345678").decode("utf-8"),
		role = role3,
        mobile = "043344553"
    )

    db.session.add(user6)
    db.session.commit()

 
    student1 = Student(
        user = user6,
        level = "Certificate III",
    )
    db.session.add(student1)
    

    student2 = Student(
        user = user5,
        level = "Certificate III",
    )
    db.session.add(student2)

    student3 = Student(
        user = user4,
        level = "Certificate III",
    )
    db.session.add(student3)
    db.session.commit()

    instructor1 = Instructor(
        user=user3,
        hire_date=date(day=12, month=1, year=2020)
    )
    db.session.add(instructor1)
    db.session.commit()

    subject1 = Subject(
        title="Math Statistics",
        credits=3,
        description="Basics of Statistics"
    )
    db.session.add(subject1)

    subject2 = Subject(
        title="Math Sets",
        credits=4,
        description="Sets"
    )
    db.session.add(subject2)

    subject3 = Subject(
        title="Math Geometric",
        credits=3,
        description="Basics of Geometric"
    )
    db.session.add(subject3)
    db.session.commit()

    class1 = TheClass(
        subject=subject3,
        instructor=instructor1,
        delivery_mode="In Class room",
        detail="This class run each afternoon for next 6 months"
    )
    db.session.add(class1)

    class2 = TheClass(
        subject=subject2,
        instructor=instructor1,
        delivery_mode="Online",
        detail="This class run from 10 to 12"
    )
    db.session.add(class2)

    class3 = TheClass(
        subject=subject1,
        instructor=instructor1,
        delivery_mode="In Class",
        detail="This class run every Monday to Friday"
    )
    db.session.add(class3)
    db.session.commit()

    enroll1 = Enrollment(
        theclass=class1,
        student=student3,
        enrollment_date=(datetime.date(datetime.now()))
    )
    db.session.add(enroll1)

    enroll2 = Enrollment(
        theclass=class2,
        student=student1,
        enrollment_date=(datetime.date(datetime.now()))
    )
    db.session.add(enroll2)

    enroll3 = Enrollment(
        theclass=class3,
        student=student2,
        enrollment_date=(datetime.date(datetime.now()))
    )
    db.session.add(enroll3)
    db.session.commit()
    print("tables seeded")