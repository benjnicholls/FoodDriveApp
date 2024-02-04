from flask_wtf import FlaskForm
from wtforms.fields import IntegerField, StringField, SubmitField, PasswordField, SelectField, FileField
from wtforms.validators import InputRequired, Length


class BetterIntegerField(IntegerField):
    render_kw = {"pattern": "[0-9]*", "input mode": "numeric"}


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[InputRequired(message='Username is required')])
    password = PasswordField(label='Password', validators=[InputRequired(message='Password is required'),])
    submit = SubmitField('Login')


class CheckInForm(FlaskForm):
    input_file = FileField(label='Capture Barcode')
    first_name = StringField(label='First Name')
    submit_barcode = SubmitField('Search')
    submit_name = SubmitField('Search')


class AddForm(FlaskForm):
    f_name = StringField(
        label='First Name',
        validators=[
            InputRequired(message='First Name required')
        ]
    )
    l_name = StringField(
        label='Last Name',
        validators=[
            InputRequired(message='Last Name required')
        ]
    )
    address = StringField(
        label='Street Address',
        validators=[
            InputRequired(message='Address required')
        ]
    )
    zipcode = BetterIntegerField(
        label='Zipcode',
        validators=[
            InputRequired(message='Zipcode required'),
            Length(min=5, max=10, message='Zipcode must be at least 5 characters long and a maximum of 10')
        ]
    )
    seniors = BetterIntegerField(label='Seniors')
    adults = BetterIntegerField(
        label='Adults',
        validators=[InputRequired()]
    )
    children = BetterIntegerField(label='Children')
    age = BetterIntegerField(
        label='Age',
        validators=[InputRequired()]
    )
    homeless = SelectField(
        label='Homeless',
        choices=[('False', 'No'), ('True', 'Yes')],
    )
    language = SelectField(
        label='Language',
        choices=[('Blank', '-Select-'), ('English', 'English'), ('Spanish', 'Spanish')],
        validators=[InputRequired()]
    )
    submit = SubmitField('Add')
