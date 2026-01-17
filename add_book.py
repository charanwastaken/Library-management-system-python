import tkinter as tk
from tkinter import messagebox

def add_book(cursor, conn):
    def submit():
        name = name_inp.get().strip()
        author = author_inp.get().strip()
        price = price_inp.get().strip()
        quantity = quantity_inp.get().strip()

        
        if not name or not author or not price or not quantity:
            messagebox.showwarning("Warning", "Please fill all fields.")
            return

        try:
    
            cursor.execute(
                "INSERT INTO books (name, author, price, quantity) VALUES (%s, %s, %s, %s)",
                (name, author, int(price), int(quantity))
            )
            conn.commit()
            messagebox.showinfo("Success", "Book added successfully!")
            add_book_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add book: {e}")


    add_book_window = tk.Toplevel()
    add_book_window.title("Add Book")

    tk.Label(add_book_window, text="Book Name:").grid(row=0, column=0, padx=10, pady=5)
    name_inp = tk.Entry(add_book_window)
    name_inp.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(add_book_window, text="Author:").grid(row=1, column=0, padx=10, pady=5)
    author_inp = tk.Entry(add_book_window)
    author_inp.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(add_book_window, text="Price:").grid(row=2, column=0, padx=10, pady=5)
    price_inp = tk.Entry(add_book_window)
    price_inp.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(add_book_window, text="Quantity:").grid(row=3, column=0, padx=10, pady=5)
    quantity_inp = tk.Entry(add_book_window)
    quantity_inp.grid(row=3, column=1, padx=10, pady=5)

    submit_button = tk.Button(add_book_window, text="Add Book", command=submit)
    submit_button.grid(row=4, column=0, columnspan=2, pady=10)

    name_inp.focus()
