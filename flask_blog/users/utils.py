import os
import secrets
from PIL import Image
from flask import url_for
from flask_blog import app, mail
from flask_mail import Message


def save_picture(form_picture):
    random_name = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    picture_name = random_name + file_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_name)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_name


def send_rest_request(user):
    token = user.create_token()
    msg = Message('Password reset email',
                  sender='bihireb1@gmail.com',
                  recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link
    {url_for('reset_password', token=token, _external=True)}.
    If you did not do this request, please ignore this request and no changes will be made.
    '''
    mail.send(msg)
