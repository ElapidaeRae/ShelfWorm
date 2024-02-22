import time
from datetime import timedelta
from re import escape

import requests
from flask import Flask, render_template, request, redirect, url_for, session, g, blueprints
import flask_login
import stripe
import scrypt
import sqlite3
import manage
from api import api

# Create a new Flask application
app = Flask(__name__)
# Set the secret key to some random bytes. For production, a random key should be used
app.secret_key = 'According to all known laws of aviation, there is no way a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyway because bees don\'t care what humans think is impossible.'

app.register_blueprint(api, url_prefix='/api')

# Create a login manager instance to manage the user session
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Set the stripe keys for the stripe API which will be used to process payments
stripe_keys = {
    'secret_key': 'sk_test_4eC39HqLyjWDarjtT1zdp7dc',
    'publishable_key': 'pk_test_TYooMQauvdEDq54NiTphI7jx'
}

# Set the stripe API key
stripe.api_key = stripe_keys['secret_key']


class User(flask_login.UserMixin):
    pass

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = manage.Database('Database.db')
    return db

@login_manager.user_loader
def user_loader(username):
    db = get_db()
    user = db.get_user(username)
    if user is None:
        return

    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    db = get_db()
    user = db.get_user(username)
    if user is None:
        return

    user = User()
    user.id = username
    return user


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    image = request.form['image']
    db = manage.Database('Database.db')
    try:
        db.add_user(username, password, email, image)
    except sqlite3.IntegrityError:
        return 'Username already exists'
    # Post-Registration, log the user in then redirect to the index page
    user = User()
    user.id = username
    flask_login.login_user(user)
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    db = get_db()
    username = request.form['username']
    users = db.get_user(username)
    salt = db.get_password_salt(request.form['password'])
    
    inputted_password = scrypt.hash(request.form['password'], salt)
    actual_password = db.get_user_password(username)
    if users is None:
        return 'User not found'
    if inputted_password == actual_password:
        user = User()
        user.id = username
        remember = request.form.get('remember')
        if remember:
            flask_login.login_user(user, remember=True, duration=timedelta(days=3))
        else:
            flask_login.login_user(user, remember=False)
        return redirect(url_for('profile'))
    return redirect(url_for('login'))

@app.route('/profile')
@flask_login.login_required
def profile():
    return render_template('profile.html')


# The search page for the book store will dynamically display the search results when the user types in the search bar
@app.route('/search')
def search():
    return render_template('search.html')


# The book page will display the details of a book when the user clicks on a book in the search results
@app.route('/book/<isbn>', methods=['GET'])
def book(isbn):
    # Get the book details from the database using the API
    book_url = url_for('api.book', isbn=isbn)
    book_data = requests.get(book_url).json()
    return render_template('book.html', book=book_data)


@app.route('/checkout', methods=['GET', 'POST'])
@flask_login.login_required
def checkout():
    # Use the stripe Checkout system to process the payment
    # The payment amount is hardcoded to £20 for testing purposes
    amount = 2000
    if request.method == 'POST':
        # Get the token from the form
        token = request.form['stripeToken']
        # Create a charge using the token
        charge = stripe.Charge.create(
            amount=amount,
            currency='gbp',
            description='Example charge',
            source=token,
        )
        return redirect(url_for('checkout_confirmation'))
    return render_template('checkout.html', stripe_keys=stripe_keys, amount=amount)


@app.route('/checkout_confirmation')
@flask_login.login_required
def checkout_confirmation():
    return render_template('checkout_confirmation.html')


@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/about')
def about():
    return render_template('about.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



if __name__ == '__main__':
    app.run(debug=True)
