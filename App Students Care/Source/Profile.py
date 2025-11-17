from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from Database import *
import tkinter as tk
import json, os
import re

# ================================ VARIABLE GLOBAL ================================ 
error_email_label = None
error_dob_label = None
# ================================ INFORMATION FORMATH ================================
def check_email(email):
    is_valid = bool(re.fullmatch(r'\w+@\w+\.\w+$', email))
    return is_valid
def check_dob(dob):
    is_valid = bool(re.fullmatch(r'^(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[0-2])/[0-9]{4}$', dob))
    return is_valid
# ================================ JSON ================================ 
def _ensure_profile_file():
    if not os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "w", encoding="utf8") as f:
            json.dump({}, f, ensure_ascii=False, indent=2)

def load_profile_for_user(username):
    _ensure_profile_file()
    with open(PROFILE_FILE, "r", encoding="utf8") as f:
        try:
            data = json.load(f)
        except:
            data = {}
    if isinstance(data, dict):
        return data.get(username, {})
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and item.get("username") == username:
                return item
    return {}

def save_profile_for_user(username, profile_dict):
    _ensure_profile_file()
    with open(PROFILE_FILE, "r", encoding="utf8") as f:
        try:
            data = json.load(f)
        except:
            data = {}
    if isinstance(data, list):
        tmp = {}
        for item in data:
            if isinstance(item, dict) and "username" in item:
                tmp[item["username"]] = item
        data = tmp
    data[username] = profile_dict
    with open(PROFILE_FILE, "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def open_profile(root, username):
    root.withdraw()
    pro_win = Toplevel()
    # ====Pro windown====
    pro_win.title('HỒ SƠ CÁ NHÂN')
    pro_win.geometry('{}x{}+{}+{}'.format(WINDOWN_WIDTH, WINDOWN_HEIGHT, WINDOWN_POSION_RIGHT, WINDOWN_POSION_DOWN))
    pro_win.resizable(False, False)
    pro_win.configure(bg="#f5f5f5")
    # ====CONTENT====
    heading = Label(pro_win, text='Hồ Sơ Cá Nhân', font=('Arial', 20, 'bold'), bg="#f5f5f5")
    heading.pack(padx=10, pady=40)
    frame = Frame(pro_win, bg="#f5f5f5", relief=GROOVE, bd=2, pady=5)
    frame.pack(padx=15, fill='x')

    # ========================================================== AVATAR FRAME ==========================================================
    avatar_frame = Frame(frame, bg="#ffffff")
    avatar_frame.grid(row=0, column=0, rowspan=5, sticky='nw', padx=(10, 0))
    # ==== Display default avatar ====
    try:
        if os.path.exists(DEFAULT_AVATAR):
            avatar_img = Image.open(DEFAULT_AVATAR)
        else:
            raise FileNotFoundError
    except Exception:
        avatar_img = Image.new('RGB', (160, 160), color='lightgray')
    avatar_img = avatar_img.resize((160, 160), Image.LANCZOS)
    avatar_photo = ImageTk.PhotoImage(avatar_img)
    avatar_label = Label(avatar_frame, image=avatar_photo, bg="#f5f5f5", relief="groove")
    avatar_photo.photo_default = avatar_photo
    avatar_photo.photo_current = avatar_photo
    avatar_label.image = avatar_photo
    avatar_label.pack(pady=5)

    # ==== Load Avatar ====
    def load_avatar():
        profile = load_profile_for_user(username) # Get information by username
        path = profile.get("avatar_path", DEFAULT_AVATAR)
        if not os.path.exists(path):
            path = DEFAULT_AVATAR if os.path.exists(DEFAULT_AVATAR) else ""
        try:
            new_img = Image.open(path).resize((160, 160), Image.LANCZOS)
        except:
            new_img = Image.new("RGB", (160, 160), color="lightgray")
        new_photo = ImageTk.PhotoImage(new_img)
        avatar_label.configure(image=new_photo)
        avatar_label.image = new_photo

    # ==== Change Avatar ====
    def change_avatar():
        file_path = filedialog.askopenfilename(
            title="Chọn ảnh đại diện",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.ico")]
            )
        if file_path:
            new_img = Image.open(file_path).resize((160, 160), Image.LANCZOS)
            new_photo = ImageTk.PhotoImage(new_img)
            avatar_label.configure(image=new_photo)
            avatar_label.image = new_photo

            profile = load_profile_for_user(username) or {}
            profile["avatar_path"] = file_path
            save_profile_for_user(username, profile)
            load_avatar()

    # ========================================================== Save Inf ==========================================================
    def save_inf():
        global error_email_label, error_dob_label
        name = name_entry.get().strip()
        mssv = mssv_entry.get().strip()
        email = email_entry.get().strip()
        dob = date_of_birth_entry.get().strip()
        address = address_text.get("1.0", "end").strip()

        if not name or not mssv or not email or not dob or not address:
            messagebox.showerror("", "Vui lòng nhập thông tin đầy đủ!")
            return

        if error_email_label:
            error_email_label.destroy()
            error_email_label = None
        if error_dob_label:
            error_dob_label.destroy()
            error_dob_label = None
            
        if not check_dob(dob):
            error_dob_label = Label(pro_win, text="Ngày sinh không hợp lệ!", fg="red")
            error_dob_label.place(x=315, y=260)
            return
        if not check_email(email):
            error_email_label = Label(pro_win, text="Email không hợp lệ!", fg="red", relief='flat', bd=0)
            error_email_label.place(x=530, y=260)
            return
        profile = load_profile_for_user(username) or {}
        avatar_path = profile.get("avatar_path", DEFAULT_AVATAR)
        profile = {
            "avatar_path": avatar_path,
            "name": name_entry.get(),
            "mssv": mssv_entry.get(),
            "dob": date_of_birth_entry.get(),
            "email": email_entry.get(),
            "sex": gender.get(),
            "address": address_text.get("1.0", END).strip(),
        }
        save_profile_for_user(username, profile)
        messagebox.showinfo("Thành công", "Hồ sơ đã được lưu!")
    def load_inf():
        profile = load_profile_for_user(username)
        name_entry.insert(0, profile.get("name",""))
        mssv_entry.insert(0, profile.get("mssv",""))
        date_of_birth_entry.insert(0, profile.get("dob",""))
        email_entry.insert(0, profile.get("email",""))
        gender.set(profile.get("sex","Nam"))
        address_text.insert("1.0", profile.get("address",""))
    
    # ========================================================== Delete Profile ==========================================================
    def delete_inf():
        cofirm = messagebox.askyesno("Xác nhận","Bạn có chắc chắn muốn xóa tài khoản chứ?")
        if cofirm:
            with open(PROFILE_FILE, "w", encoding="utf8") as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
            name_entry.delete(0, END)
            mssv_entry.delete(0, END)
            date_of_birth_entry.delete(0, END)
            email_entry.delete(0, END)
            gender.set('Nam')
            address_text.delete("1.0", END)

            with open(STUDY_RESULT, 'w', encoding="utf8") as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
            with open(LEARNING_STATISTICS, 'w', encoding="utf8") as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
            with open(USERS_FILE, 'w', encoding="utf8") as f:
                json.dump({}, f, ensure_ascii=False, indent=2)

        if os.path.exists(DEFAULT_AVATAR):
            default_img = Image.open(DEFAULT_AVATAR)
        else:
            default_img = Image.new("RGB", (160, 160), color="lightgray")

        default_img  = Image.open(DEFAULT_AVATAR).resize((160,160), Image.LANCZOS)
        avatar_photo = ImageTk.PhotoImage(default_img)
        avatar_label.configure(image=avatar_photo)
        avatar_label.photo_default = avatar_photo
        avatar_label.photo_current = avatar_photo
        avatar_label.image = avatar_photo

    Button(avatar_frame, text="🖼 Thay đổi ảnh", font=('Arial', 10, 'bold'),
        bg="#4CAF50", fg="white", command=change_avatar).pack(pady=5, fill='x')

    Button(avatar_frame, text="💾 Lưu hồ sơ", font=('Arial', 10, 'bold'),
        bg="#2196F3", fg="white", command=save_inf).pack(pady=5, fill='x')
    
    Button(avatar_frame, text="🗑 Xóa tài khoản", font=('Arial', 10, 'bold'),
        bg="#f44336", fg="white", command=delete_inf).pack(pady=5, fill='x')
    
    # ========================================================== INFORMATION ==========================================================
    # ====ROW 1====
    name_label = Label(frame,bg="#f5f5f5", text='Họ và tên:',width=8, anchor='w', font=('Abadi', 12, 'bold')).grid(row=1, column=1, pady=10)
    name_entry = Entry(frame, width=22)
    name_entry.grid(row=1, column=2, pady=10 )
    mssv_label = Label(frame,bg="#f5f5f5", text='MSSV:',width=5, anchor='w', font=('Abadi', 12, 'bold')).grid(row=1, column=3, pady=10)
    mssv_entry = Entry(frame, width=22)
    mssv_entry.grid(row=1, column=4, pady=10)
    # ====ROW 2====
    date_of_birth_label = Label(frame,bg="#f5f5f5", text='Ngày sinh:',width=8, anchor='w', font=('Abadi', 12, 'bold')).grid(row=2, column=1, pady=10)
    date_of_birth_entry = Entry(frame, width=22)
    date_of_birth_entry.grid(row=2, column=2, pady=10)
    email_label = Label(frame,bg="#f5f5f5", text='Email:',width=5, anchor='w', font=('Abadi', 12, 'bold')).grid(row=2, column=3, pady=10)
    email_entry = Entry(frame, width=22)
    email_entry.grid(row=2, column=4, pady=10)
    # ====ROW 3====
    gender = StringVar()
    gender.set('Nam')   
    gender_label = Label(frame,bg="#f5f5f5", text='Giới tính:',width=10, font=('Abadi', 12, 'bold')).grid(row=3, column=1,padx=5, pady=10)
    Radiobutton(frame,bg="#f5f5f5", text='Nam', variable=gender, value='Nam').grid(row=3, column=2, pady=10, sticky='w', padx=5)
    Radiobutton(frame,bg="#f5f5f5", text='Nữ', variable=gender, value='Nữ').grid(row=3, column=2, pady=10, sticky='w', padx=55)
    # ====ROW 4====
    address_label = Label(frame,bg="#f5f5f5", text='Địa chỉ:',width=10, font=('Abadi', 12, 'bold')).grid(row=4, column=1,padx=5, pady=5)
    address_text = Text(frame, width=30, height=3)
    address_text.grid(row=4, column=1, columnspan=6, padx=120, sticky='w')

    def back_to_main():
        pro_win.destroy()
        root.deiconify()
    Button(pro_win, text="⬅ Quay lại", font=('Arial', 12), bg="#f44336", fg="white", command=back_to_main).place(x=10, y=460)
    pro_win.protocol("WM_DELETE_WINDOW", back_to_main)
    load_inf()
    load_avatar()