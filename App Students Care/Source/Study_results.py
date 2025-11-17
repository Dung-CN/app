from tkinter import *
from Database import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
import json, os
import re

# ================================ INFORMATION FORMATH ================================
def check_score(score):
    is_valid = bool(re.fullmatch(r'^(10(\.0+)?)|([0-9](\.\d+)?)$', score))
    return is_valid
def check_year(year):
    is_valid = re.fullmatch(r'(20\d{2}-(20\d{2}))', year)
    if not is_valid:
        return False
    y1, y2 = map(int, year.split('-'))
    return y2 == y1 + 1
# ================================ JSON ================================ 
def _ensure_study_file(): # Check file existence
    if not os.path.exists(STUDY_RESULT):
        with open(STUDY_RESULT, "w", encoding="utf8") as f:
            json.dump({}, f, ensure_ascii=False, indent=2)

def load_user_courses(username):
    _ensure_study_file()
    with open(STUDY_RESULT, "r", encoding="utf8") as f:
        try:
            data = json.load(f)
        except:
            data = {}
    if not isinstance(data, dict):
        data = {}
    return data.get(username, [])

def save_user_courses(username, courses_list):
    _ensure_study_file()
    with open(STUDY_RESULT, "r", encoding="utf8") as f:
        try:
            data = json.load(f)
        except:
            data = {}
    if not isinstance(data, dict):
        data = {}
    data[username] = courses_list
    with open(STUDY_RESULT, "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
# =============================== Study_windown ===============================
def open_study_result(root, username):
    root.withdraw()
    std_win = Toplevel()
    std_win.title("Kết quả học tập")
    std_win.geometry("{}x{}+{}+{}".format(WINDOWN_WIDTH, WINDOWN_HEIGHT, WINDOWN_POSION_RIGHT, WINDOWN_POSION_DOWN))
    std_win.resizable(False, False)
    std_win.configure(bg="#f5f5f5")
    # ====Frame avatar + name + mssv =====
    frame = Frame(std_win, relief="flat", bg="#CCFF99")
    frame.pack(padx=5, pady=5, fill='x')
    # ---- Avatar ----
    try:
        with open(PROFILE_FILE, 'r', encoding="utf8") as f:
            data = json.load(f)
            user_data = data.get(username, {})
            name = user_data.get("name", "Unknown Student")
            mssv = user_data.get("mssv", "Unknown MSSV")
            avatar_path = user_data.get("avatar_path", "")
    except:
        name = "Unknown Student"
        mssv = "Unknown MSSV"
        avatar_path = ""
    if avatar_path and os.path.exists(avatar_path):
        avatar_img = Image.open(avatar_path)
    elif os.path.exists(DEFAULT_AVATAR):
        avatar_img = Image.open(DEFAULT_AVATAR)
    else:
        avatar_img = Image.new("RGB", (160, 160), color="lightgray")
    avatar_img = avatar_img.resize((50, 50), Image.LANCZOS)
    avatar_photo = ImageTk.PhotoImage(avatar_img)
    avatar_label = Label(frame, image=avatar_photo, bg="#CCFF99", relief="flat")
    avatar_label.image = avatar_photo
    avatar_label.pack(side="left", padx=20)
    # ========================================================== Frame con chứa Tên + MSSV ==========================================================
    info_frame = Frame(frame, bg="#CCFF99")
    info_frame.pack(side="left", anchor="w")
    name_label = Label(info_frame, bg="#CCFF99", text=name, font=('Abadi', 16, 'bold'))
    name_label.pack(anchor="w")
    mssv_label = Label(info_frame, bg="#CCFF99", text=mssv, font=('Abadi', 12, 'bold'))
    mssv_label.pack(anchor="w")
    
    def calculate_average_score(att, mid, fin): 
        try:
            att = float(att)    
            mid = float(mid)
            fin = float(fin)
            asc = att*0.1 + mid*0.2 + fin*0.7
            return round(asc, 2)
        except:
            return 0

    # ========================================================== Thêm inf vào bảng ==========================================================
    def add_record():
        attendance_score = attendance_score_entry.get().strip()
        midterm_score = midterm_score_entry.get().strip()
        final_score = final_score_entry.get().strip()
        school_year = school_year_entry.get().strip()

        if not check_score(attendance_score):
            messagebox.showerror("", "Điểm chuyên cần không hợp lệ!")
            return
        elif not check_score(midterm_score):
            messagebox.showerror("", "Điểm GK không hợp lệ!")
            return
        elif not check_score(final_score):
            messagebox.showerror("", "Điểm CK không hợp lệ!")
            return
        if not check_year(school_year):
            messagebox.showerror("", "Năm học không hợp lệ!")
            return

        average_score = calculate_average_score(attendance_score_entry.get(), midterm_score_entry.get(), final_score_entry.get())
        data = (
            course_code_entry.get().strip(),
            course_name_entry.get().strip(),
            semester_entry.get().strip(),
            credit_entry.get().strip(),
            attendance_score_entry.get().strip(),
            midterm_score_entry.get().strip(),
            final_score_entry.get().strip(),
            average_score,
            school_year_entry.get().strip()
        )
        if not data[0] or not data[1]:
            return
        tree.insert("", "end", values=data)
        data_1 = (
            course_code_entry,
            course_name_entry,
            semester_entry,
            credit_entry,
            attendance_score_entry,
            midterm_score_entry,
            final_score_entry,
            school_year_entry
            )
        for i in data_1:
            i.delete(0, END)
    # ========================================================== Save Json ==========================================================
    def save_json():
        all_data = []
        for item in tree.get_children():
            values = tree.item(item, "values")
            all_data.append(
                {
                "course_code": values[0],
                "course_name": values[1],
                "semester": values[2],
                "credit": values[3],
                "attendance_score": values[4],
                "midterm_score": values[5],
                "final_score": values[6],
                "average_score": values[7],
                "school_year": values[8]
                }
            )
        save_user_courses(username, all_data)
        messagebox.showinfo("Thông báo","Lưu dữ liệu thành công!")
    # ====Load json->tree ====
    def load_inf():
        courses = load_user_courses(username)
        for item in courses:
            tree.insert("","end", values=(
                item["course_code"],
                item["course_name"],
                item["semester"],
                item["credit"],
                item["attendance_score"],
                item["midterm_score"],
                item["final_score"],
                item.get("average_score", calculate_average_score(item["attendance_score"], item["midterm_score"], item["final_score"])),
                item["school_year"]
            ))
    # ======================= Delete record =======================
    def delete_record():
        selected = tree.focus()
        if not selected:
            return
        confirm = messagebox.askyesno("Thông báo", "Bạn chắc chắn muốn xóa Không!")
        if not confirm:
            return
        tree.delete(selected)
        for e in [course_code_entry, course_name_entry, semester_entry, credit_entry,attendance_score_entry, midterm_score_entry, final_score_entry, school_year_entry]:
            e.delete(0, END)
        messagebox.showinfo("Thông báo", "Xóa thành công!")
    # ======================= Update record =======================
    def update_record():
        selected = tree.focus()
        if not selected:
            return
        average_score = calculate_average_score(attendance_score_entry.get(), midterm_score_entry.get(), final_score_entry.get())
        new_data = (
            course_code_entry.get().strip(),
            course_name_entry.get().strip(),
            semester_entry.get().strip(),
            credit_entry.get().strip(),
            attendance_score_entry.get().strip(),
            midterm_score_entry.get().strip(),
            final_score_entry.get().strip(),
            average_score,
            school_year_entry.get().strip()
        )
        tree.item(selected, values=new_data)
        data_1 = (
            course_code_entry,
            course_name_entry,
            semester_entry,
            credit_entry,
            attendance_score_entry,
            midterm_score_entry,
            final_score_entry,
            school_year_entry
            )
        for i in data_1:
            i.delete(0, END)
        messagebox.showinfo("Thông Báo", "Cập nhật thành công!")
          
    # ======================= Frame Content =======================
    frame_1 = Frame(std_win, relief="groove", bd=2, bg="#f5f5f5")
    frame_1.pack(padx=5, pady=5, fill='x')
    course_code_label = Label(frame_1, bg="#f5f5f5", text='Mã môn học',width=10,anchor='w', font=('Abadi', 12, 'bold')).grid(row=1, column=0, padx=(10, 0), pady=10)
    course_code_entry = Entry(frame_1, width=15)
    course_code_entry.grid(row=1, column=1, pady=10)
    course_name_label = Label(frame_1, bg="#f5f5f5", text='Môn học',width=14, anchor='w', font=('Abadi', 12, 'bold')).grid(row=1, column=2, padx=(10, 0), pady=10)
    course_name_entry = Entry(frame_1, width=15)
    course_name_entry.grid(row=1, column=3, pady=10)
    semester_label = Label(frame_1, bg="#f5f5f5", text='Học kỳ',width=10, anchor='w', font=('Abadi', 12, 'bold')).grid(row=1, column=4, padx=(10, 0), pady=10)
    semester_entry = Entry(frame_1, width=15)
    semester_entry.grid(row=1, column=5, pady=10)

    credit_label = Label(frame_1, bg="#f5f5f5", text='Số tín chỉ',width=10, anchor='w', font=('Abadi', 12, 'bold')).grid(row=2, column=0, padx=(10, 0), pady=10)
    credit_entry = Entry(frame_1, width=15)
    credit_entry.grid(row=2, column=1, pady=10)
    attendance_score_label = Label(frame_1, bg="#f5f5f5", text='Điểm chuyên cần',width=14, anchor='w', font=('Abadi', 12, 'bold')).grid(row=2, column=2, padx=(10, 0), pady=10)
    attendance_score_entry = Entry(frame_1, width=15)
    attendance_score_entry.grid(row=2, column=3, pady=10)
    midterm_score_label = Label(frame_1, bg="#f5f5f5", text='Điểm GK',width=10, anchor='w', font=('Abadi', 12, 'bold')).grid(row=2, column=4, padx=(10, 0), pady=10)
    midterm_score_entry = Entry(frame_1, width=15)
    midterm_score_entry.grid(row=2, column=5, pady=10)

    final_score_label = Label(frame_1, bg="#f5f5f5", text="Điểm CK",width=10, anchor='w', font=('Abadi', 12, 'bold')).grid(row=3, column=0, padx=(10, 0), pady=10)
    final_score_entry = Entry(frame_1, width=15)
    final_score_entry.grid(row=3, column=1, pady=10)
    school_year_label = Label(frame_1, bg="#f5f5f5", text='Năm học',width=14, anchor='w', font=('Abadi', 12, 'bold')).grid(row=3, column=2, padx=(10, 0) , pady=10)
    school_year_entry = Entry(frame_1, width=15)
    school_year_entry.grid(row=3, column=3, pady=10)

    # ======================= Treeview =======================
    cols = ('Mã môn học', 'Môn học', 'Học kỳ', 'Số TC','Điểm chuyên cần', 'Điểm GK', 'Điểm CK', 'Điểm TB', 'Năm học')
    tree_frame = Frame(std_win)
    tree_frame.pack(padx=10, pady=50, fill='both', expand=True)

    tree = ttk.Treeview(tree_frame, columns=cols, show='headings', selectmode='browse')
    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, width=len(c)*5, anchor='center')
    tree.pack(side='left', fill='both', expand=True)

    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')
    tree.configure(yscrollcommand=vsb.set)

    # ======================= Click on treeView line =======================
    def on_tree_select(event):
        selected = tree.focus()
        if not selected:
            return
        values = tree.item(selected, "values")
        entries = [course_code_entry, course_name_entry, semester_entry, credit_entry,attendance_score_entry, midterm_score_entry, final_score_entry, school_year_entry]
        for e, v in zip(entries, [values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[8]]):
            e.delete(0, END)
            e.insert(0, v)
    tree.bind("<<TreeviewSelect>>", on_tree_select)

    # ======================= Function button =======================
    button_1 = Button(std_win, bg="#27ae60", text='🆕 Thêm', width=9, font=('Abadi', 13, 'bold'), command=add_record).place(x=100, y=220)
    button_2 = Button(std_win, bg="#2980b9", text='💾 Lưu', width=9, font=('Abadi', 13, 'bold'), command=save_json).place(x=230, y=220)
    button_3 = Button(std_win, bg="#f39c12", text='🖉Cập Nhật', width=9, font=('Abadi', 13, 'bold'), command=update_record).place(x=360, y=220)
    button_3 = Button(std_win, bg="#e74c3c", text='🗑 Xóa', width=9, font=('Abadi', 13, 'bold'), command=delete_record).place(x=490, y=220)
    
    load_inf() # Put information on the board
    def back_to_interface():
        std_win.destroy()
        root.deiconify()
    Button(std_win, text="⬅ Quay lại", font=('Arial', 12), bg="#f44336", fg="white", command=back_to_interface).place(x=10, y=460)
    std_win.protocol("WM_DELETE_WINDOW", back_to_interface)