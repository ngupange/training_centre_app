# T2A2 - API Webserver Project

## Links

**GitHub Repository:** [Click here](https://github.com/ngupange/training_centre_app)
---
## R1 Identification of the problem you are trying to solve by building this particular app.


The main purpose of this project is to develop an API in charge of certain task of a fictional Vocational training center / school.

Nowadays, it is desirable for any public or private entity with an educational or formative vocation to adhere to the new formula of delivering their courses that would allow that institution to put their contents online to overcome the problems of congestion within their classes and extend their geographical scope anyone who is interested around the world can take their course via online or on location.
This API will help student to enrol in a class, get their results / grade. Instructor will be able to grade their student and API has an Admin who will be in charge of creating classes and assign instructors to them. There is much to improve on this API in future. 

---
## R2 Why is it a problem that needs solving?


The original intention of this API was to create something that will help me to learn and feel more comfortable with Python and web development. With other skills I will get in next term my plan is to make this functional and any school in need may use it. We will add more task 

---
## R3 Why have you chosen this database system. What are the drawbacks compared to others?


I chose to develop this API using PostgreSQL as my database system because of many reasons here are some:  

- Postgres is an open-source DB
- Highly extensible
- It is easy to deal with complex data types like geodata for GPS
- Flexible text search 
- Ability to create functions, triggers, data types etc. 
- Supports JSON 
- It’ is cross-platform 

Here are some desadvantages:

- Not available by default on all hosts 
- It is a bit slower compared to other RDBMS’s speed

---
## R4 Identify and discuss the key functionalities and benefits of an ORM


An object-relational mapper (ORM) is a technique that allows a developer to query and manipulate data in a database using an object-oriented paradigm. To develop an application connected to a database normally requires database skills (SQL) on top of the programming language skills.
ORM is used to manipulate data (CRUD) between app and database but with ORM you only need programming language skills to manipulate objects in source codes and transform them into a database. Mapping is a tedious thing that you can use to automate the ORM to make it independent of the database you want to use, and you can even change the database management system without a problem. There is no need to learn SQL to perform databases tasks.

But these are not all good things ORM also has its drawbacks. In highly loaded environments, this can reduce performance because you add an extra layer to the system. It also involves learning the ORM so you can use it, which can take time to fully understand and take advantage of it

---
## R5 Document all endpoints for your API



---
## R6 Entity Relationship (ER) Diagram


![ERD](docs/erd.png)


---
## R7 Detail any third party services that your app will use

To develop this API I used Flask any third part I instolled was compatible with Flask. Here are some of third part we use to achieve this result and brief definition.

- ***Bcrypt:*** Bcrypt is an algorithm specially designed for hashing, based on an encryption algorithm commonly known as "Blowfish". I used it to avoid saving and retreiving password as plain text. 
- ***Flask*** Flask is an easy and simple python micro-framework that allows you to make scalable web applications. Flask depends on Werkzeug's WSGI web application library and the Jinja template engine.
- ***Json*** JSON (JavaScript Object Notation) is a textual file format designed for data exchange. It represents structured data based on the syntax of javaScript programming language objects.  We used Jsonfy in this API. Jsonify is a function in Flask's flask.json module. jsonify serializes data to JavaScript Object Notation (JSON) format, wraps it in a Response object with the application/json mimetype.
- ***JWT Extended*** A Web Token JSON is an access token with RFC 7519 standards that allows a secure exchange of data between two parties. It contains all the important information about an entity, which makes it unnecessary to consult a database and the session does not need to be save their credential on the server (stateless session). We used this to identify which user is loged in and what he is allowed to do once authenticated.
- ***Marshmallow:***  I used it jut to create schema and validate the data from the API.
- ***Psycopg2:*** This helps our API to connect to our database (Postgres). It is in charge of safe connection between app and DB.
- ***SQLAlchemy :*** Essentially, SQLAlchemy is the Python SQL toolkit that gives developers the ability to use the SQL database. . The advantage of using this special library is that the Python developer can work with language-specific objects rather than having to create separate SQL queries. Essentially, you can use SQLAlchemy in python to access and manipulate databases.

---
## R8 Describe your projects models in terms of the relationships they have with each other

In this project I will be tracking 7 tables :

- #### 1. Roles ####
    - This Table will have 4 differents users role an ***Admin*** in charge of the system, A ***student***, an ***instructor*** and a ***user*** who will be a default role for any user who sign in before he gets approved by admin. Roles table will hold 3 details about each record.
        - ***Role Id***: as a primary key to identifies each subject
        - ***Role***: a title of role
        - ***Description:*** Explanation about user or some comments about a specific user.

- #### 2. Users ####
    - This table will save all details about person who use this system. In order to achieve this user must have an account and password to be authenticated. Here are some details we will track:
        - ***User ID*** : helps to have unique user 
        - ***First Name, Last Name, Date of birth as dob*** : as idefication of a user,
        - ***E-mail, Mobile number*** : Helps to capture user's contact details 
        - ***Username, password, role_id*** : This will help in authenticating and authorisation for certains task. Password is hashed for security reason.

- #### 3. Students ####
    - This table will save all records regarding student users this table has relationship with user and Enrolments. This table will capture 4 inputs per each record:
        - ***Student_id :*** As a primary key to enforce uniqueness 
        - ***User_id :*** is a Foreign Key to hold all values about student's accounts details from user table.
        - ***Level :*** What is the highest level this student achieved. 
        - ***Status :***  When Student record created starts with a default value of *FALSE* this will change when Admin approve the application to become a student then Status will turns to True and if student is banned to use the system we can change status without delete his record.

- #### 4. Instructors ####
    - This table will save all record about our instructors. after signed in to the system an admin will assign a role to a pending user and make him an instructor. This table will collect 4 different input per each record:
      - ***Instructor Id :*** Primary key to identify instructors
      - ***User Id :*** Has a relashionship with users  table.
      - ***Hire Date :*** Automatically will grab today's date and save it
      - ***Status :*** Has a default value of false for each new record till Admin change it. this will also used in logic when we  checking if the instructor's account is active.

- #### 5. Subjects ####
    - This table is in charge of saving all about Subject. This will track 4 inputs for each record:
      - ***Subject ID :*** A Primary key for this table
      - ***Title :*** Title of the subject
      - ***Credits :*** Number of credits that coure has
      - ***Description :*** Details about this Subject

- #### 6. Classes ####
    - This table is a joint table between Subject and instructor and will save following data:
      - 
    ***Class Id :***  Primary Key  
    ***Subject Id :*** Foreign key because one subject may have more than one class
    ***Instructor Id :*** Foreign key because an Instructor may tutor more than one class
    ***Status :*** If class is running or is a graduated obe
    ***Delivery Mode :*** Now days some classes are in physical class room, online, on site this field will record way of class being delivered
    ***Detail :*** Some details or comments about class
- #### 7. Enrollments ####
    - This table is join table which represents relationship between classes table and Students. A class is taken by many students and one student can attend many classes. Here are some record to track about this table:
    - Enrollment Id :
    - Class Id 
    - Student Id
    - Enrollment Date:
    - Grade 
    - Status = Column(Boolean, default = True)
---
## R9 Discuss the database relations to be implemented in your application

- A **user** can have one and only one **role**, but a **role** can held by many **users**. (1 - 1)
- An **Instructor** can have a single account each (**user**) and and an account (**user**) is for a single **instructor** (1 -1)
- A **Student** can have a single account (**user**) and an account(**user**) is for a single **Student** (1 - 1)
- A **Subject** can be taught in many **classes**, but a **class** can be about one **Subject**. (1-M) this relationship is a result of a ***many to many*** relationship between *subject* and an *instructor*. **Instructor** can teach many **subject** and one **subject** can be taught by many **instuctors** (M-M)
- An **Instructor** can teach many **classes**, but every **class** has one instructor. (1-M)
- A **Student** can enroll in many **enrollments**, but an **enrollment** is for a single **student** only.
- An **enrollment** is for a single **class** and a **class** can have many **enrollments** (1-M). This relationship is a result of a ***Many to Many*** relationship between *class* and *student* where a ***student*** can attends many ***classes*** and each ***class*** has many ***students***. 

---
## R10 Describe the way tasks are allocated and tracked in your project
The tasks and features comprised of this project are broken down, implemented and tracked through trello board. Following an agile methodology.
Link to trello board: [Click here](https://trello.com/b/PpCH5HJm)

