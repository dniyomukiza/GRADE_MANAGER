from re import search

from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import login_user, current_user, login_required, logout_user
from wtforms.fields.simple import BooleanField
from .extensions import db
from .models import User, Class, Student
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Length

main = Blueprint('main', __name__, template_folder='templates')


# Landing page route
@main.route('/')
def landing_page():
    return render_template('landing_page.html')


# Login route
@main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.class_dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            db.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.class_dashboard'))
    return render_template("login.html", title='Login', form=form)


# Register route
# Register route
@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user_username = form.username.data
        new_user_password = form.password.data
        if len(new_user_username) < 7 or search("[\d]+", new_user_username) is None or search("[A-Z]+",
                                                                                              new_user_username) is None:
            flash("Username doesn't satisfy criteria")
        elif len(new_user_password) < 12 or search("[A-Z]+", new_user_password) is None or search("[_@#$]+",
                                                                                                  new_user_password) is None:
            flash("Password doesn't satisfy criteria")
        else:
            db.session.add(User(username=new_user_username, password=new_user_password))
            db.session.commit()
            flash(f'Your account has been successfully created! Please login below')
            return redirect(url_for('main.login'))
    return render_template("register.html", title='Register', form=form)


# Route for the class manager page
@main.route('/class_dashboard')
@login_required
def class_dashboard():
    # Query classes associated with the current user
    user_classes = Class.get_user_classes(current_user.id)
    return render_template('class_dashboard.html', classes=user_classes)


# Route for handling class operations
@main.route('/class_operation/<operation>')
@login_required
def class_operation(operation):
    # Redirect to respective subsystems based on user operation
    if operation == 'create':
        return redirect(url_for('main.create_class'))
    elif operation == 'rename':
        return redirect(url_for('main.rename_class'))
    elif operation == 'delete':
        return redirect(url_for('main.delete_class'))
    else:
        return redirect(url_for('main.class_manager'))


# Route for the create class page
@main.route('/create_class', methods=['GET', 'POST'])
@login_required
def create_class():
    if request.method == 'POST':
        class_name = request.form['class_name']
        if len(class_name) < 4:
            flash("Class name must have more than 4 characters")
        else:
            # Create the class and add it to the database
            Class.create_class(class_name, current_user.id)
            flash('Class "{}" created successfully.'.format(class_name), 'success')
            return redirect(url_for('main.class_dashboard'))
    return render_template('create_class.html')


@main.route('/rename_class', methods=['GET', 'POST'])
@login_required
def rename_class():
    if request.method == 'POST':
        class_id = request.form['class_id']
        new_class_name = request.form['new_class_name']
        class_obj = Class.query.get(class_id)
        if len(new_class_name) < 4:
            flash("Class name must have at least 4 characters")
        elif class_obj is None or class_obj.user_id != current_user.id:
            # Retrieve the class object
            # Handle unauthorized access or non-existing class
            flash('Class does not exist or you are not authorized to rename it.', 'error')
            return redirect(url_for('main.class_dashboard'))
        else:
            # Update the class name
            old_class_name = class_obj.class_name
            class_obj.class_name = new_class_name
            db.session.commit()
            flash('Class "{}" renamed to "{}" successfully.'.format(old_class_name, new_class_name), 'success')
            return redirect(url_for('main.class_dashboard'))

    # Render the template for renaming a class

    user_classes = Class.get_user_classes(current_user.id)

    return render_template('rename_class.html', classes=user_classes)


@main.route('/delete_class', methods=['GET', 'POST'])
@login_required
def delete_class():
    if request.method == 'POST':
        class_id = request.form['class_id']
        # Retrieve the class object
        class_obj = Class.query.get(class_id)
        if class_obj is None or class_obj.user_id != current_user.id:
            # Handle unauthorized access or non-existing class
            flash('Class does not exist or you are not authorized to delete it.', 'error')
            return redirect(url_for('main.class_dashboard'))
        # Delete the class
        db.session.delete(class_obj)
        db.session.commit()
        flash('Class "{}" deleted successfully.'.format(class_obj.class_name), 'success')
        return redirect(url_for('main.class_dashboard'))
    else:
        # Render the template for deleting a class
        user_classes = Class.get_user_classes(current_user.id)
        return render_template('delete_class.html', classes=user_classes)


