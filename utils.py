from extensions import db
from sqlalchemy.sql import func
from model import Customer
from PIL import Image
from pyzbar.pyzbar import decode


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



