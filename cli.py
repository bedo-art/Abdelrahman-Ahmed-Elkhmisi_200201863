import database


def add_book():
    title = input("Enter book title: ")
    author = input("Enter author name: ")

    conn = database.get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO books (title, author) VALUES (?, ?)",
        (title, author)
    )

    conn.commit()
    conn.close()

    print("Book added successfully.")


def view_books():
    conn = database.get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    conn.close()

    if not books:
        print("No books found.")
        return

    for book in books:
        status = "Available" if book[3] == 1 else "Borrowed"

        print(
            f"ID: {book[0]} | Title: {book[1]} | Author: {book[2]} | {status}"
        )


def delete_book():
    book_id = input("Enter book ID to delete: ")

    conn = database.get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM books WHERE id=?",
        (book_id,)
    )

    conn.commit()
    conn.close()

    print("Book deleted successfully.")


def menu():

    database.create_tables()

    while True:

        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. View Books")
        print("3. Delete Book")
        print("4. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            add_book()

        elif choice == "2":
            view_books()

        elif choice == "3":
            delete_book()

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()