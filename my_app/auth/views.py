import functools
from flask import request, render_template, flash, redirect, url_for, session, Blueprint, abort
from my_app import app, db, login_manager
from my_app.auth.models import User, RegistrationForm, LoginForm
from flask import g
from flask_login import current_user, login_user, logout_user, login_required





auth = Blueprint('auth', __name__)

@auth.route('/')
@auth.route('/home')
def home():
    return render_template('home.html')

def has_role(name):
    def real_decorator(f):
        def wraps(*args, **kwargs):
            if current_user.has_role(name):
                return f(*args, **kwargs)
            else:
                abort(403)
        return functools.update_wrapper(wraps, f)
    return real_decorator


@auth.route('/register', methods=['GET', 'POST'])
@login_required
@has_role('admin')
def register():
    if session.get('username'):
        flash('You are already logged in.', 'info')
        return redirect(url_for('auth.home'))

    form =  RegistrationForm()

    if form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash('This username has been already taken. Try another one.', 'warning')

        user = User(username, password)
        db.session.add(user)
        db.session.commit()
        flash('You are now registered. Please login.', 'success')
        return redirect(url_for('auth.login'))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        flash('You are already loged in.', 'info')
        return redirect(url_for('auth.home'))

    form = LoginForm()
    if form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')
        existing_user = User.query.filter_by(username=username).first()

        if not (existing_user and existing_user.check_password(password)):
            flash('Invalid username or password. Please try again.', 'danger')
            return render_template('login.html', form=form)

        login_user(existing_user, remember=True)
        flash('You have successfuly logged in.', 'success')
        return redirect(url_for('auth.home'))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('login.html', form=form)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.home'))


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@auth.before_request
def get_current_user():
    g.user = current_user
