#################
#### imports ####
#################

from flask import render_template, Blueprint, request, flash, redirect, url_for
from flask_login import login_user, current_user, login_required, logout_user

from .forms import RegisterForm, LoginForm
from project.models import User
from project import db


################
#### config ####
################

users_blueprint = Blueprint('users', __name__)


################
#### routes ####
################

@users_blueprint.route('/')
def index():
    return render_template('index.html')


@users_blueprint.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_user = User(form.email.data, form.password.data)
        new_user.authenticated = True
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash('Thanks for registering, {}!'.format(new_user.email))
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.is_correct_password(form.password.data):
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Thanks for logging in, {}!'.format(current_user.email))
            return redirect(url_for('users.profile'))
        else:
            flash('ERROR! Incorrect login credentials.')
    return render_template('login.html', form=form)


@users_blueprint.route('/logout')
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    flash('Goodbye!')
    return redirect(url_for('users.index'))
