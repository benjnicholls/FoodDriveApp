from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, IntegerField, PasswordField,
                     SelectField)
from wtforms.validators import DataRequired


class BetterIntegerField(IntegerField):
    render_kw = {"pattern": "[0-9]*", "input mode": "numeric"}


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')


class AddForm(FlaskForm):
    f_name = StringField('First Name', validators=[DataRequired()])
    l_name = StringField('Last Name', validators=[DataRequired()])
    address = StringField('Street Address', validators=[DataRequired()])
    zipcode = BetterIntegerField('Zipcode', validators=[DataRequired()])
    seniors = BetterIntegerField('Seniors')
    adults = BetterIntegerField('Adults', validators=[DataRequired()])
    children = BetterIntegerField('Children')
    age = BetterIntegerField('Age', validators=[DataRequired()])
    homeless = SelectField('Homeless', choices=[('False', 'No'), ('True', 'Yes')], validators=[DataRequired()])
    language = SelectField('Language', choices=[('Blank', '-Select-'), ('English', 'English'), ('Spanish', 'Spanish')],
                           validators=[DataRequired()])
    submit = SubmitField('Add')
