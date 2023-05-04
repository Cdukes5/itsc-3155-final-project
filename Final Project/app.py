from flask import Flask, render_template, request, session, redirect, url_for, flash, get_flashed_messages, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import LoginManager, current_user, login_user, UserMixin, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import DataRequired
import secrets
from datetime import datetime

app = Flask(__name__)

# Configure Flask app to use MySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/flasksql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'mykey'

db = SQLAlchemy(app)

# Get the current_user
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Function to generate user session key

def generate_session_key():
    return secrets.token_hex(16)

# MODELS

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def get_id(self):
        return str(self.id)
    @property
    def is_authenticated(self):
        return True

# Define the Forum model    
class Forum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


# Define the Post model    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    username = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)

# Define the Thread model
class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    forum_id = db.Column(db.Integer, db.ForeignKey('forum.id'), nullable=False)
    username = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)
    forum = db.relationship('Forum', backref=db.backref('threads', lazy=True))

# Define the Session model
class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    session_key = db.Column(db.String(80), unique=True)

class ThreadForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    image = FileField('Image')

class PostForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    image = FileField('Image')

# TEMPLATES

# Template routes

@app.route('/')
def home():
        print(current_user.is_authenticated)
        return render_template('home.html', current_user=current_user)

@app.route('/about')
def about():
    return render_template('about.html', current_user=current_user)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get the user's information from the form
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Generate a password hash for the user's password
        password_hash = generate_password_hash(password)

        # Create a new user object with the information from the form
        new_user = User(username=username, email=email, password=password_hash)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Redirect the user to the login page
        return redirect(url_for('login'))
    
    # If the request method is GET, render the sign-up form template
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # Get the user's information from the form
        username = request.form['username-login']
        password = request.form['password-login']
        # Find the user in the database
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            # Log the user in and store their information in a session
            login_user(user)
            session['user_id'] = user.id
            session['session_key'] = generate_session_key()
            session_data = Session(user_id=user.id, session_key=session['session_key'])
            db.session.add(session_data)
            db.session.commit()
            return redirect(url_for('home'))
        # If not found
        else:
            error = 'Invalid username or password'
    return render_template('login.html', error=error)

@app.route('/user', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        if 'update_email' in request.form:
            # Get the user's new email from the form
            new_email = request.form['email']
            # Update the user's email in the database
            current_user.email = new_email
            db.session.commit()
            flash('Your email has been updated!', 'success')
        elif 'update_password' in request.form:
            # Get the user's current password, new password, and confirm password from the form
            current_password = request.form['current_password']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']
            # Check if the current password is correct
            if not check_password_hash(current_user.password, current_password):
                flash('Incorrect current password', 'error')
            # Check if the new password and confirm password match
            elif new_password != confirm_password:
                flash('New password and confirm password must match', 'error')
            else:
                # Generate a new password hash for the user's new password
                new_password_hash = generate_password_hash(new_password)
                # Update the user's password hash in the database
                current_user.password = new_password_hash
                db.session.commit()
                flash('Your password has been updated!', 'success')
    return render_template('user.html', current_user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/contact')
def contact():
    return render_template('contact.html', current_user=current_user)

@app.route('/career')
def career():
    return render_template('career.html', current_user=current_user)

# Forum routes

#Display forums in the database
@app.route('/forum')
@login_required
def forums():
    forums = Forum.query.all()
    return render_template('forum.html', forums=forums)

# Route for displaying the threads in a forum
@app.route('/forum/<int:forum_id>')
def forum(forum_id):
    forum = Forum.query.get(forum_id)
    threads = Thread.query.filter_by(forum_id=forum_id).all()
    return render_template('threads.html', forum=forum, threads=threads)

# Route for displaying the posts in a thread
@app.route('/thread/<int:thread_id>')
def thread(thread_id):
    thread = Thread.query.get(thread_id)
    user = User.query.get(thread.username)
    posts = Post.query.filter_by(thread_id=thread_id).all()
    return render_template('posts.html', thread=thread, posts=posts, user=user)

# Route for creating a new thread
@app.route('/forum/<int:forum_id>/new_thread', methods=['GET', 'POST'])
def new_thread(forum_id):
    forum = Forum.query.get(forum_id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        thread = Thread(title=title, content=content, forum_id=forum_id, username=current_user.username)
        db.session.add(thread)
        db.session.commit()
        return redirect(url_for('thread', thread_id=thread.id))

    return render_template('new_thread.html', forum=forum)

# Route for creating a new post
@app.route('/thread/<int:thread_id>/new_post', methods=['GET', 'POST'])
def new_post(thread_id):
    thread = Thread.query.get(thread_id)
    if request.method == 'POST':
        content = request.form['content']
        user_id = current_user.id
        post = Post(content=content, username=current_user.username, thread_id=thread_id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('thread', thread_id=thread_id))
    else:
        return render_template('new_post.html', thread=thread)
    
# Route for editing a thread    
@app.route('/edit_thread/<int:thread_id>', methods=['GET', 'POST'])
@login_required
def edit_thread(thread_id):
    thread = Thread.query.get_or_404(thread_id)
    if current_user.username != thread.username:
        abort(403)
    form = ThreadForm(obj=thread)
    if form.validate_on_submit():
        form.populate_obj(thread)
        db.session.commit()
        flash('Your thread has been updated.', 'success')
        return redirect(url_for('thread', thread_id=thread.id))
    return render_template('edit_thread.html', form=form, thread=thread)

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.username != post.username:
        abort(403)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        form.populate_obj(post)
        db.session.commit()
        flash('Your thread has been updated.', 'success')
        return redirect(url_for('thread', thread_id=post.thread_id))
    return render_template('edit_post.html', form=form, post=post)