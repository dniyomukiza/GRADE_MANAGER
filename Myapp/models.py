from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db
from flask_login import UserMixin
from wtforms.validators import ValidationError


# Define the Class model (database)
class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(100))
    user_id = db.Column(db.Integer)  # Assuming a foreign key relationship

    # Define relationship with Student model
    students = db.relationship('Student', backref='class_enrolled', lazy=True)

    @classmethod
    def get_user_classes(cls, user_id):
        # Method to retrieve classes associated with the user
        user_classes = cls.query.filter_by(user_id=user_id).all()
        return user_classes

    @classmethod
    def create_class(cls, class_name, user_id):
        # Method to create a new class
        new_class = cls(class_name=class_name, user_id=user_id)
        db.session.add(new_class)
        db.session.commit()
        return new_class


# Define the Student model (database)
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    grade = db.Column(db.Float)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))  # Foreign key relationship

    @classmethod
    def get_student(cls, student_id):
        # Method to retrieve student by ID
        return cls.query.get(student_id)

    @classmethod
    def create_student(cls, name, grade):
        # Method to create a new student
        new_student = cls(name=name, grade=grade)
        db.session.add(new_student)
        db.session.commit()
        return new_student

    def update_name(self, new_name):
        # Method to update student's name
        self.name = new_name
        db.session.commit()

    def update_grade(self, new_grade):
        # Method to update student's grade
        self.grade = new_grade
        db.session.commit()

    def delete_student(self):
        # Method to delete student
        db.session.delete(self)
        db.session.commit()

    def get_class_id(self):
        # Method to return the associated class ID
        return self.class_id


# Define the User model (database)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(250))  # Assuming password hashing for security

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)  # Set the password using the set_password method

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def create_user(cls, username, password_hash):
        new_user = cls(username=username, password=password_hash)
        db.session.add(new_user)
        db.session.commit()

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
