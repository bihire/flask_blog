from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import data_required, Length, Email, EqualTo, ValidationError
from flask_blog.models import User, Post

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[data_required(), Length(min=6, max=20)])
    email = StringField('Email',
                        validators=[data_required(), Email()])
    password = PasswordField('Password',
                             validators=[data_required(), Length(min=8, max=32)])
    confirm_password = PasswordField('Confirm password',
                                     validators=[data_required(), EqualTo('password')])
    submit = SubmitField('submit')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('email exist already!')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[data_required(), Email()])
    password = PasswordField('Password',
                             validators=[data_required(), Length(min=8, max=32)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class UpdateForm(FlaskForm):
    username = StringField('Username',
                           validators=[data_required(), Length(min=6, max=20)])
    email = StringField('Email',
                        validators=[data_required(), Email()])
    picture = FileField('Update Profile picture',
                        validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('user exist already!')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('email exist already!')
