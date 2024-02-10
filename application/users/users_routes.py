from flask import Blueprint, render_template, redirect, url_for, flash
from ..forms import LoginForm
from ..models import db, User
from .. import login_manager
from flask_login import login_user, logout_user, login_required

users_bp = Blueprint(
    name='users_bp',
    import_name=__name__,
    template_folder='templates'
)


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        existing_user = User.query.filter(User.username == login_form.username.data).first()
        print(existing_user)
        if existing_user and existing_user.check_password(login_form.password.data):
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


@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_bp.home'))


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('users_bp.login'))
