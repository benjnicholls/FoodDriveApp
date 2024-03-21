from flask import Blueprint, render_template, redirect, url_for, flash, request
from ..forms import LoginForm, RegisterForm
from ..models import User
from .. import login_manager
from .. import db
from ..decorators import admin_required
from flask_login import login_user, logout_user, login_required
from datetime import datetime as dt

users_bp = Blueprint(
    name='users_bp',
    import_name=__name__,
    template_folder='templates'
)


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if request.method == 'POST' and login_form.validate():
        existing_user = User.query.filter(User.username == login_form.username.data).first()

        if existing_user and existing_user.check_password(login_form.password.data):
            existing_user.last_login = dt.now()
            existing_user.created_on = dt.now()
            print("changed last_login")
            db.session.commit()
            print("commited")
            login_user(existing_user)
            return redirect(url_for('home_bp.home'))
        else:
            flash("Username/Password combination didn't work. Please try again.")

    return render_template(
        template_name_or_list='login.html',
        form=login_form,
        title='Login page',
        description='Webpage for logging in users.'
    )


@users_bp.route('/register', methods=['GET', 'POST'])
@admin_required
def register():
    register_form = RegisterForm()
    if request.method == 'POST' and register_form.validate():
        if User.query.filter(User.username == register_form.username.data).first():
            flash("Username already taken. Choose another.")
        else:
            new_user = User(
                username=register_form.username.data,
            )
            new_user.set_password(register_form.password.data)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('home_bp.home'))

    return render_template(
        template_name_or_list='register.html',
        form=register_form,
        title='Registration page',
        description='Webpage for registering new users.'
    )


@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_bp.home'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id) if user_id is not None else None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('users_bp.login'))
