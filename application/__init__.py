from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .webdriver import WebDriverSingleton
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager

db = SQLAlchemy()
driver = WebDriverSingleton()
bootstrap = Bootstrap5()
login_manager = LoginManager()


def init_app():  # sourcery skip: extract-method
    application = Flask(__name__, instance_relative_config=False)
    application.config.from_object('config.Config')

    db.init_app(application)
    bootstrap.init_app(application)
    login_manager.init_app(application)

    with application.app_context():
        from .home import home_routes
        from .users import users_routes
        from .check_in import check_in_routes

        db.create_all()

        application.register_blueprint(home_routes.home_bp)
        application.register_blueprint(users_routes.users_bp)
        application.register_blueprint(check_in_routes.check_in_bp)

        return application
