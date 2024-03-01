from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed, FileSize
from wtforms import validators
from wtforms.fields.simple import StringField, PasswordField, BooleanField, EmailField

from config import images, image_max_size


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired()])
    remember = BooleanField('Remember Me')


class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25), validators.DataRequired()])
    email = EmailField('Email Address', [validators.Length(min=6, max=35), validators.DataRequired()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    image = FileField('Profile Picture', [validators.Optional(), FileAllowed(images, 'Images only!'), FileSize(max_size=image_max_size)])
    # The profile picture must be a .jpg file and must not contain any slashes, periods or backslashes
    recaptcha = RecaptchaField(validators=[validators.DataRequired()])


class AddBookForm(FlaskForm):
    title = StringField('Title', [validators.Length(min=1, max=200), validators.DataRequired()])
    author = StringField('Author', [validators.Length(min=1, max=100), validators.DataRequired()])
    genre = StringField('Genre', [validators.Length(min=1, max=120), validators.DataRequired()])
    year = StringField('Year', [validators.Length(min=4, max=4), validators.DataRequired()])
    isbn = StringField('ISBN', [validators.Length(min=13, max=13), validators.DataRequired()])
    image = FileField('Book Image', [validators.Optional(), FileAllowed(images, 'Images only!'), FileSize(max_size=image_max_size)])
    summary = StringField('Summary', [validators.Length(min=1, max=1500), validators.DataRequired()])
    price = StringField('Price', [validators.Length(min=1, max=4), validators.Optional()])
    stock = StringField('Stock', [validators.Length(min=1, max=6), validators.Optional()])
