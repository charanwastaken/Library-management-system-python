import tkinter as tk
from tkinter import messagebox
import smtplib
from email.message import EmailMessage
import csv
import mysql.connector as msc
import random
import os

conn = None
cursor = None
d = {}
usgup_frm = None
ufp_frm = None
ufpb_frm = None
usgup_btn = None
lg_frm = None
db_cnt_frm = None
current_user = ""
sent_otps = {}

def ad_m():
    action_frame.pack(pady=20)

def login():
    global current_user
    usn = usn_entry.get().strip()
    psd = psd_entry.get().strip()
    if not usn or not psd:
        messagebox.showerror("Login Failed", "Please enter both username and password")
        return
    if usn in d and d[usn][1] == psd:
        messagebox.showinfo("Login Successful", f"Welcome, {d[usn][0]}!")
        current_user = d[usn][0]
        us_m()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

def us_m():
    lg_frm.pack_forget()
    ufpb_frm.pack_forget()
    usgup_btn.pack_forget()
    us_action_frame.pack(pady=20)

def ufg_p():
    global ufp_frm
    def snd_otp():
        inp_em = inp_em_entry.get().strip()
        if not inp_em:
            messagebox.showerror("Error", "Please enter email!")
            return
        if inp_em not in d:
            messagebox.showerror("Error", "Email not registered!")
            return
        otp = str(random.randint(100000, 999999))
        sent_otps[inp_em] = otp
        if send_email_otp(inp_em, otp):
            messagebox.showinfo("Success", "OTP sent to your email!")
            ufp_frm.pack_forget()
            open_otp_window(inp_em)
    if ufp_frm is not None:
        ufp_frm.pack_forget()
    ufp_frm = tk.Frame(root)
    ufp_frm.pack(pady=20)
    tk.Label(ufp_frm, text="Enter your registered email:", font=("Helvetica", 12)).pack(pady=5)
    inp_em_entry = tk.Entry(ufp_frm, width=40)
    inp_em_entry.pack(pady=5)
    tk.Button(ufp_frm, text="Send OTP", command=snd_otp).pack(pady=10)

def send_email_otp(to_email, otp):
    from_mail = "litheavenlibrary@gmail.com"
    subject = "Lit Heaven Library - Password Reset OTP"
    body = f"Your OTP for resetting password is: {otp}"
    msg = EmailMessage()
    msg.set_content(body)
    msg['From'] = from_mail
    msg['To'] = to_email
    msg['Subject'] = subject
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_mail, "yknt idfn qzmz woys")   
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Email sending failed: {e}")
        return False

