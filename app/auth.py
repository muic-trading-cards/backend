from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from . import db
import re
from app.schema import *
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    session = Session()

    user = session.query(User).filter_by(email=email).first()

    # check if user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    session.close()
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/register')
def register():
    return render_template('register.html')

@auth.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    password = request.form.get('password')


    session = Session()

    user = session.query(User).filter_by(email=email).first() # if this returns a user, then the email already exists in database
    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.register'))

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if not re.fullmatch(regex, email): # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address is not a valid address, please enter a valid Email address')
        return redirect(url_for('auth.register'))

    if len(password) < 8:
        flash('Password must be at least 8 characters long')
        return redirect(url_for('auth.register'))
    

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, password=generate_password_hash(password, method='sha256'), first_name=first_name, last_name=last_name, permission_level=1)

    # add the new user to the database
    session.add(new_user)
    session.commit()

    session.close()
    return redirect(url_for('auth.login'))



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/admin')
def admin():
    return render_template('admin.html')