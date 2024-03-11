# This file handles a lot of the backend functionality for the website
# This includes the loading of user data and book data from databases

import sqlite3
import string
import random

import config

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
                         (username TEXT, password TEXT, FOREIGN KEY(username) REFERENCES users(username))''')
        c.execute('''CREATE TABLE IF NOT EXISTS books (title TEXT, author TEXT, genre TEXT, year INTEGER, isbn INTEGER, image TEXT, 
                    summary TEXT, price REAL, stock INTEGER, PRIMARY KEY(isbn))''')

    def add_user(self, username, password, email, image=config.default_image, role='user'):
        c = self.conn.cursor()
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (username, email, image, role, sqlite3.Date.today()))
        salt = config.random_string(32).encode()
        hashed_password = config.argon2hasher.hash(password, salt=salt)
        c.execute("INSERT INTO passwords VALUES (?, ?)", (username, hashed_password))
        self.conn.commit()
        c.close()

    def get_user(self, username):
        c = self.conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        c.close()
        return user

    def get_user_role(self, username):
        c = self.conn.cursor()
        c.execute("SELECT role FROM users WHERE username=?", (username,))
        role = c.fetchone()
        c.close()
        return role[0]

    def get_user_password(self, username):
        c = self.conn.cursor()
        c.execute("SELECT * FROM passwords WHERE username=?", (username,))
        password = c.fetchone()
        c.close()
        return password[1]

    def add_book(self, title, author, genre, year, isbn, price=0.00, stock=0, summary=config.default_summary, image=config.default_image,):
        c = self.conn.cursor()
        c.execute("INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (title, author, genre, year, isbn, image, summary, price, stock))
        self.conn.commit()
        c.close()

    def get_book_by_isbn(self, isbn):
        """
        Returns the one book with the given ISBN from the database
        :param isbn:
        :type isbn: int
        :return: book
        :rtype: tuple
        """
        c = self.conn.cursor()
        c.execute("SELECT * FROM books WHERE isbn=?", (isbn,))
        book = c.fetchone()
        c.close()
        return book

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

    def get_books_by_params(self, title='%', author='%', genre='%', isbn='%'):
        """
        Returns a list of books that match the given parameters from the database
        :param title: The title of the book
        :param author: The author of the book
        :param genre: The genre of the book
        :param isbn: The ISBN of the book
        :type title: str or None
        :type author: str or None
        :type genre: str or None
        :type isbn: int or None
        :return: returnlist
        :rtype: list
        """
        c = self.conn.cursor()
        returnlist = []
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
        db.add_book('Test Book', 'Test Author', 'Test Genre', 2021, 1234567890123)
        db.add_book('The Silmarillion', 'J.R.R. Tolkien', 'Fantasy', 1977, 9780261102736, 10.99, 100,
                    'The Silmarillion is a collection of mythopoeic works by English writer J. R. R. Tolkien, edited and published posthumously by his son, Christopher Tolkien, in 1977, with assistance from Guy Gavriel Kay.', 'static/images/The-Silmarillion-Book-Cover.jpg')
        db.add_book('The Hobbit', 'J.R.R. Tolkien', 'Fantasy', 1937, 9780261102217, 7.99, 100,
                    'The Hobbit, or There and Back Again is a childrens fantasy novel by English author J. R. R. Tolkien. It was published on 21 September 1937 to wide critical acclaim, being nominated for the Carnegie Medal and awarded a prize from the New York Herald Tribune for best juvenile fiction.')
        db.add_book('The Lord of the Rings', 'J.R.R. Tolkien', 'Fantasy', 1954, 9780261102385, 19.99, 100,
                    'The Lord of the Rings is an epic high-fantasy novel written by English author and scholar J. R. R. Tolkien. The story began as a sequel to Tolkien\'s 1937 childrens book The Hobbit, but eventually developed into a much larger work.')
        db.add_book('Miss Peregrines Home for Peculiar Children', 'Ransom Riggs', 'Fantasy', 2011, 9781594746031, 12.99, 100,
                    'Miss Peregrines Home for Peculiar Children is a contemporary fantasy debut novel by American author Ransom Riggs. The story follows 16-year-old Jacob Portman as he investigates his grandfathers death and discovers a group of peculiar children on a holiday to Cairnholm Island.')
        db.add_book('The Great Gatsby', 'F. Scott Fitzgerald', 'Classic', 1925, 9780743273565, 9.99, 100,
                    'The Great Gatsby is a 1925 novel by American writer F. Scott Fitzgerald. Set in the Jazz Age on Long Island, near New York City, the novel depicts first-person narrator Nick Carraways interactions with mysterious millionaire Jay Gatsby and Gatsbys obsession to reunite with his former lover, Daisy Buchanan.')
        db.add_book('To Kill a Mockingbird', 'Harper Lee', 'Classic', 1960, 9780061120084, 8.99, 100,
                    'To Kill a Mockingbird is a novel by the American author Harper Lee. It is set in the fictional town of Maycomb, Alabama, and is narrated by the six-year-old Jean Louise Scout Finch as she grows up during the Great Depression.')
        db.add_book('1984', 'George Orwell', 'Dystopian', 1949, 9780451524935, 11.99, 100,
                    '1984 is a dystopian social science fiction novel by English novelist George Orwell. It was published on 8 June 1949 by Secker & Warburg as Orwells ninth and final book completed in his lifetime. Thematically, 1984 centres on the consequences of totalitarianism, mass surveillance, and repressive regimentation of persons and behaviours within society.')
        db.add_book('Brave New World', 'Aldous Huxley', 'Dystopian', 1932, 9780060850524, 10.99, 100,
                    'Brave New World is a dystopian social science fiction novel by English author Aldous Huxley, written in 1931 and published in 1932. Largely set in a futuristic World State, whose citizens are environmentally engineered into an intelligence-based social hierarchy, the novel anticipates huge scientific advancements in reproductive technology, sleep-learning, psychological manipulation and classical conditioning that are combined to make a utopian society that goes challenged only by a single outsider.')
        db.add_book('The Hunger Games', 'Suzanne Collins', 'Dystopian', 2008, 9780439023481, 13.99, 100,
                    'The Hunger Games is a 2008 dystopian novel by the American writer Suzanne Collins. It is written in the voice of 16-year-old Katniss Everdeen, who lives in the future, post-apocalyptic nation of Panem in North America. The Capitol, a highly advanced metropolis, exercises political control over the rest of the nation.')
        db.add_book('Percy Jackson and the Lightning Thief', 'Rick Riordan', 'Fantasy', 2005, 9780786838653, 11.99, 100,
                    'Percy Jackson and the Lightning Thief is a 2005 fantasy-adventure novel based on Greek mythology, the first young adult novel written by Rick Riordan. It is the first novel in the Percy Jackson & the Olympians series.')

if __name__ == '__main__':
    main()
