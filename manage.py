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
                         (username TEXT, email TEXT, image TEXT, role TEXT, signup DATE, PRIMARY KEY(username))''')
        c.execute('''CREATE TABLE IF NOT EXISTS passwords
                         (username TEXT, password TEXT, salt TEXT, FOREIGN KEY(username) REFERENCES users(username))''')
        c.execute('''CREATE TABLE IF NOT EXISTS books (title TEXT, author TEXT, genre TEXT, year INTEGER, isbn INTEGER, image TEXT, 
                    summary TEXT, price REAL, stock INTEGER, PRIMARY KEY(isbn))''')

    def add_user(self, username, password, email, image=None, role='user'):
        c = self.conn.cursor()
        if image is None:
            # If no image is provided, use the default image in static
            image = 'static/images/BookDefault.jpg'
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (username, email, image, role, sqlite3.Date.today()))
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

    def add_book(self, title, author, genre, year, isbn, image, summary, price=0.00, stock=0):
        c = self.conn.cursor()
        if image is None:
            image = 'static/images/BookDefault.jpg'
        c.execute("INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (title, author, genre, year, isbn, image, summary, price, stock))
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

    def get_books_by_year(self, year):
        c = self.conn.cursor()
        returnlist = []
        c.execute("SELECT * FROM books WHERE year=?", (year,))
        books = c.fetchall()
        for book in books:
            returnlist.append(book)
        c.close()
        return returnlist

    def get_books_by_price(self, min_price, max_price):
        c = self.conn.cursor()
        returnlist = []
        c.execute("SELECT * FROM books WHERE price BETWEEN ? AND ?", (min_price, max_price))
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
        db.add_user('admin', 'password', 'admin@admin.admin', role='admin')
        db.add_user('user', 'password', 'test@test.com')
        db.add_book('Test Book', 'Test Author', 'Test Genre', 2000, 1234567890, None, 'This is a test book, only here to test if searches work.', 10.00, 10)
        db.add_book('The Silmarillion', 'J.R.R. Tolkien', 'Fantasy', 1977, 9780261102736, 'static/images/TheSilmarillion.jpg', 'The Silmarillion is a collection of mythopoeic works by English writer J. R. R. Tolkien, edited and published posthumously by his son, Christopher Tolkien, in 1977, with assistance from Guy Gavriel Kay.', 8.99, 10)
        db.add_book('The Hobbit', 'J.R.R. Tolkien', 'Fantasy', 1937, 9780261102217, None, 'The Hobbit, or There and Back Again is a childrens fantasy novel by English author J. R. R. Tolkien. It was published on 21 September 1937 to wide critical acclaim, being nominated for the Carnegie Medal and awarded a prize from the New York Herald Tribune for best juvenile fiction.', 7.99, 10)
        db.add_book('The Lord of the Rings', 'J.R.R. Tolkien', 'Fantasy', 1954, 9780261102385, None, 'The Lord of the Rings is an epic high-fantasy novel written by English author and scholar J. R. R. Tolkien. The story began as a sequel to Tolkien\'s 1937 fantasy novel The Hobbit, but eventually developed into a much larger work.', 12.99, 10)
        db.add_book('The Fellowship of the Ring', 'J.R.R. Tolkien', 'Fantasy', 1954, 9780261102354, None, 'The Fellowship of the Ring is the first of three volumes of the epic novel The Lord of the Rings by the English author J. R. R. Tolkien. It is followed by The Two Towers and The Return of the King.', 9.99, 10)
        db.add_book('The Two Towers', 'J.R.R. Tolkien', 'Fantasy', 1954, 9780261102361, None, 'The Two Towers is the second volume of J.R.R. Tolkiens epic saga, The Lord of the Rings. The Fellowship has been forced to split up. Frodo and Sam must continue alone towards Mount Doom, where the One Ring must be destroyed.', 9.99, 10)
        db.add_book('The Return of the King', 'J.R.R. Tolkien', 'Fantasy', 1955, 9780261102378, None, 'The Return of the King is the third and final volume of J.R.R. Tolkiens The Lord of the Rings, following The Fellowship of the Ring and The Two Towers. The story begins in the kingdom of Gondor, which is soon to be attacked by the Dark Lord Sauron.', 9.99, 10)

if __name__ == '__main__':
    main()


def random_string(length):
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(length))