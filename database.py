import sqlite3

DATABASE_NAME = "library.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        available INTEGER DEFAULT 1
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS borrowings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER,
        member_id INTEGER,
        borrow_date TEXT,
        return_date TEXT,
        FOREIGN KEY(book_id) REFERENCES books(id),
        FOREIGN KEY(member_id) REFERENCES members(id)
    )
    """)

    connection.commit()
    connection.close()


# BOOKS

def add_book(title, author):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO books(title, author) VALUES (?, ?)",
        (title, author)
    )

    conn.commit()
    conn.close()


def get_books():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    conn.close()

    return books


# MEMBERS

def add_member(name, email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO members(name, email) VALUES (?, ?)",
        (name, email)
    )

    conn.commit()
    conn.close()


def get_members():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()

    conn.close()

    return members


def delete_member(member_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM members WHERE id=?",
        (member_id,)
    )

    conn.commit()
    conn.close()


# BORROWING

def borrow_book(book_id, member_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO borrowings(book_id, member_id, borrow_date)
        VALUES (?, ?, DATE('now'))
        """,
        (book_id, member_id)
    )

    cursor.execute(
        """
        UPDATE books
        SET available = 0
        WHERE id = ?
        """,
        (book_id,)
    )

    conn.commit()
    conn.close()


def return_book(book_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE borrowings
        SET return_date = DATE('now')
        WHERE book_id = ?
        AND return_date IS NULL
        """,
        (book_id,)
    )

    cursor.execute(
        """
        UPDATE books
        SET available = 1
        WHERE id = ?
        """,
        (book_id,)
    )

    conn.commit()
    conn.close()
# UPDATE BOOK

def update_book(book_id, title, author):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE books
        SET title = ?, author = ?
        WHERE id = ?
        """,
        (title, author, book_id)
    )

    conn.commit()
    conn.close()



# UPDATE MEMBER

def update_member(member_id, name, email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE members
        SET name = ?, email = ?
        WHERE id = ?
        """,
        (name, email, member_id)
    )

    conn.commit()
    conn.close()



# BORROWING RECORDS

def get_borrowings():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 
        borrowings.id,
        books.title,
        members.name,
        borrowings.borrow_date,
        borrowings.return_date

        FROM borrowings

        JOIN books
        ON borrowings.book_id = books.id

        JOIN members
        ON borrowings.member_id = members.id
        """
    )

    borrowings = cursor.fetchall()

    conn.close()

    return borrowings



# UPDATE BOOK

def delete_borrowing(borrowing_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM borrowings
        WHERE id = ?
        """,
        (borrowing_id,)
    )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("Database initialized successfully.")