from tkinter import *
from PIL import Image, ImageTk
from Database import *
import Profile
import Study_results
import Learning_statistics
import json, os

# ==================== Get information from file.json ====================
def load_user_data(file, username):
    if not os.path.exists(file):
        return {}
    with open(file, 'r', encoding='utf8') as f:
        try:
            data = json.load(f)
        except:
            return {}
    if isinstance(data, dict):
        return data.get(username, {})
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                if item.get("username") == username:
                    return item
        return {}
    return {}

def open_interface(pw_win, username):
    pw_win.withdraw()
    root = Toplevel()
    root.title('Student Care')
    root.geometry('{}x{}+{}+{}'.format(WINDOWN_WIDTH, WINDOWN_HEIGHT, WINDOWN_POSION_RIGHT, WINDOWN_POSION_DOWN))
    root.resizable(False, False)
    root.configure(bg="#f5f5f5")
    profile = load_user_data("profile.json", username) or {}
    study_result = load_user_data("study_result.json", username) or {}
    learning_stats = load_user_data("learning_statistics.json", username) or {}
    style = {
        "font": ("Arial", 14, "bold"),
        "width": 18,
        "relief": "raised",
        "bd": 2,
    }
    # ====Icon====
    icon_path = r"C:\Users\Nga\Desktop\APP STUDENTS CARE\Images\icon_students_care.png"
    icon = Image.open(icon_path).resize((32, 32), Image.LANCZOS)
    icon_tk = ImageTk.PhotoImage(icon)
    root.iconphoto(True, icon_tk)
    root.icon_tk = icon_tk
    # ====HEADING====
    frame = Frame(root, relief='flat')
    frame.pack(pady=0 ,anchor='center', fill='x')
    heading = Label(frame, height=3, text="🎓 Student Care", font=("Helvetica", 22, "bold"), bg="#2c3e50", fg="white")
    heading.pack(anchor='center', fill='both', expand=True)
    # ====CONTENT====
    button_1 = Button(root, text='Hồ Sơ Cá Nhân', **style, bg="#428bca", fg='black', activebackground="#3498db", activeforeground="white", command=lambda : Profile.open_profile(root, username))
    button_1.pack(anchor='center', pady=(50, 20))
    button_2 = Button(root, text='Kết Quả Học Tập', **style, bg="#5cb85c", fg='black', activebackground="#2ecc71", activeforeground="white", command=lambda: Study_results.open_study_result(root, username))
    button_2.pack(anchor='center', pady=20)
    button_3 = Button(root, text='Thống Kê Học Tập', **style, bg="#f0ad4e", fg='black', activebackground="#f39c12", activeforeground="white", command=lambda: Learning_statistics.open_learning_statistics(root, username))
    button_3.pack(anchor='center', pady=20)
    button_4 = Button(root, text='Thoát', **style, bg="#d9534f", fg='black', activebackground="#e74c3c", activeforeground="white", command=root.quit)
    button_4.pack(anchor='center', pady=20)
    root.protocol("WM_DELETE_WINDOW", lambda: os._exit(0))
