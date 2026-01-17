import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector 

def display_books_ad():
    try:
        conn = mysql.connector.connect(
            host="localhost",      
            user="root",         
            password="1234", 
            database="bookshop"     
        )
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM books")
        rows = cursor.fetchall()

        display_window = tk.Toplevel()
        display_window.title("Display Books")
        display_window.geometry("700x400")

        tree = ttk.Treeview(display_window, columns=("Name", "Author", "Price", "Quantity"), show="headings")
        tree.heading("Name", text="Book Name")
        tree.heading("Author", text="Author")
        tree.heading("Price", text="Price")
        tree.heading("Quantity", text="Quantity")

        tree.column("Name", anchor="center", width=150)
        tree.column("Author", anchor="center", width=150)
        tree.column("Price", anchor="center", width=100)
        tree.column("Quantity", anchor="center", width=100)

        for k in rows:
            tree.insert("", "end", values=k)

        scrollbar = tk.Scrollbar(display_window, orient="vertical", command=tree.yview)
        tree.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(padx=10, pady=10, expand=True, fill="both")
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Failed to fetch books: {err}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

