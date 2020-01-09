import os
import secrets
from PIL import Image
from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_blog import app, db, bcrypt, mail
from flask_blog.users.forms import (RegistrationForm, LoginForm,
                              UpdateForm, RequestResetForm,
                              RequestPasswordReset)
from flask_blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from flask_blog.users.utils import save_picture, send_rest_request

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('wrong email or password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            if current_user.image_file != 'default.jpg':
                old_file = os.path.join(
                    app.root_path, 'static/images', current_user.image_file)
                os.remove(old_file)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('your account has been apdated', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='images/' +
                         current_user.image_file)
    return render_template('account.html', title='My Account', image_file=image_file, form=form)


@users.route("/user/<user_id>")
def user_posts(user_id):
    page = request.args.get('page', type=int, default=1)
    user = User.query.filter_by(id=user_id).first_or_404()
    print(user)
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.created_on.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_rest_request(user)
        flash('An email has been sent for your password reset')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', form=form, title='Reeset Password')


@users.route("/reset_password/<string:token>", methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_token(token)
    if not user:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = RequestPasswordReset()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(
            f'Password successfully reset for {form.username.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_password.html', form=form, title='Reeset Password')
