# This file contains the API endpoints for the application. The API is used to interact with the database and perform
# operations such as searching for books and adding new books. The API is implemented using the Flask Blueprint
# class, which allows the API to be modular and easily integrated into the main application.
# One of the main features of the API is the ability to search for books in the database. This is done by sending a
# POST request to the /search endpoint with a query parameter. The API then searches the database for books that match
# the query and returns the results as JSON. The API also includes endpoints for adding new books to the database and
# retrieving book details by ISBN. These endpoints are implemented using the Database class from the manage.py file,
# which provides an interface for interacting with the database. The API also includes a test endpoint at the root URL
# that returns a simple JSON response. This is used to verify that the API is working correctly. The API is designed to
# be used by the front-end of the application, which is implemented using the Flask web framework. The front-end


from flask import Blueprint, request, g, render_template, logging
import sqlite3
import base64
from manage import Database

api = Blueprint('api', __name__)

DATABASE = 'Database.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = Database(DATABASE)
    return db


@api.route('/', methods=['GET', 'POST'])
def index():
    # The test page for the API
    # If the request is a GET, return the test page
    if request.method == 'GET':
        return render_template('api_index.html')
    # If the request is a POST, return JSON
    elif request.method == 'POST':
        return {'message': 'Hello, World!'}
    else:
        return 'Invalid request method'


@api.route('/search', methods=['POST'])
def search():
    # Searches the books database for the user's query
    # Use the request body as the query
    query = request.get_json()['input']
    if query is None:
        return 'Invalid query'
    print(query)
    # Get the books database
    db = get_db()
    # Search the database for books that match the query
    books = db.get_books_by_title(query)
    # Return the search results
    return books


@api.route('/book/<isbn>', methods=['GET'])
def book(isbn):
    # Returns the details of a book with the given ISBN
    # Get the books database
    db = get_db()
    # Get the details of the book with the given ISBN
    book = db.get_book_by_isbn(isbn)
    # Convert the book details to JSON
    book_data = {'title': book[0], 'author': book[1], 'genre': book[2], 'isbn': book[3], 'image': book[4], 'summary': book[5], 'price': book[6], 'stock': book[7]}
    return book_data


@api.route('/register', methods=['POST'])
def register():
    # Registers a new user based on the flask-wtf data from the registration form
    # Get the request data
    data = request.get_json()
    username = data['username']
    password = data['password']
    email = data['email']
    image = data['image']
    # Get the users database
    db = get_db()

    # Add the user to the database
    db.add_user(username, password, email, image)
    # Return a success message
    return {'message': 'User registered successfully'}


@api.route('/add_book', methods=['POST'])
def add_book():
    # Adds a new book to the database based on the flask-wtf data from the add book form
    # Get the request data
    data = request.get_json()
    title = data['title']
    author = data['author']
    genre = data['genre']
    year = data['year']
    isbn = data['isbn']
    image = data['image']
    summary = data['summary']
    price = data['price']
    stock = data['stock']
    # Get the books database
    db = get_db()
    # Add the book to the database
    db.add_book(title, author, genre, year, isbn, image, summary, price, stock)
    # Return a success message
    return {'message': 'Book added successfully'}


