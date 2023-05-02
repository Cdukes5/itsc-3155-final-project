from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, UserMixin, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

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

# Define the Session model
class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    session_key = db.Column(db.String(80), unique=True)

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
    error = None
    if request.method == 'POST':
        # Get the user's information from the form
        email = request.form['email']
        password = request.form['password']

        # Update the user's email and password in the database
        current_user.email = email
        current_user.password = generate_password_hash(password)
        db.session.commit()

        # Redirect the user to their updated profile
        return redirect(url_for('profile'))

    # If the request method is GET, render the profile template
    return render_template('user.html', current_user=current_user, error=error)

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