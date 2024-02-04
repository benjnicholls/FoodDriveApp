from ..models import db, Customer
from sqlalchemy.sql import func
from flask import Blueprint, render_template

home_bp = Blueprint(
    name='home_bp',
    import_name=__name__,
    template_folder='templates'
)


@home_bp.route('/')
@home_bp.route('/home')
@home_bp.route('/index')
def home():
    """Homepage"""

    return render_template(
        template_name_or_list='index.html',
        residents=db.session.query(func.sum(Customer.active_family_size)).scalar(),
        title='Homepage',
        description='A homepage for the food drive web application. '
                    'From here, you can login and check in guests or add them.'
    )