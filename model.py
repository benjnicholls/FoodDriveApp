from flask_login import UserMixin
from extensions import db
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    active_family_size = db.Column(db.Integer, nullable=False)
    family_id = db.Column(db.Integer, nullable=False, unique=True)
    HOH_first_name = db.Column(db.String(250))
    HOH_last_name = db.Column(db.String(250))
    dob = db.Column(db.String(250))
    age = db.Column(db.Integer)
    address1 = db.Column(db.Text)
    address2 = db.Column(db.String(250))
    zip = db.Column(db.Integer)
    phone_number = db.Column(db.Integer)
    current_selected_form_language = db.Column(db.String(250))


class AddedCustomer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(250), nullable=False)
    l_name = db.Column(db.String(250), nullable=False)
    address = db.Column(db.Text, nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)
    seniors = db.Column(db.Integer, nullable=False)
    adults = db.Column(db.Integer, nullable=False)
    children = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    homeless = db.Column(db.Boolean, nullable=False)
    language = db.Column(db.String(250), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.now)


class CheckIn(db.Model):
    __tablename__ = 'check_ins'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    customer = db.relationship('Customer', backref='check_ins')
    new_customer_id = db.Column(db.Integer, db.ForeignKey('added_customer.id'))
    new_customer = db.relationship('AddedCustomer', backref='check_ins')
    checkin_date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"CheckIn({self.id}, {self.customer.HOH_first_name}, {self.checkin_date})"