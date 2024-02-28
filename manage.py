# This file handles a lot of the backend functionality for the website
# This includes the loading of user data and book data from databases

import sqlite3
import string
import base64
import scrypt
import random
import re

usersdb = 'users.db'
booksdb = 'books.db'


# Create a table in the database to store user data if it doesn't already exist
# The password is hashed using scrypt to ensure security and stored in a different table to the username and other details
# The salt is randomly generated for each user and stored in the same table as the hashed password
# The password table is linked to the user table with a foreign key

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                         (username text, email text, image blob, signup date, PRIMARY KEY(username))''')
        c.execute('''CREATE TABLE IF NOT EXISTS passwords
                         (username text, password text, salt text, FOREIGN KEY(username) REFERENCES users(username))''')
        c.execute('''CREATE TABLE IF NOT EXISTS books (title TEXT, author TEXT, genre TEXT, isbn INTEGER, image TEXT, 
                    summary TEXT, price REAL, stock INTEGER, PRIMARY KEY(isbn))''')

    def add_user(self, username, password, email, image=None):
        c = self.conn.cursor()
        if image is None:
            # If no image is provided, use the default image in static
            image = 'static/images/BookDefault.jpg'
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (username, email, image, sqlite3.Date.today()))
        salt = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(32))
        hashed_password = scrypt.hash(password, salt)
        c.execute("INSERT INTO passwords VALUES (?, ?, ?)", (username, hashed_password, salt))
        self.conn.commit()
        c.close()

    def get_user(self, username):
        c = self.conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        c.close()
        return user

    def get_user_password(self, username):
        c = self.conn.cursor()
        c.execute("SELECT * FROM passwords WHERE username=?", (username,))
        password = c.fetchone()
        c.close()
        return password

    def get_password_salt(self, password):
        c = self.conn.cursor()
        c.execute("SELECT salt FROM passwords WHERE password=?", (password,))
        salt = c.fetchone()
        c.close()
        return salt

    def add_book(self, title, author, genre, isbn, image, summary, price=0.00, stock=0):
        c = self.conn.cursor()
        c.execute("INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (title, author, genre, isbn, image, summary, price, stock))
        self.conn.commit()
        c.close()

    def get_books_by_isbn(self, isbn):
        c = self.conn.cursor()
        c.execute("SELECT * FROM books WHERE isbn=?", (isbn,))
        books = c.fetchall()
        c.close()
        return books

    def get_books_by_title(self, title):
        c = self.conn.cursor()
        returnlist = []
        title = '%' + title + '%'
        c.execute("SELECT * FROM books WHERE title LIKE ?", (title,))
        books = c.fetchall()
        for book in books:
            returnlist.append(book)
        c.close()
        return returnlist

    def get_books_by_author(self, author):
        c = self.conn.cursor()
        returnlist = []
        c.execute("SELECT * FROM books WHERE author=?", (f'%{author}%',))
        books = c.fetchall()
        for book in books:
            returnlist.append(book)
        c.close()
        return returnlist

    def get_books_by_genre(self, genre):
        c = self.conn.cursor()
        returnlist = []
        c.execute("SELECT * FROM books WHERE genre=?", (f'%{genre}%',))
        books = c.fetchall()
        for book in books:
            returnlist.append(book)
        c.close()
        return returnlist

    def get_all_books(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM books")
        books = c.fetchall()
        c.close()
        return books

    def get_books_by_query(self, query):
        c = self.conn.cursor()
        returnlist = []
        # Find books with a weak match to the query
        c.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR genre LIKE ? OR summary LIKE ?",
                  ('%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%'))
        books = c.fetchall()
        for book in books:
            returnlist.append(book)
        c.close()
        return returnlist

    def get_books_by_params(self, title, author, genre, isbn):
        c = self.conn.cursor()
        returnlist = []
        if title == '':
            title = '%'
        if author == '':
            author = '%'
        if genre == '':
            genre = '%'
        if isbn == '':
            isbn = '%'
        c.execute("SELECT * FROM books WHERE title LIKE ? AND author LIKE ? AND genre LIKE ? AND isbn LIKE ?",
                  ('%' + title + '%', '%' + author + '%', '%' + genre + '%', '%' + isbn + '%'))
        books = c.fetchall()
        for book in books:
            returnlist.append(book)
        c.close()
        return returnlist

    def __enter__(self):
        self.conn = sqlite3.connect('Database.db')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


def main():
    with Database('Database.db') as db:
        # Load the silmarillion image from the file as base64
        with open('static/images/The-Silmarillion-Book-Cover.jpg', 'rb') as file:
            silmarillionimage = base64.b64encode(file.read())
        db.add_user('admin', 'admin', 'admin@Shelfworm.com')
        db.add_user('user', 'user', 'test@test.test')
        db.add_book('The Hobbit', 'J.R.R. Tolkien', 'Fantasy', 9780261102217, None, 'The Hobbit is a fantasy novel')
        db.add_book('The Fellowship of the Ring', 'J.R.R. Tolkien', 'Fantasy', 9780261102354, None,
                    'The Fellowship of the Ring is a fantasy novel')
        db.add_book('The Two Towers', 'J.R.R. Tolkien', 'Fantasy', 9780261102361, None, 'The Two Towers is a fantasy novel')
        db.add_book('The Return of the King', 'J.R.R. Tolkien', 'Fantasy', 9780261102378, None,
                    'The Return of the King is a fantasy novel')
        db.add_book('The Silmarillion', 'J.R.R. Tolkien', 'Fantasy', 9780261102736, silmarillionimage, 'The Silmarillion is a fantasy novel')
        db.add_book('The Children of Hurin', 'J.R.R. Tolkien', 'Fantasy', 9780007246229, None, 'The Children of Hurin is a fantasy novel')
        db.add_book('The Fall of Gondolin', 'J.R.R. Tolkien', 'Fantasy', 9780008302757, None, 'The Fall of Gondolin is a fantasy novel')
        db.add_book('Beren and Luthien', 'J.R.R. Tolkien', 'Fantasy', 9780008214197, None, 'Beren and Luthien is a fantasy novel')
        db.add_book('Unfinished Tales', 'J.R.R. Tolkien', 'Fantasy', 9780261102163, None, 'Unfinished Tales is a fantasy novel')
        db.add_book('The History of Middle-earth', 'J.R.R. Tolkien', 'Fantasy', 9780261102750, None, 'The History of Middle-earth is a fantasy novel')
        db.add_book('The Lord of the Rings', 'J.R.R. Tolkien', 'Fantasy', 9780261102385, None, 'The Lord of the Rings is a fantasy novel')


if __name__ == '__main__':
    main()


def random_string(length):
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(length))