from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required
from ..forms import CheckInForm, AddForm
from ..models import db, Customer, CheckIn, AddedCustomer
from .. import driver
from datetime import datetime as dt
import os
from subprocess import getoutput
from pyzbar.pyzbar import decode
from PIL import Image
from pandas import read_csv

check_in_bp = Blueprint(
    name='check_in_bp',
    import_name=__name__,
    template_folder='templates'
)


def read_barcode(image_path):
    try:
        img = decode(Image.open(image_path))
    except FileNotFoundError as e:
        print(e)
    else:
        return str(img[0].data, 'utf-8')[4:]


def check_in_customer(customer_id, engine):
    if not isinstance(customer_id, int):
        raise TypeError("Customer_id needs to be an integer")
    customer_to_be_added = engine.get_or_404(Customer, customer_id)
    engine.session.add(customer_to_be_added)
    engine.session.commit()


def format_csv():
    with open(getoutput('find . -name "export*"'), 'r') as file:
        try:
            data_df = read_csv(file)
            formatted_df = data_df[['active_family_size', 'family_id', 'HOH_first_name', 'HOH_last_name',
                                    'dob', 'age', 'address1', 'address2', 'zip']]
        except FileNotFoundError as e:
            return e

        return formatted_df


@check_in_bp.route('/check-in', methods=['GET', 'POST'])
@login_required
def check_in():
    check_in_form = CheckInForm()
    if check_in_form.validate_on_submit():
        barcode_file = check_in_form.input_file
        customer_name = check_in_form.first_name
        if barcode_file:
            barcode_id = read_barcode(barcode_file)
            search_result = db.session.execute(db.Select(Customer).where(Customer.family_id == barcode_id)).scalar()
            return redirect(url_for('check_in_bp.display_checked_in', id=search_result.id))
        elif customer_name:
            search_result = db.session.execute(db.Select(Customer).where(Customer.HOH_first_name == customer_name))
            return render_template(
                template_name_or_list='check-in.html',
                table_data=search_result.scalars()
            )

    return render_template(
        template_name_or_list='check-in.html',
        form=check_in_form
    )


@check_in_bp.route('/all-checked-in')
@login_required
def display_checked_in():
    if request.args.get('id'):
        customer = db.get_or_404(Customer, request.args.get('id'))
        check_in_table = CheckIn(customer=customer)
        db.session.add(check_in_table)
        db.session.commit()
        return redirect(url_for('check_in_bp.display_checked_in'))

    customer_data = db.session.execute(db.select(CheckIn).filter_by(new_customer_id=None)).scalars()
    new_customer_data = db.session.execute(db.select(CheckIn).filter_by(customer_id=None)).scalars()

    return render_template(
        template_name_or_list='check-in-table.html',
        customers=customer_data,
        new_customers=new_customer_data,
        date=dt.now().strftime('%B %d, %Y')
    )


@check_in_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    add_form = AddForm()
    if add_form.validate_on_submit():

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
        flash('Success!')
        return redirect(url_for('check_in_bp.add'))
    return render_template('add.html', form=add_form)


@check_in_bp.get('/update')
@login_required
def update_db():
    driver.update()
    format_csv().to_sql('customer', db.engine, if_exists='replace', index=False)
    os.remove(getoutput('find . -name "export*"'))
    return jsonify({'status': 'success'})
