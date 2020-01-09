from flask import Blueprint, render_template, url_for, flash, redirect, request, abort

from flask_blog.posts.forms import CreatePost
from flask_login import current_user, login_required
from flask_blog import db
from flask_blog.models import Post


posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePost()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post  has been created', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', legend='New Post', form=form)


@posts.route("/post/<int:post_id>")
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('specific_post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)
    form = CreatePost()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.view_post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', legend='Update Post', form=form)


@posts.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