def open_otp_window(email):
    otp_window = tk.Toplevel(root)
    otp_window.title("Verify OTP & Reset Password")
    otp_window.geometry("400x250")
    tk.Label(otp_window, text="Enter OTP:", font=("Helvetica", 12)).pack(pady=5)
    otp_entry = tk.Entry(otp_window, width=30)
    otp_entry.pack(pady=5)
    tk.Label(otp_window, text="New Password:", font=("Helvetica", 12)).pack(pady=5)
    new_pass_entry = tk.Entry(otp_window, width=30, show="*")
    new_pass_entry.pack(pady=5)
    def verify_and_reset():
        entered_otp = otp_entry.get().strip()
        new_password = new_pass_entry.get().strip()
        if not entered_otp or not new_password:
            messagebox.showerror("Error", "All fields are required")
            return
        if email not in sent_otps or entered_otp != sent_otps[email]:
            messagebox.showerror("Error", "Invalid OTP")
            return
        try:
            rows = []
            with open("users.csv", "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0] == email:
                        rows.append([row[0], row[1], new_password])
                        d[email][1] = new_password
                    else:
                        rows.append(row)
            with open("users.csv", "w", newline="") as f:
                csv.writer(f).writerows(rows)
            messagebox.showinfo("Success", "Password reset successfully!")
            otp_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating password: {e}")
    tk.Button(otp_window, text="Submit", command=verify_and_reset).pack(pady=10)

def nw_usgn():
    signup_window = tk.Toplevel(root)
    signup_window.title("Sign Up")
    signup_window.geometry("400x300")
    def sv_usd():
        usn = signup_usn_entry.get().strip()
        inp_em = signup_inp_em_entry.get().strip()
        psd = signup_psd_entry.get().strip()
        if not usn or not inp_em or not psd:
            messagebox.showerror("Sign Up Failed", "All fields are required.")
            return
        if inp_em in d or any(user[0] == usn for user in d.values()):
            messagebox.showerror("Sign Up Failed", "Username or Email is already registered.")
            return
        d[inp_em] = [usn, psd]
        with open("users.csv", "a", newline="") as file:
            csv.writer(file).writerow([inp_em, usn, psd])
        messagebox.showinfo("Sign Up Successful", "You have successfully signed up!")
        signup_window.destroy()
    tk.Label(signup_window, text="Sign Up", font=("Helvetica", 14)).pack(pady=5)
    tk.Label(signup_window, text="username", font=("Helvetica", 12)).pack(pady=5)
    signup_usn_entry = tk.Entry(signup_window, width=40)
    signup_usn_entry.pack(pady=5)
    tk.Label(signup_window, text="email id:", font=("Helvetica", 12)).pack(pady=5)
    signup_inp_em_entry = tk.Entry(signup_window, width=40)
    signup_inp_em_entry.pack(pady=5)
    tk.Label(signup_window, text="password:", font=("Helvetica", 12)).pack(pady=5)
    signup_psd_entry = tk.Entry(signup_window, show="*", width=40)
    signup_psd_entry.pack(pady=5)
    tk.Button(signup_window, text="Sign Up", command=sv_usd, width=20).pack(pady=10)

def connect_db():
    global conn, cursor
    user = db_user_entry.get()
    psd = db_pass_entry.get()
    try:
        conn = msc.connect(host="localhost", user=user, password=psd)
        cursor = conn.cursor(buffered=True)  # buffered cursor to prevent unread result errors
        cursor.execute("CREATE DATABASE IF NOT EXISTS bookshop")
        cursor.execute("USE bookshop")
        cursor.execute('''CREATE TABLE IF NOT EXISTS books (
            name VARCHAR(255),
            author VARCHAR(255),
            price INT,
            quantity INT
        )''')
        messagebox.showinfo("Success", "Connected to the database!")
        ad_m()
    except msc.Error as e:
        messagebox.showerror("Error", f"Database connection failed: {e}")

def adm_addb():
    import add_book
    add_book.add_book(cursor, conn)

def adm_upb():
    import update_book
    update_book.update_book(cursor, conn)

def adm_delb():
    import delete_book
    delete_book.delete_book(cursor, conn)

def adm_dispb():
    import display_books
    display_books.display_books_ad()

def us_rtb(current_user):
    rent_window = tk.Toplevel()
    rent_window.title("Rent a Book")
    tk.Label(rent_window, text="Enter book name to rent:").pack(pady=5)
    bookname_inp = tk.Entry(rent_window)
    bookname_inp.pack(pady=5)

    def process_rent():
        bookname = bookname_inp.get().strip()
        if not bookname:
            messagebox.showerror("Error", "Please enter a book name.")
            return

        borrowed_books = []
        if os.path.exists("borrowed_books.csv"):
            with open("borrowed_books.csv", "r") as f:
                borrowed_books = list(csv.reader(f))

        for row in borrowed_books:
            if row[0] == current_user and row[1].lower() == bookname.lower() and row[2] == "Rented":
                messagebox.showerror("Error", f'You already rented "{bookname}".')
                return

        try:
            conn = msc.connect(host="localhost", user="root", password="1234", database="bookshop")
            cursor = conn.cursor(buffered=True)
            cursor.execute("SELECT quantity FROM books WHERE LOWER(name)=%s", (bookname.lower(),))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Error", f'Book "{bookname}" not found in DB.')
                return

            quantity = result[0]
            if quantity > 0:
                cursor.execute("UPDATE books SET quantity = quantity - 1 WHERE LOWER(name)=%s", (bookname.lower(),))
                conn.commit()
                with open("borrowed_books.csv", "a", newline="") as f:
                    csv.writer(f).writerow([current_user, bookname, "Rented"])
                messagebox.showinfo("Success", f'Book "{bookname}" rented successfully.')
            else:
                messagebox.showerror("Error", f'"{bookname}" is out of stock.')
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"DB error: {e}")

    tk.Button(rent_window, text="Rent", command=process_rent).pack(pady=10)

