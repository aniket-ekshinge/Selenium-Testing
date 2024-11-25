import sys
import os
import sqlite3
import pytest

# Add the parent directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import init_db

# Test setup: Create a separate testing database
@pytest.fixture
def db_connection():
    # Remove the test database file if it exists
    if os.path.exists('library_test.db'):
        os.remove('library_test.db')
    init_db()  # Initialize testing database tables
    conn = sqlite3.connect('library_test.db')
    yield conn
    conn.close()


# Unit Test: Add Book
def test_add_book(db_connection):
    conn = db_connection
    c = conn.cursor()
    c.execute("INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)", ("Test Book", "Test Author", "111111"))
    conn.commit()

    # Check if the book is added
    c.execute("SELECT * FROM books WHERE title = ?", ("Test Book",))
    book = c.fetchone()
    assert book is not None

    # Cleanup
    c.execute("DELETE FROM books WHERE title = ?", ("Test Book",))
    conn.commit()

# Unit Test: Issue Book
def test_issue_book(db_connection):
    conn = db_connection
    c = conn.cursor()

    # Add a book to issue
    c.execute("INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)", ("Issue Book", "Author Name", "222222"))
    conn.commit()

    # Issue the book
    c.execute("INSERT INTO issued_books (book_id, issued_to) VALUES (?, ?)", (1, "John Doe"))
    conn.commit()

    # Check if the book is issued
    c.execute("SELECT * FROM issued_books WHERE book_id = ?", (1,))
    issued_book = c.fetchone()
    assert issued_book is not None

    # Cleanup
    c.execute("DELETE FROM books WHERE title = ?", ("Issue Book",))
    c.execute("DELETE FROM issued_books WHERE book_id = ?", (1,))
    conn.commit()

# Unit Test: Return Book
def test_return_book(db_connection):
    conn = db_connection
    c = conn.cursor()

    # Add and issue a book to return
    c.execute("INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)", ("Return Book", "Author Name", "333333"))
    conn.commit()
    c.execute("INSERT INTO issued_books (book_id, issued_to) VALUES (?, ?)", (1, "John Doe"))
    conn.commit()

    # Return the book
    c.execute("DELETE FROM issued_books WHERE book_id = ?", (1,))
    conn.commit()

    # Check if the book is returned
    c.execute("SELECT * FROM issued_books WHERE book_id = ?", (1,))
    returned_book = c.fetchone()
    assert returned_book is None

    # Cleanup
    c.execute("DELETE FROM books WHERE title = ?", ("Return Book",))
    conn.commit()
