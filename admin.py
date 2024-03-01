# This file handles the admin functionality for the website
# This includes the ability to add, edit and delete books from the database as well as view user data
# The admin will have a dashboard where they can view data and manage the website
import flask_login
from flask import Blueprint, request, g, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from flask_wtf.file import FileSize, FileAllowed, FileField
from werkzeug.utils import secure_filename
from wtforms import validators
from wtforms.fields.simple import StringField

from config import images, image_max_size
from forms import AddBookForm
from manage import Database

admin = Blueprint('admin', __name__)

DATABASE = 'Database.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = Database(DATABASE)
    return db


@admin.route('/dashboard', methods=['GET'])
def dashboard():
    # The admin dashboard
    # Get the books database
    db = get_db()
    # Get all the books in the database
    books = db.get_all_books()
    # Get all the users in the database
    users = db.get_all_users()
    # Gather the statistics to display on the dashboard
    total_books = len(books)
    total_users = len(users)
    total_stock = sum([book[7] for book in books])
    return render_template('dashboard.html', books=books, users=users, total_books=total_books, total_users=total_users, total_stock=total_stock)


# The Add Book page will allow an admin to add a new book to the database
@admin.route('/add_book', methods=['GET', 'POST'])
@flask_login.login_required
def add_book():
    session['url'] = url_for('add_book')
    form = AddBookForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            db = get_db()
            title = form.title.data
            author = form.author.data
            genre = form.genre.data
            year = form.year.data
            isbn = form.isbn.data
            image = form.image.data
            image_name = secure_filename(image.filename)
            if image_name != '':
                image.save('data/' + image_name)
                image = 'data/' + image_name
            summary = form.summary.data
            price = form.price.data
            stock = form.stock.data
            db.add_book(title, author, genre, year, isbn, image, summary, price, stock)
            return redirect(session.pop('url'))
    # If the request method is GET, Check if the user has the role of admin, if not, throw a 404 error
    if g.user.role != 'admin':
        return render_template('errors/404.html')
    return render_template('add_book.html', form=form)

