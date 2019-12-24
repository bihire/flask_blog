from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import data_required, Length, Email, EqualTo

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


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[data_required(), Email()])
    password = PasswordField('Password',
                             validators=[data_required(), Length(min=8, max=32)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
