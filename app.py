from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('library_test.db')  
    c = conn.cursor()
    # Create books table
    c.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT NOT NULL UNIQUE
        )
    ''')
    # Create issued_books table
    c.execute('''
        CREATE TABLE IF NOT EXISTS issued_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            issued_to TEXT NOT NULL,
            FOREIGN KEY (book_id) REFERENCES books (id)
        )
    ''')
    conn.commit()
    conn.close()


init_db()

# Home page route
@app.route('/')
def home():
    return render_template('index.html')

# Route for adding books
@app.route('/add-book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']

        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)", (title, author, isbn))
        conn.commit()
        conn.close()

        return redirect(url_for('home'))
    return render_template('add_book.html')

# Route for issuing books
@app.route('/issue-book', methods=['GET', 'POST'])
def issue_book():
    if request.method == 'POST':
        book_id = request.form['book_id']
        issued_to = request.form['issued_to']

        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("INSERT INTO issued_books (book_id, issued_to) VALUES (?, ?)", (book_id, issued_to))
        conn.commit()
        conn.close()

        return redirect(url_for('home'))
    return render_template('issue_book.html')

# Route for returning books
@app.route('/return-book', methods=['GET', 'POST'])
def return_book():
    if request.method == 'POST':
        book_id = request.form['book_id']

        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("DELETE FROM issued_books WHERE book_id = ?", (book_id,))
        conn.commit()
        conn.close()

        return redirect(url_for('home'))
    return render_template('return_book.html')


if __name__ == '__main__':
    app.run(debug=True)
