from controllers.auth_controller import auth
from controllers.classes_controller import classes
# from controllers.enrollments_controller import enrollments
from controllers.instructors_controller import instructors
from controllers.students_controller import students
# from controllers.subjects_controller import subjects
from controllers.grade_controller import grades

# registerable_controllers = [auth, classes, enrollments, instructors, students, subjects]

registerable_controllers = [grades, auth, students, instructors, classes]