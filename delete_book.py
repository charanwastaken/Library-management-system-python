import tkinter as tk
from tkinter import messagebox

def delete_book(cursor, conn):
    def submit():
        name = name_entry.get().strip()

        if not name:
            messagebox.showwarning("Warning", "Please enter the book name.")
            return

        try:
            
            cursor.execute("DELETE FROM books WHERE LOWER(name) = %s", (name.lower(),))
            conn.commit()

            if cursor.rowcount > 0:  
                messagebox.showinfo("Info", f"Book '{name}' deleted successfully!")
                delete_book_window.destroy()
            else:
                messagebox.showwarning("Warning", f"No book found with name '{name}' in database.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete book: {e}")


    delete_book_window = tk.Toplevel()
    delete_book_window.title("Delete Book")

    tk.Label(delete_book_window, text="Book Name:").grid(row=0, column=0, padx=10, pady=5)
    name_entry = tk.Entry(delete_book_window)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    submit_button = tk.Button(delete_book_window, text="Delete Book", command=submit)
    submit_button.grid(row=1, column=0, columnspan=2, pady=10)

    name_entry.focus()
