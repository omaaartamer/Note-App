from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
auth = Blueprint('auth', __name__)

@auth.route('/login',methods = ['GET', 'POST'])
def login():
    data = request.form
    print(data)
    print(request.form)
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        print(email)
        print(password)
        # Add logic to check the user's credentials
        user = User.query.filter_by(email=email).first()
        print(user)
        if user:
            if check_password_hash(user.password, password):
                flash('Login successful!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Login failed. Check your email and password.', category='error')
        else:
            flash('User does not exist.', category='error')
    return render_template('login.html', user=current_user)

@auth.route('logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up',methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')         
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        print(email)
        print(password1)
        # Add logic to save the user to the database
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # Add logic to save the user to the database
            new_user = User(email=email, firstName=firstName, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
        # If the user already exists, show an error message
                
    return render_template("sign_up.html",user = current_user)