from . import login_manager
from functools import wraps
from flask_login import current_user


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if (
            not current_user.is_authenticated
            and current_user.username != 'bnicholls'
        ):
            return login_manager.unauthorized()
        return func(*args, **kwargs)

    return decorated_view
