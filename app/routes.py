from flask import Blueprint, request, redirect, url_for, render_template, flash, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db, mail  # Import db and mail directly from __init__.py
import random
from flask_mail import Message

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/login/user')
def login_user():
    return render_template('user/login_options.html')

@main.route('/login/admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Verify admin credentials
        if email == current_app.config['ADMIN_EMAIL'] and password == current_app.config['ADMIN_PASSWORD']:
            #flash('Admin login successful!', 'success')
            return redirect(url_for('main.admin_dashboard'))  # Redirect to admin dashboard
        else:
            flash('Invalid admin credentials', 'danger')

    return render_template('admin/login.html')

@main.route('/user/dashboard', methods=['GET', 'POST'])
def user_dashboard():
    return render_template('user/home.html')

@main.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    return render_template('admin/dashboard.html')

@main.route('/login/user/form', methods=['GET', 'POST'])
def user_login_form():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Query the database for the user
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):  # Use hashed password verification
            # Log the user in
            session['user_id'] = user.id
            session['username'] = user.username
            #flash('Login successful!', 'success')
            return redirect(url_for('main.user_dashboard'))  # Redirect to user dashboard
        else:
            flash('Invalid email or password', 'danger')

    return render_template('user/login_form.html')

@main.route('/register/user', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please log in.', 'danger')
            return redirect(url_for('main.user_login_form'))

        # Hash the password before saving
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Log the user in automatically
        session['user_id'] = new_user.id
        session['username'] = new_user.username
        #flash('Registration successful! Welcome to your dashboard.', 'success')
        return redirect(url_for('main.user_dashboard'))

    return render_template('user/register.html')

@main.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('Email not found. Please register first.', 'danger')
            return redirect(url_for('main.user_register'))

        reset_code = str(random.randint(100000, 999999))
        session['reset_code'] = reset_code
        session['reset_email'] = email

        # Send the reset code via email
        try:
            msg = Message('Password Reset Code',
                          sender='your_email@gmail.com',
                          recipients=[email])
            msg.body = f'Your password reset code is: {reset_code}'
            mail.send(msg)
            flash('A reset code has been sent to your email.', 'success')
            return redirect(url_for('main.reset_password'))
        except Exception as e:
            flash('Failed to send email. Please try again later.', 'danger')
            print(f"Error: {e}")

    return render_template('user/forgot_password.html')

@main.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        entered_code = request.form.get('reset_code')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Verify the reset code
        if entered_code != session.get('reset_code'):
            flash('Invalid reset code. Please try again.', 'danger')
            return redirect(url_for('main.reset_password'))

        # Verify the new password and confirm password match
        if new_password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('main.reset_password'))

        # Update the user's password in the database
        email = session.get('reset_email')
        user = User.query.filter_by(email=email).first()
        if user:
            hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')
            user.password = hashed_password
            db.session.commit()
            flash('Password reset successful! You can now log in with your new password.', 'success')
            return redirect(url_for('main.user_login_form'))

    return render_template('user/reset_password.html')