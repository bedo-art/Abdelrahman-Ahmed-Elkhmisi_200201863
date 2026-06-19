import tkinter as tk
from tkinter import messagebox
import database


database.create_tables()


def add_book():
    title = book_title_entry.get()
    author = book_author_entry.get()

    if title == "" or author == "":
        messagebox.showwarning("Warning", "Fill all fields")
        return

    database.add_book(title, author)

    refresh_books()


def refresh_books():

    books_list.delete(0, tk.END)

    books = database.get_books()

    for book in books:

        status = "Available" if book[3] == 1 else "Borrowed"

        books_list.insert(
            tk.END,
            f"ID:{book[0]} | {book[1]} | {book[2]} | {status}"
        )


def delete_book():

    selected = books_list.curselection()

    if not selected:
        return

    data = books_list.get(selected[0])

    book_id = data.split("|")[0].replace("ID:", "").strip()

    conn = database.get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM books WHERE id=?",
        (book_id,)
    )

    conn.commit()
    conn.close()

    refresh_books()



def update_book():

    selected = books_list.curselection()

    if not selected:
        return

    data = books_list.get(selected[0])

    book_id = data.split("|")[0].replace("ID:", "").strip()

    database.update_book(
        book_id,
        book_title_entry.get(),
        book_author_entry.get()
    )

    refresh_books()



def add_member():

    database.add_member(
        member_name_entry.get(),
        member_email_entry.get()
    )

    refresh_members()



def refresh_members():

    members_list.delete(0, tk.END)

    members = database.get_members()

    for member in members:

        members_list.insert(
            tk.END,
            f"ID:{member[0]} | {member[1]} | {member[2]}"
        )



def delete_member():

    selected = members_list.curselection()

    if not selected:
        return

    data = members_list.get(selected[0])

    member_id = data.split("|")[0].replace("ID:", "").strip()

    database.delete_member(member_id)

    refresh_members()



def update_member():

    selected = members_list.curselection()

    if not selected:
        return

    data = members_list.get(selected[0])

    member_id = data.split("|")[0].replace("ID:", "").strip()


    database.update_member(
        member_id,
        member_name_entry.get(),
        member_email_entry.get()
    )

    refresh_members()



def borrow_book():

    database.borrow_book(
        int(borrow_book_id.get()),
        int(borrow_member_id.get())
    )

    refresh_books()
    refresh_borrowings()



def return_book():

    database.return_book(
        int(return_book_id.get())
    )

    refresh_books()
    refresh_borrowings()



def refresh_borrowings():

    loans_list.delete(0, tk.END)

    loans = database.get_borrowings()

    for loan in loans:

        loans_list.insert(
            tk.END,
            str(loan)
        )



def delete_borrowing():

    selected = loans_list.curselection()

    if not selected:
        return

    loan = loans_list.get(selected[0])

    loan_id = loan.replace("(", "").split(",")[0]

    database.delete_borrowing(loan_id)

    refresh_borrowings()



window = tk.Tk()

window.title("Library Management System - Python + SQLite")

window.geometry("900x600")


canvas = tk.Canvas(window)

scrollbar = tk.Scrollbar(
    window,
    orient="vertical",
    command=canvas.yview
)

scrollable_frame = tk.Frame(
    canvas,
    width=800
)


scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)


canvas.create_window(
    (400,0),
    window=scrollable_frame,
    anchor="n"
)


canvas.configure(
    yscrollcommand=scrollbar.set
)


canvas.pack(
    side="left",
    fill="both",
    expand=True
)

canvas.bind(
    "<Configure>",
    lambda e: canvas.itemconfig(
        canvas.find_all()[0],
        width=e.width
    )
)


scrollbar.pack(
    side="right",
    fill="y"
)


window = scrollable_frame


# BOOKS

tk.Label(window,text="Books").pack()

book_title_entry=tk.Entry(window)
book_title_entry.pack()

book_author_entry=tk.Entry(window)
book_author_entry.pack()


tk.Button(window,text="Add Book",command=add_book).pack()

tk.Button(window,text="Update Book",command=update_book).pack()

books_list=tk.Listbox(window,width=90)
books_list.pack()

tk.Button(window,text="Refresh Books",command=refresh_books).pack()

tk.Button(window,text="Delete Book",command=delete_book).pack()



# MEMBERS

tk.Label(window,text="Members").pack()


member_name_entry=tk.Entry(window)
member_name_entry.pack()


member_email_entry=tk.Entry(window)
member_email_entry.pack()


tk.Button(window,text="Add Member",command=add_member).pack()

tk.Button(window,text="Update Member",command=update_member).pack()


members_list=tk.Listbox(window,width=90)
members_list.pack()


tk.Button(window,text="Refresh Members",command=refresh_members).pack()

tk.Button(window,text="Delete Member",command=delete_member).pack()



# BORROW


tk.Label(window,text="Borrow Book").pack()


borrow_book_id=tk.Entry(window)
borrow_book_id.pack()


borrow_member_id=tk.Entry(window)
borrow_member_id.pack()


tk.Button(window,text="Borrow Book",command=borrow_book).pack()



# RETURN


tk.Label(window,text="Return Book").pack()


return_book_id=tk.Entry(window)
return_book_id.pack()


tk.Button(window,text="Return Book",command=return_book).pack()



# LOANS


tk.Label(window,text="Borrowing Records").pack()


loans_list=tk.Listbox(window,width=60)

loans_list.pack()


tk.Button(
    window,
    text="Refresh Loans",
    command=refresh_borrowings
).pack()


tk.Button(
    window,
    text="Delete Loan",
    command=delete_borrowing
).pack()



refresh_books()
refresh_members()
refresh_borrowings()


window.mainloop()