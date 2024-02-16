from re import escape

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

# Hardcoded users for the login system (for testing purposes)
users = {'admin': {'password': 'admin'},
         'user': {'password': 'user'},
         'test': {'password': 'test'}}


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return

    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if username not in users:
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
    # Add the new user to the users database
    users[username] = {'password': password}
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    if request.form['password'] == users[username]['password']:
        user = User()
        user.id = username
        remember = request.form.get('remember')
        if remember:
            flask_login.login_user(user, remember=True)
        else:
            flask_login.login_user(user)
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


@app.route('/search_results/<search_query>')
def search_results(search_query):
    # Get the search results from the database
    # This is a placeholder for the actual search results
    search_results = [
        {'title': 'Search Result 1', 'description': 'This is the first search result'},
        {'title': 'Search Result 2', 'description': 'This is the second search result'},
        {'title': 'Search Result 3', 'description': 'This is the third search result'},
        {'title': 'Search Result 4', 'description': 'This is the fourth search result'},
        {'title': 'Search Result 5', 'description': 'This is the fifth search result'}
    ]
    return render_template('search_results.html', search_query=search_query, search_results=search_results)


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



if __name__ == '__main__':
    app.run(debug=True)
