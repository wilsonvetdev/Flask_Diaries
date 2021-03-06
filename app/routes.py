from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, AddPostForm, UpdatePostForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from werkzeug.urls import url_parse

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    addPostForm = AddPostForm()

    if addPostForm.validate_on_submit():
        post = Post(title=addPostForm.title.data, body=addPostForm.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    
    posts = current_user.posts.order_by(Post.timestamp.desc())

    return render_template('index.html', title='Home', addPostForm=addPostForm, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password. Please try again!')
            return redirect(url_for('login'))

        login_user(user)
        flash(f'Login Success! Login requested for user {form.username.data}.')

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Log In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user! Please log in with your credentials.')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route('/post/<post_id>/update', methods=['GET', 'POST'])
@login_required
def update(post_id):
    form = UpdatePostForm()
    post = Post.query.filter_by(id=post_id).first()

    if request.method == 'GET':
        form.title.data = post.title 
        form.body.data = post.body

    if form.validate_on_submit():
        if post:
            db.session.delete(post)
            db.session.commit()

            title = form.title.data
            body = form.body.data
            updated_post = Post(id=post_id, author=current_user, title=title, body=body)
            db.session.add(updated_post)
            db.session.commit()
            
            flash('Your post is successfully updated!')
            return redirect(url_for('index'))

    return render_template('_post.html', post=post, form=form)

@app.route('/post/<post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete(post_id):

    post = Post.query.filter_by(id=post_id).first()

    if post and post.author == current_user:
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('index'))
    
    return redirect(url_for('index'))