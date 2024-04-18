
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length,ValidationError,Email
from flask import Flask,redirect,url_for,render_template,request,flash,abort

app=Flask(__name__)# initiliaze app and configure the secret key
@app.route("/")
def landing():
    return "hi"
'''
@app.route("/signup",methods=['GET','POST'])
def register():
    log_web_visit()
    form=RegistrationForm()
    if form.validate_on_submit():
        #hash_pass= bcrypt.generate_password_hash(form.password.data)
        new_user=User(username=form.username.data,password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Your account has been succesfully created!')
        return redirect(url_for('login'))    
    return render_template("signup.html",title='Register',form=form)

@app.route("/login",methods=['GET','POST'])
def login():
    log_web_visit()
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter(User.username==form.username.data).first()
        if user and user.password==form.password.data:
            login_user(user)
            flash('You are in! Create title and blog then post it')
            return redirect(url_for('blogpost'))
        flash("Password does not match!")
    return render_template("login.html",title='Login',form=form)


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
'''

if __name__ == "__main__":
    app.run(debug=True)


