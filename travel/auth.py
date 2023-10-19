# Import necessary modules
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from flask_bcrypt import generate_password_hash, check_password_hash

# Import custom modules
from .forms import LoginForm, RegisterForm
from .models import User
from . import db

# Create a Blueprint
auth_bp = Blueprint('auth', __name__)

# Registration route
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    registration_form = RegisterForm()

    # Check if the form is submitted and valid
    if registration_form.validate_on_submit():
        # Get user input from the form
        username = registration_form.user_name.data
        password = registration_form.password.data
        email = registration_form.email_id.data

        # Check if a user with the same username exists
        existing_user = User.query.filter_by(name=username).first()
        if existing_user:
            flash('Username already exists, please try another.')
            return redirect(url_for('auth.register'))

        # Hash the password before storing it
        hashed_password = generate_password_hash(password)

        # Create a new User object and add it to the database
        new_user = User(name=username, password_hash=hashed_password, emailid=email)
        db.session.add(new_user)
        db.session.commit()

        # Redirect to the main page after successful registration
        return redirect(url_for('main.index'))

    # Render the registration form if it's a GET request
    return render_template('user.html', form=registration_form, heading='Register')

# Login route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    error = None

    if login_form.validate_on_submit():
        # Get user input from the form
        user_name = login_form.user_name.data
        password = login_form.password.data

        # Query the database to find the user by username
        user = User.query.filter_by(name=user_name).first()

        # Check if the user exists
        if not user:
            error = 'Incorrect username or password.'
        else:
            # Check the password hash
            if not check_password_hash(user.password_hash, password):
                error = 'Incorrect username or password.'

        if error is None:
            # Authenticate the user and redirect to the main page
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash(error)

    # Render the login form if it's a GET request
    return render_template('user.html', form=login_form, heading='Login')

# Logout route
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
