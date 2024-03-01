from datetime import timedelta
from re import escape
import requests
from flask import Flask, render_template, request, redirect, url_for, session, g, blueprints
import flask_login
import stripe
import scrypt
from werkzeug.utils import secure_filename
import manage
from admin import admin
from api import api
from forms import RegistrationForm, LoginForm
import config

# Create a new Flask application
app = Flask(__name__)
# Set the secret key to some random bytes. For production, a random key should be used
app.secret_key = config.secret_key

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(admin, url_prefix='/admin')

# Create a login manager instance to manage the user session
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



# Set the stripe API key
stripe.api_key = config.stripe_keys['secret_key']

# Set the recaptcha parameters
app.config['RECAPTCHA_PARAMETERS'] = config.RECAPTCHA_PARAMETERS
app.config['RECAPTCHA_DATA_ATTRS'] = config.RECAPTCHA_DATA_ATTRS
app.config['RECAPTCHA_PUBLIC_KEY'] = config.RECAPTCHA_PUBLIC_KEY
app.config['RECAPTCHA_PRIVATE_KEY'] = config.RECAPTCHA_PRIVATE_KEY


class User(flask_login.UserMixin):
    pass


@app.before_request
def before_request():
    g.user = flask_login.current_user
    if 'username' in session:
        g.username = session['username']

    else:
        g.username = None
    if 'dark_mode' in session:
        g.dark_mode = session['dark_mode']
    else:
        session['dark_mode'] = False
        g.dark_mode = False


@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


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
    user.role = db.get_user_role(username)
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
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            db = get_db()
            username = form.username.data
            email = form.email.data
            password = form.password.data
            image = form.image.data
            image_name = secure_filename(image.filename)
            if image_name != '':
                image.save('data/' + image_name)
                image = 'data/' + image_name

            db.add_user(username, password, email, image)
            return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            db = get_db()
            username = form.username.data
            users = db.get_user(username)
            salt = db.get_password_salt(form.password.data)
            inputted_password = scrypt.hash(form.password.data, salt)
            actual_password = db.get_user_password(username)
            if users is None:
                return 'User not found'
            if inputted_password == actual_password:
                user = User()
                user.id = username
                remember = form.remember.data
                if remember:
                    flask_login.login_user(user, remember=True, duration=timedelta(days=3))
                else:
                    flask_login.login_user(user, remember=False)
                if 'url' in session:
                    return redirect(session.pop('url'))
                else:
                    return redirect(url_for('profile'))
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/profile')
@flask_login.login_required
def profile():
    session['url'] = url_for('profile')
    return render_template('profile.html')


# The search page for the book store will dynamically display the search results when the user types in the search bar
@app.route('/search')
def search():
    session['url'] = url_for('search')
    return render_template('search.html')


# The book page will display the details of a book when the user clicks on a book in the search results
@app.route('/book/<isbn>', methods=['GET'])
def book(isbn):  # :TODO: Make the book page display the book details
    session['url'] = url_for('book', isbn=isbn)
    # Get the book details from the database
    db = get_db()
    book = db.get_books_by_isbn(isbn)
    if book is None:
        return 'Book not found'
    return render_template('book.html', book=book)



@app.route('/checkout', methods=['GET', 'POST'])
@flask_login.login_required
def checkout():  # :TODO: Add the stripe checkout system to the checkout page and add a checkout page
    session['url'] = url_for('checkout')
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
    return render_template('checkout.html', stripe_keys=config.stripe_keys, amount=amount)


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
    return render_template('about.html')  # :TODO: Add an about page


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
@app.route('/500')
def internal_server_error(e):
    return render_template('errors/500.html'), 500


# Update the session's dark mode setting to what is sent in the request
@app.route('/dark_mode', methods=['POST', 'GET'])
def dark_mode():
    if request.method == 'GET':
        return {'darkmode': session['dark_mode']}
    dark_mode = request.get_json()['darkmode']
    session['dark_mode'] = dark_mode
    return {'message': 'Dark mode updated', 'darkmode': dark_mode}

# test page for flask-wtf
@app.route('/test', methods=['GET', 'POST'])
def test():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            return 'Form submitted successfully'
    return render_template('test.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
