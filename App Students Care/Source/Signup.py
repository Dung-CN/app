from tkinter import *
from Database import *
import json, os
import re

# ================================ VARIABLE GLOBAL ================================ 
error_email_label = None
error_pw_label = None
# ================================ INFORMATION FORMATH ================================
def check_email(email):
    is_valid = bool(re.fullmatch(r'\w+@\w+\.\w+$', email))
    return is_valid
def check_password(password):
    is_valid = bool(re.fullmatch(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[@#_]).+$', password))
    return is_valid
# ================================ JSON ================================
def load_users(): # Get user information
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf8') as f:
            try:
                data = json.load(f)
                return data
            except:
                return {}
    return {}
def save_users(data): # Save user information
    with open(USERS_FILE, 'w', encoding="utf8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
# ================================ Sign up windown ================================
def open_signup(lg_win):
    lg_win.withdraw()
    sgn = Toplevel()
    sgn.title('SIGN UP')
    sgn.geometry("350x290+580+140")
    sgn.resizable(False, False)

    # ============== Form information ==============
    username = Label(sgn, text="Username", font=("Arial", 11, 'bold'))
    username.place(x=10, y=60)
    username_entry = Entry(sgn, text="Username", width=30)
    username_entry.place(x=150, y=60)
    email = Label(sgn, text="Email", font=("Arial", 11, 'bold'))
    email.place(x=10, y=95)
    email_entry = Entry(sgn, width=30)
    email_entry.place(x=150, y=95)
    password = Label(sgn, text="Password", font=("Arial", 11, 'bold'))
    password.place(x=10, y=130)
    password_entry = Entry(sgn, text="Password", width=30, show="*")
    password_entry.place(x=150, y=130)
    confirm_password = Label(sgn, text="Confirm Password", font=("Arial", 11, 'bold'))
    confirm_password.place(x=10, y=165)
    confirm_password_entry = Entry(sgn, text="Confirm Password", width=30, show="*")
    confirm_password_entry.place(x=150, y=165)
    signup = Label(sgn, text="SIGN UP", font=('Arial', 18, 'bold'))
    signup.place(x=120, y=10)

    # ========= Show/ hide password =========
    def toggle_pw(entry, btn):
        if entry.cget('show') == '':
            entry.config(show='*')
            btn.config(text='👁️‍🗨️')
        else:
            entry.config(show='')
            btn.config(text='👁️')
    eye1 = Button(sgn, text='👁️‍🗨️', relief='flat', command=lambda: toggle_pw(password_entry, eye1))
    eye1.place(x=320, y=128)
    eye2 = Button(sgn, text='👁️‍🗨️', relief='flat', command=lambda: toggle_pw(confirm_password_entry, eye2))
    eye2.place(x=320, y=163)

    # ===== Create account =====
    def create_acc():
        global error_email_label, error_pw_label
        user_name = username_entry.get().strip()
        email = email_entry.get().strip()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        if error_email_label:
            error_email_label.destroy() 
            error_email_label = None
        if error_pw_label:
            error_pw_label.destroy()
            error_pw_label = None

        if not check_email(email):
            error_email_label = Label(sgn, text="Email không hợp lệ", fg="red", relief='flat', bd=0)
            error_email_label.place(x=150, y=110)
            return
        if not check_password(password):
            error_pw_label = Label(sgn, text="Password phải chứa ít nhất kí tự viết hoa, kí đặc biệt và chữ số", fg="red")
            error_pw_label.place(x=15, y=148)
            return

        users = load_users() # Get user information
        if user_name in users:
            Label(sgn, text="Tên người dùng đã tồn tại!", fg="red", relief='flat', bd=0).place(x=100, y=195)
            return
        elif password != confirm_password:
            Label(sgn, text="Mật khẩu không khớp!", fg="red").place(x=100, y=195)
            return
        users[user_name] = {"email": email, "password": password}
        save_users(users)
        Label(sgn, text="✅ Tạo tài khoản thành công", fg="green").place(x=100, y=195)
    create_acc = Button(sgn, text='Create Account', font=('Arial', 13, 'bold'), command=create_acc)
    create_acc.place(x=105 ,y=220)

    def back_to_login():
        username_entry.delete(0, END)
        email_entry.delete(0, END)
        password_entry.delete(0, END)
        confirm_password_entry.delete(0, END)
        sgn.destroy()
        lg_win.deiconify()
    Button(sgn, text="Back", relief='flat', bd=0, command=back_to_login).place(x=10, y=250)
    sgn.protocol("WM_DELETE_WINDOW", lambda: None)

    

    