# Route for the class homepage
@main.route('/class_home/<int:class_id>', methods=['GET', 'POST'])
@login_required
def class_home(class_id):
    # Retrieve the class object
    class_obj = Class.query.get(class_id)
    if class_obj is None or class_obj.user_id != current_user.id:
        # Handle unauthorized access or non-existing class
        return "Unauthorized access or class does not exist.", 404

    # Retrieve students enrolled in the class
    students = class_obj.students

    if request.method == 'POST':
        # Handle any other class-related actions, if needed
        pass

    return render_template('class_home.html', class_obj=class_obj, students=students, class_id=class_id)


# Route for adding a student
@main.route('/add_student/<int:class_id>', methods=['GET', 'POST'])
@login_required
def add_student(class_id):
    # Retrieve the class object
    class_obj = Class.query.get(class_id)
    if class_obj is None or class_obj.user_id != current_user.id:
        # Handle unauthorized access or non-existing class
        return "Unauthorized access or class does not exist.", 404

    if request.method == 'POST':
        # Process form submission to add a new student
        # Retrieve form data
        name = request.form['name']
        grade = request.form['grade']
        # Validate and add the student
        if len(name) < 4 or not name.replace(" ", "").isalpha():
            flash("Student name must have at least 4 characters and contain only alphabetic characters")
        elif not (grade.replace('.', '', 1).isdigit()) or not (0 <= float(grade) <= 100):
            flash("Grade percentage must be between 0 and 100")
        else:
            new_student = Student(name=name, grade=grade, class_enrolled=class_obj)
            db.session.add(new_student)
            db.session.commit()
            flash('Student "{}" added successfully.'.format(name), 'success')
            return redirect(url_for('main.class_home', class_id=class_id))

    # Pass class_id to the template
    return render_template('add_student.html', class_id=class_id)


@main.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('main.landing_page'))


@main.route('/student_sub_page/<int:student_id>', methods=['GET', 'POST'])
@login_required
def student_sub_page(student_id):
    # Retrieve the student object
    student = Student.query.get(student_id)
    class_id = Student.query.get(student_id).class_id
    if student is None:
        # Handle non-existing student
        return "Student does not exist.", 404

    if request.method == 'POST':
        if 'delete_student' in request.form:
            # Delete the student
            return_class_id = student.get_class_id()
            db.session.delete(student)
            db.session.commit()
            flash('Student "{}" deleted successfully.'.format(student.name), 'success')
            return redirect(url_for('main.class_home', class_id=return_class_id))
        elif 'update_name' in request.form:
            # Update the student's name
            new_name = request.form['new_name']
            if len(new_name) < 4 or not new_name.isalpha():
                flash("Student name must have at least 4 characters and contain only alphabetic characters")
                return render_template('student_subpage.html', student=student, class_id=class_id)
            else:
                student.name = new_name
                db.session.commit()
                flash('Student name updated successfully.', 'success')
                return redirect(url_for('main.student_sub_page', student_id=student_id))
        elif 'update_grade' in request.form:
            # Update the student's grade
            new_grade = request.form['new_grade']
            if not (new_grade.replace('.', '', 1).isdigit()) or not (0 <= float(new_grade) <= 100):
                flash("Grade percentage must be between 0 and 100")
                return render_template('student_subpage.html', student=student, class_id=class_id)
            else:
                student.grade = new_grade
                db.session.commit()
                flash('Student grade updated successfully.', 'success')
                return redirect(url_for('main.student_sub_page', student_id=student_id))

    return render_template('student_subpage.html', student=student, class_id=class_id)


class RegistrationForm(FlaskForm):
    username = StringField(validators=[DataRequired()], render_kw={"placeholder": "Username"})
    password = StringField(validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user_exists = User.query.filter_by(username=username.data).first()
        if user_exists:
            flash("This user already exists, just log in!")
            raise ValidationError


class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()], render_kw={"placeholder": "Username"})
    password = StringField(validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')
