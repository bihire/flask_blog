import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flask_blog import app, db, bcrypt
from flask_blog.forms import RegistrationForm, LoginForm, UpdateForm
from flask_blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


posts = [
    {
        "title": "this the first title",
        "author": "bihire",
        "date_posted": "2018-12-09",
        "content": "this is the dummy data for the first article and more if you want more don't wait for more",
    },
    {
        "title": "this the second title",
        "author": "boris",
        "date_posted": "2019-04-12",
        "content": "this is the dummy data for the first article and more if you want more don't wait for more",

    }
]


@app.route("/")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            image_file=form.image_file.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('wrong email or password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


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


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            old_file = os.path.join(app.root_path, 'static/images', current_user.image_file)
            os.remove(old_file)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('your account has been apdated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='images/' +
                         current_user.image_file)
    return render_template('account.html', title='My Account', image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
def create_post():
    return render_template('create_post.html', title='New Post')