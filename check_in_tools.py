from extensions import db
from sqlalchemy.sql import func
from model import Customer
from PIL import Image
from pyzbar.pyzbar import decode
from subprocess import getoutput
import pandas as pd


def sum_family_count():
    return db.session.query(func.sum(Customer.active_family_size)).scalar()


def read_barcode(image_path):
    try:
        img = decode(Image.open(image_path))
    except FileNotFoundError as e:
        print(e)
    else:
        return str(img[0].data, 'utf-8')[4:]


def check_in_customer(customer_id):
    customer_to_be_added = db.get_or_404(Customer, customer_id)
    db.session.add(customer_to_be_added)


def format_csv():
    with open(getoutput('find . -name "export*"'), 'r') as file:
        data_df = pd.read_csv(file)
        formatted_df = data_df[['active_family_size', 'family_id', 'HOH_first_name', 'HOH_last_name',
                                'dob', 'age', 'address1', 'address2', 'zip']]
        return formatted_df

format_csv()
