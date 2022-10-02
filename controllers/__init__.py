from controllers.auth_controller import auth
from controllers.classes_controller import classes
from controllers.enrollments_controller import enrollments
from controllers.instructors_controller import instructors
from controllers.students_controller import students
from controllers.subjects_controller import subjects
from controllers.grade_controller import grades
from controllers.titles_controller import trials
from controllers.users_controller import users


registerable_controllers = [grades, auth, students,
                            instructors, classes, enrollments, subjects, trials, users]