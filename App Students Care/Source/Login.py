from tkinter import*
from Database import *
import tkinter as tk
import Signup
import Forget_password
import Interface
import json, os

# =============================== JSON PROCESSING ===============================
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf8') as f:
            try:
                data = json.load(f)
                return data
            except:
                return {}
    return {}
def save_users(users):
    with open(USERS_FILE, "w", encoding="utf8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

# =============================== Login_windown ===============================
lg_win = Tk()
lg_win.title("Account")
lg_win.geometry("350x250+580+140")
lg_win.resizable(False, False)
login = Label(lg_win, text="LOGIN", font=('Arial', 18, 'bold'))
login.place(x=135, y=10)
username_email = Label(lg_win, text="Username/Email", font=("Arial", 11, 'bold'))
username_email.place(x=20, y=60)
username_email_entry = Entry(lg_win, text="Username/Email", width=28)
username_email_entry.place(x=150, y=60)
password = Label(lg_win, text="Password", font=("Arial", 11, 'bold'))
password.place(x=20, y=95)
password_entry = Entry(lg_win, text="Password", width=28, show="*")
password_entry.place(x=150, y=95)
msg_lbl = Label(lg_win, text="", fg="red", font=('Arial', 9, 'bold'))
msg_lbl.place(x=42, y=140)
# ==== Show/ hide password ====
def toggle_pw(entry, btn):
        if entry.cget('show') == '':
            entry.config(show='*')
            btn.config(text='👁️‍🗨️')
        else:
            entry.config(show='')
            btn.config(text='👁️')
eye = Button(lg_win, text='👁️‍🗨️', relief='flat', command=lambda: toggle_pw(password_entry, eye))
eye.place(x=320, y=95)
# ==== Remember password ====
is_checked = tk.BooleanVar(value=False)
check = tk.Checkbutton(lg_win, text="Remember me", variable=is_checked)
check.place(x=0, y=120)
# ==== Check username ====
users = load_users()
for username, info in users.items():
    if info.get("remember", False):
        username_email_entry.insert(0, username)
        password_entry.insert(0, info.get("password", ""))
        is_checked.set(True)
        break
# ==== Login ====
def login_acc():
    username_input = username_email_entry.get().strip()
    password_input = password_entry.get()
    users = load_users()
    login_user = None
    for username, info in users.items():
        if ((username_input == username or username_input == info['email']) and (password_input == info['password'])):
            login_user = username
            break
    if login_user:
        msg_lbl.config(text="✅ Login thành công!", fg="green")
        for user in users:
            users[user]["remember"] = False  # reset tất cả
        users[login_user]["remember"] = is_checked.get()
        save_users(users)  # Lưu lại file users.json
        Interface.open_interface(lg_win, login_user)
    else:
        msg_lbl.config(text="❌ Username/Email hoặc mật khẩu không đúng", fg="red")
# ==== Delete entry and open sign up ====
def go_to_signup():
    username_email_entry.delete(0, END)
    password_entry.delete(0, END)
    is_checked.set(False)
    msg_lbl.config(text="")
    Signup.open_signup(lg_win)
# ==== Function Button ====
login = Button(lg_win, text="Login", font=('Arial', 13, 'bold'), fg='white', bg='blue', command=login_acc)
login.place(x=145, y=160)
forget_pw = Button(lg_win, text="Forget password", font=('Arial', 9), activeforeground="#6633FF", relief='flat', bd=0, highlightthickness=0, command=lambda: Forget_password.open_forget_password(lg_win))
forget_pw.place(x=0, y=200)
signup_entry = Button(lg_win, text='Have an account? Sign up', font=('Arial', 9), activeforeground="#6633FF", relief='flat', bd=0, highlightthickness=0, command=go_to_signup)
signup_entry.place(x=0, y=220)

lg_win.mainloop()