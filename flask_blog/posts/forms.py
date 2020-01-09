from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import data_required


class CreatePost(FlaskForm):
    title = StringField('Title', validators=[data_required()])
    content = TextAreaField('Content', validators=[data_required()])
    submit = SubmitField('Post')
