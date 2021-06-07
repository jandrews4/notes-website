from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint("auth", __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in sucessfully')
                login_user(user, remember=True)
            else:
                flash('Uh oh!! Dou did a fucko boingo this passwowd is incowwect!!', category='error')
        else:
            flash('Oh no!! Thewe is no account assoswiated with that email!!', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()

        if user:
            flash("emaiw alweady exists OwO", category='error')
        elif len(email) < 4:
            flash("Email must be greater than 3 characters", category='error')
        elif len(firstName) < 2:
            flash("Name must be greater than 1 character", category='error')
        elif password1 != password2:
            flash("uwu you made a fucky wucky a wittle typo in youw passwowd", category='error')
        elif len(password1) < 8:
            flash("password must be greater than 7 characters", category='error')
        else:
            new_user = User(email=email, firstName=firstName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Poggers! You made and account', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'), user=current_user)
    return render_template("signup.html")