def us_rntb(current_user):
    return_window = tk.Toplevel()
    return_window.title("Return a Book")
    tk.Label(return_window, text="Enter the name of the book to return:").pack(pady=5)
    return_entry = tk.Entry(return_window)
    return_entry.pack(pady=5)

    def rt_bk():
        bookname = return_entry.get().strip()
        if not bookname:
            messagebox.showerror("Error", "Please enter a book name.")
            return

        borrowed_books = []
        if os.path.exists("borrowed_books.csv"):
            with open("borrowed_books.csv", "r") as f:
                borrowed_books = list(csv.reader(f))

        rented = False
        updated = []
        for row in borrowed_books:
            if row[0] == current_user and row[1].lower() == bookname.lower() and row[2] == "Rented":
                rented = True
                updated.append([row[0], row[1], "Returned"])
            else:
                updated.append(row)

        if not rented:
            messagebox.showerror("Error", f'You have not rented "{bookname}".')
            return

        try:
            conn = msc.connect(host="localhost", user="root", password="1234", database="bookshop")
            cursor = conn.cursor(buffered=True)
            cursor.execute("UPDATE books SET quantity = quantity + 1 WHERE LOWER(name)=%s", (bookname.lower(),))
            conn.commit()
            cursor.close()
            conn.close()

            with open("borrowed_books.csv", "w", newline="") as f:
                csv.writer(f).writerows(updated)

            messagebox.showinfo("Success", f'Book "{bookname}" returned successfully.')
        except Exception as e:
            messagebox.showerror("Error", f"DB error: {e}")

    tk.Button(return_window, text="Return", command=rt_bk).pack(pady=10)

def us_dispb():
    import display_books
    display_books.display_books_ad()

root = tk.Tk()
root.title("Lit Heaven Library Management")
root.geometry("500x500")

try:
    with open("users.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 3:
                d[row[0]] = [row[1], row[2]]
except FileNotFoundError:
    pass

welcome_label = tk.Label(root, text="LIT HEAVEN LIBRARY", font=("Helvetica", 16, "bold"), pady=10)
welcome_label.pack()

option_frame = tk.Frame(root)
option_frame.pack(pady=20)

def adm_pr():
    option_frame.pack_forget()
    db_cnt_frm.pack(pady=20)

def us_pr():
    option_frame.pack_forget()
    lg_frm.pack(pady=20)
    sh_usb()

def sh_usb():
    ufpb_frm.pack(pady=5)
    usgup_btn.pack(pady=5)

admin_button = tk.Button(option_frame, text="Admin", font=("Helvetica", 12), command=adm_pr, width=20)
admin_button.pack(pady=5)
user_button = tk.Button(option_frame, text="User", font=("Helvetica", 12), command=us_pr, width=20)
user_button.pack(pady=5)

ufpb_frm = tk.Button(root, text="Forgot password", font=("Helvetica", 12), command=ufg_p, width=20)
usgup_btn = tk.Button(root, text="Sign up", font=("Helvetica", 12), command=nw_usgn, width=20)

lg_frm = tk.Frame(root)
tk.Label(lg_frm, text="Email id", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=5)
usn_entry = tk.Entry(lg_frm, width=40)
usn_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Label(lg_frm, text="password", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=5)
psd_entry = tk.Entry(lg_frm, show="*", width=40)
psd_entry.grid(row=1, column=1, padx=10, pady=5)
tk.Button(lg_frm, text="Login", command=login, width=20).grid(row=2, column=0, columnspan=2, pady=10)

action_frame = tk.Frame(root)
tk.Button(action_frame, text="Add Book", command=adm_addb, width=25).pack(pady=5)
tk.Button(action_frame, text="Update Book", command=adm_upb, width=25).pack(pady=5)
tk.Button(action_frame, text="Delete Book", command=adm_delb, width=25).pack(pady=5)
tk.Button(action_frame, text="Display Books", command=adm_dispb, width=25).pack(pady=5)

us_action_frame = tk.Frame(root)
tk.Button(us_action_frame, text="Rent Book", command=lambda: us_rtb(current_user), width=25).pack(pady=5)
tk.Button(us_action_frame, text="Return Book", command=lambda: us_rntb(current_user), width=25).pack(pady=5)
tk.Button(us_action_frame, text="Display Books", command=us_dispb, width=25).pack(pady=5)

db_cnt_frm = tk.Frame(root)
tk.Label(db_cnt_frm, text="Username:", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=5)
db_user_entry = tk.Entry(db_cnt_frm, width=40)
db_user_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Label(db_cnt_frm, text="Password:", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=5)
db_pass_entry = tk.Entry(db_cnt_frm, show="*", width=40)
db_pass_entry.grid(row=1, column=1, padx=10, pady=5)
tk.Button(db_cnt_frm, text="Connect", command=connect_db, width=20).grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()

