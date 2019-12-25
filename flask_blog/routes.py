from flask import render_template, url_for, flash, redirect
from flask_blog import app, db, bcrypt
from flask_blog.forms import RegistrationForm, LoginForm
from flask_blog.models import User, Post


posts=[
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


@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            # image_file=form.image_file.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == '123456789':
            flash('you have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('wrong email or password', 'danger')
    return render_template('login.html', title='Login', form=form)