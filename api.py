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


from flask import Blueprint, request, g, render_template
import sqlite3
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
        return '{"message": "Hello, World!"}'
    else:
        return 'Invalid request method'


@api.route('/search', methods=['POST'])
def search():
    # Searches the books database for the user's query
    query = request.form['query']
    books = get_db().get_books_by_name(query)
    # Return the search results as a list of JSON objects (one for each book)
    return_books = []
    for book in books:
        book_dict = {'title': book[1], 'author': book[2], 'genre': book[3], 'isbn': book[4], 'summary': book[6]}
        return_books.append(book_dict)
    return return_books

