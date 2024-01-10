from datetime import datetime

from flask import Flask, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from forms import LoginForm, RegisterForm, AddForm
from model import User, Customer, AddedCustomer, CheckIn
from extensions import db, login_manager, bootstrap
from check_in_tools import sum_family_count, read_barcode
import os
from dotenv import load_dotenv

load_dotenv()
application = Flask(__name__)
application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///food-drive.db"
application.secret_key = os.getenv('APP_SECRET_KEY')
login_manager.init_app(application)
db.init_app(application)
bootstrap.init_app(application)

with application.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


@application.route('/')
def home():
    return render_template('index.html', residents=sum_family_count())


@application.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()

    if request.method == "POST":
        username = request.form.get('username')
        existing_user = db.session.query(User).filter(User.username == username).first()

        if existing_user is None:
            # noinspection PyArgumentList
            new_user = User(username=username,
                            password_hash=generate_password_hash(request.form.get('password')))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)

            return redirect(url_for('home'))
        else:
            flash('Username already exists. Please try again.')

    return render_template('register.html', form=register_form)


@application.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if request.method == 'POST':
        form_data = request.form.to_dict()
        if current_user := db.session.execute(
                db.Select(User).where(User.username == form_data["username"])
        ).scalar():
            if check_password_hash(current_user.password_hash, form_data['password']):
                login_user(current_user)
                return redirect(url_for('home'))
            else:
                flash('Password incorrect. Please try again.')
        else:
            flash('User does not exist. Please try again.')

    return render_template('login.html', form=login_form)


@application.route('/check-in', methods=['GET', 'POST'])
@login_required
def check_in():
    if request.method == 'POST':
        barcode_file = request.files['inputFile']
        customer_name = request.form.to_dict()['firstName']
        if barcode_file:
            barcode_id = read_barcode(barcode_file)
            search_result = db.session.execute(db.Select(Customer).where(Customer.family_id == barcode_id)).scalar()
            return redirect(url_for('display_checked_in', id=search_result.id))
        elif customer_name:
            search_result = db.session.execute(db.Select(Customer).where(Customer.HOH_first_name == customer_name))
            return render_template('check-in.html', table_data=search_result.scalars())

    return render_template('check-in.html')


@application.route('/all-checked-in')
def display_checked_in():
    if request.args.get('id'):
        customer = db.get_or_404(Customer, request.args.get('id'))
        check_in_table = CheckIn(customer=customer)
        db.session.add(check_in_table)
        db.session.commit()
        return redirect(url_for('display_checked_in'))

    customer_data = db.session.execute(
        db.select(CheckIn).filter_by(new_customer_id=None)).scalars()
    new_customer_data = db.session.execute(
        db.select(CheckIn).filter_by(customer_id=None)).scalars()

    return render_template('check-in-table.html', customers=customer_data,
                           new_customers=new_customer_data, date=datetime.now)


@application.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    add_form = AddForm()
    if add_form.validate_on_submit():
        print("hooray!")
        # Create a new AddedCustomer object with data from the form
        new_customer = AddedCustomer(
            f_name=add_form.f_name.data,
            l_name=add_form.l_name.data,
            address=add_form.address.data,
            zipcode=add_form.zipcode.data,
            seniors=add_form.seniors.data,
            adults=add_form.adults.data,
            children=add_form.children.data,
            age=add_form.age.data,
            homeless=bool(add_form.homeless.data),
            language=add_form.language.data
        )
        check_in_table = CheckIn(new_customer=new_customer)

        # Add new customer to the database and commit changes
        db.session.add(new_customer)
        db.session.add(check_in_table)
        db.session.commit()

        # Redirect to a success page or display a confirmation
        print("success")
        flash('Success!')
        return redirect(url_for('add'))
    return render_template('add.html', form=add_form)


@application.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == "__main__":
    application.run(debug=True, port=5000)
