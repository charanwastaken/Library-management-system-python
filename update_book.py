import tkinter as tk
from tkinter import messagebox

def update_book(cursor, conn):
    def update_options():
        nonlocal bookname
        bookname = booknameinp.get().strip()

        if bookname == "":  
            messagebox.showwarning("Validation Error", "Please enter the book name.")
            return

        bookname_frame.pack_forget()
        choose_frame.pack(pady=20)

    def perform_update(field):
        def update():
            new_value = new_entry.get().strip()

            if new_value == "":
                messagebox.showwarning("Validation Error", "Please enter a valid value.")
                return

            try:
                # Convert types where needed
                if field in ("price", "quantity"):
                    new_value_casted = int(new_value)
                else:
                    new_value_casted = new_value

                query = f"UPDATE books SET {field} = %s WHERE name = %s"
                cursor.execute(query, (new_value_casted, bookname))
                conn.commit()

                if cursor.rowcount == 0:
                    messagebox.showwarning("Update Failed", "No book found with the specified name.")
                else:
                    messagebox.showinfo("Success", f"Book's {field} updated successfully!")

                update_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update book: {e}")
                update_window.destroy()

        choose_frame.pack_forget()

        tk.Label(update_window, text=f"Enter New {field.capitalize()}:").pack(pady=5)
        new_entry = tk.Entry(update_window)
        new_entry.pack(pady=5)
        tk.Button(update_window, text="Submit", command=update).pack(pady=10)
        new_entry.focus()

    bookname = ""

    update_window = tk.Toplevel()
    update_window.title("Update Book")
    update_window.geometry("400x300")

    bookname_frame = tk.Frame(update_window)
    bookname_frame.pack(pady=20)

    tk.Label(bookname_frame, text="Enter Book Name:").pack(pady=5)
    booknameinp = tk.Entry(bookname_frame)
    booknameinp.pack(pady=5)
    tk.Button(bookname_frame, text="Next", command=update_options).pack(pady=10)

    choose_frame = tk.Frame(update_window)
    tk.Label(choose_frame, text="Choose the field to update:").pack(pady=5)
    tk.Button(choose_frame, text="Update Name", command=lambda: perform_update("name")).pack(pady=5)
    tk.Button(choose_frame, text="Update Author", command=lambda: perform_update("author")).pack(pady=5)
    tk.Button(choose_frame, text="Update Price", command=lambda: perform_update("price")).pack(pady=5)
    tk.Button(choose_frame, text="Update Quantity", command=lambda: perform_update("quantity")).pack(pady=5)
