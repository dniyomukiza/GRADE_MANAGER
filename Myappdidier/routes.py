from flask import Blueprint, redirect, url_for, render_template,flash
from flask_login import login_user
from .extensions import db
from .models import User
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired,ValidationError,Length


main = Blueprint('main', __name__, template_folder='templates')

# Landing page route
@main.route('/')
def landing_page():
    return render_template('landing_page.html')


# Login route
@main.route("/login",methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter(User.username==form.username.data).first()
        if user and user.password==form.password.data:
            login_user(user)
            flash('You are in! Create title and blog then post it')
            return redirect(url_for('blogpost'))
        flash("Password does not match!")
    return render_template("login.html",title='Login',form=form)


# Register route
@main.route('/register',methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        new_user=User(username=form.username.data,password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Your account has been succesfully created!')
        return redirect(url_for('login'))   
    return render_template("register.html",title='Register',form=form)
    

class RegistrationForm(FlaskForm):
    username=StringField(validators=[DataRequired()],render_kw={"placeholder":"Username"})
    password=StringField(validators=[DataRequired(),Length(min=2,max=20)],render_kw={"placeholder":"Password"})
    submit=SubmitField('Sign up')
    def validate_username(self,username):
        user_exists=User.query.filter_by(username=username.data).first()
        if user_exists:
            flash("This user already exists, just log in!")
            raise ValidationError   

class LoginForm(FlaskForm):
    username=StringField(validators=[DataRequired()],render_kw={"placeholder":"Username"})
    password=StringField(validators=[DataRequired(),Length(min=2,max=20)],render_kw={"placeholder":"Password"})
    submit=SubmitField('Login')