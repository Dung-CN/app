from tkinter import *
from Database import *
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import json, os

# ================================ JSON ================================
def _ensure_study_file():
    if not os.path.exists(LEARNING_STATISTICS):
        with open(LEARNING_STATISTICS, "w", encoding="utf8") as f:
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
    with open(LEARNING_STATISTICS, "r", encoding="utf8") as f:
        try:
            data = json.load(f)
        except:
            data = {}
    if not isinstance(data, dict):
        data = {}
    data[username] = courses_list
    with open(LEARNING_STATISTICS, "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ================================ Calculate gpa ================================ 
def grade_to_4scale(gpa_10):
    gpa_10 = float(gpa_10)
    if gpa_10 >= 9: return 4.0
    if gpa_10 >= 8: return 3.5
    if gpa_10 >= 7: return 3.0
    if gpa_10 >= 6: return 2.5
    if gpa_10 >= 5: return 2.0
    if gpa_10 >= 4: return 1.5
    return 0.0
def calculate_gpa4(courses):       
    total_point = 0
    total_credit = 0
    for c in courses:
        try:
            credit = float(c.get("credit", 0))
            gpa_10 = float(c.get("average_score", 0))
            gpa_4 = grade_to_4scale(gpa_10)
            total_point += gpa_4 * credit
            total_credit += credit
        except:
            continue
    if total_credit == 0:
        return 0
    return round(total_point / total_credit, 2)

# ================================ Comment ================================
def generate_feedback(username ,score_data):
    try:
        with open(LEARNING_STATISTICS, 'r', encoding="utf8") as f:
            data = json.load(f)
            user_data = data.get(username, [])
            if user_data:
                gpa = float(user_data[-1].get("gpa", 0))
            else:
                gpa = 0.0
    except:
        gpa = 0.0
    if not score_data:
        return "Không có dữ liệu để nhận xét"
    max_score = max(score_data.values())
    max_subjects = [subj for subj, s in score_data.items() if s == max_score]
    max_subjects_str = ", ".join(max_subjects)

    nhan_xet = f"**BÁO CÁO TỔNG QUAN HỌC TẬP:**\n\n"
    nhan_xet += f"Điểm GPA học kỳ 1 là **{gpa}**.\n"
    nhan_xet += (f"Điểm trung bình cao nhất là môn **{max_subjects_str}** với **{max_score}**.\n"
                 f"Bạn đã thể hiện sự nỗ lực và khả năng tốt ở lĩnh vực này.\n")
    try:
        with open(STUDY_RESULT, 'r', encoding="utf8") as f:
            data = json.load(f)
            course_average_score = data.get(username, [])
    except (FileNotFoundError, json.JSONDecodeError):
        course_average_score = []
    excellent, good, fair, average = [], [], [], []
    for item in course_average_score:
        avg = float(item.get("average_score", 0))
        name = item.get("course_name", "Unknown")
        if avg >= 9.0:
            excellent.append((name, avg))
        elif avg >= 8.0:
            good.append((name, avg))
        elif avg >= 6.5:
            fair.append((name, avg))
        else:
            average.append((name, avg))
    if excellent:
        nhan_xet += "Các môn Xuất sắc: " + ", ".join([s[0] for s in excellent]) + ". Thành tích học tập **RẤT TỐT**. Tiếp tục duy trì phong độ xuất sắc này và thử thách bản thân với những môn nâng cao!\n"
    if good:
        nhan_xet += "Các môn Giỏi: " + ", ".join([s[0] for s in good]) + ". Thành tích học tập **TỐT**, bạn học tốt nhưng vẫn còn cơ hội để đạt xuất sắc. Hãy tập trung vào những chi tiết nhỏ và luyện tập thêm để nâng cao.\n"
    if fair:
        nhan_xet += "Các môn Khá: " + ", ".join([s[0] for s in fair]) + ". Môn này có thành tích khá, bạn nên ôn tập kỹ hơn, làm thêm bài tập và tham khảo tài liệu để nâng điểm lên mức Giỏi.\n"
    if average:
        nhan_xet += "Cần chú ý cải thiện môn: " + ", ".join([s[0] for s in average]) + ". Bạn phải dành thời gian nhiều hơn cho môn này, sắp xếp lại lịch học của mình sao cho hợp lý, học đúng cách để cải thiện tốt nhất\n"
    return nhan_xet

# ================================ Learning_windown ================================
def open_learning_statistics(root, username):
    root.withdraw()
    lst_win = Toplevel()
    lst_win.title("Thống kê học tập")
    lst_win.geometry("{}x{}+{}+{}".format(WINDOWN_WIDTH, WINDOWN_HEIGHT, WINDOWN_POSION_RIGHT, WINDOWN_POSION_DOWN))
    lst_win.resizable(False, False)
    lst_win.configure(bg="#f5f5f5")
    # ================================ Scroolbar ================================
    main_canvas = Canvas(lst_win, bg="#f5f5f5")
    main_canvas.pack(side='left', fill='both', expand=True)
    y_scrollbar = ttk.Scrollbar(lst_win, orient="vertical", command=main_canvas.yview)
    y_scrollbar.pack(side='right', fill='y')
    main_canvas.configure(yscrollcommand=y_scrollbar.set)
    frame_content = Frame(main_canvas)
    frame_content_window = main_canvas.create_window((0,10), window=frame_content, anchor='nw')

    # ---- Update scroll area, keep frame_content as wide as canvas ----
    def update_scrollregion(event):
        main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        main_canvas.itemconfig(frame_content_window, width=main_canvas.winfo_width())
    frame_content.bind("<Configure>", update_scrollregion)

    # ---- Mouse scroll ----
    def on_mousewheel(event):
        main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    main_canvas.bind_all("<MouseWheel>", on_mousewheel)

    # ================================ Frame Avatar + name + mssv ================================
    frame = Frame(frame_content, relief="flat", bg="#CCFF99")
    frame.pack(padx=5, pady=5, fill="x")
    # ----Avatar----
    try:
        with open(PROFILE_FILE, 'r', encoding="utf8") as f:
            data = json.load(f)
            user_data = data.get(username, {})
            name = user_data.get("name", "Unknown Student")
            mssv = user_data.get("mssv", "Unknown MSSV")
            avatar_path = user_data.get("avatar_path", "")
    except:
        name = "Unknown Name"
        mssv = "Unknown Mssv"
        avatar_path = ""
    if avatar_path and os.path.exists(avatar_path):
        avatar_img = Image.open(avatar_path)
    elif os.path.exists(DEFAULT_AVATAR):
        avatar_img = Image.open(DEFAULT_AVATAR)
    else:
        avatar_img = Image.new("RGB", (160, 160), color="lightgray")
    avatar_img = avatar_img.resize((50, 50), Image.LANCZOS)
    avatar_photo = ImageTk.PhotoImage(avatar_img)
    avatar_label = Label(frame, image=avatar_photo, bg='white', relief='flat')
    avatar_label.image = avatar_photo
    avatar_label.pack(side='left', padx=20)
    # ----Name + Mssv----
    info_frame = Frame(frame, relief='flat', bg="#CCFF99")
    info_frame.pack(side='left', anchor='w')
    name_label = Label(info_frame, bg="#CCFF99", text=name, font=('Abadi', 16, 'bold'))
    name_label.pack(anchor='w')
    mssv_label = Label(info_frame, bg="#CCFF99", text=mssv, font=('Abadi', 16, 'bold'))
    mssv_label.pack(anchor='w')

    # ==========================================================Treeview==========================================================
    cols = ('Năm học', 'HK', 'GPA', 'Tỷ lệ đạt môn', 'Xếp loại')
    tree_frame = Frame(frame_content, bg="#f5f5f5")
    tree_frame.pack(padx=10, pady=0, fill='both', expand=True)
    tree = ttk.Treeview(tree_frame, columns=cols, show='headings', selectmode='browse', height=6)
    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, width=100, anchor='center')
    tree.pack(side='left', fill='both', expand=True)

    # ----Điều chỉnh theo chiều rộng cửa sổ ----
    def resize_tree_columns(event):
        total_width = tree.winfo_width()
        col_width = total_width // len(cols)
        for c in cols:
            tree.column(c, width=col_width)
    tree.bind("<Configure>", resize_tree_columns)

    # ========================================================== Load information on the treeview ==========================================================
    courses = load_user_courses(username)  # Get information by username
    school_years = sorted({c.get("school_year") for c in courses})
    semesters = sorted({c.get("semester") for c in courses})
    all_data = []
    for year in school_years:
        for sem in semesters:
            semesters_course = [c for c in courses if c.get("school_year")==year and c.get("semester")==sem]
            if not semesters_course:
                continue
            gpa_sem = calculate_gpa4(semesters_course)
            passed = sum(1 for c in semesters_course if float(c.get("average_score",0)) >= 5)
            total = len(semesters_course)
            pass_rate = f"({passed/total*100:.0f}%)"
            rank = "Xuất Sắc" if gpa_sem >= 3.6 else "Giỏi" if gpa_sem >= 3.2 else "Khá" if gpa_sem >= 2.5 else "Trung bình"
            tree.insert("", "end", values=(year, sem, gpa_sem, pass_rate, rank))
            stat_item = {"school_year": year, "semester": sem, "gpa": gpa_sem, "pass_rate": pass_rate, "rank": rank}
            all_data.append(stat_item)
    save_user_courses(username, all_data)
    # ==========================================================Frame chart==========================================================
    chart_frame = Frame(frame_content, bg="#f5f5f5")
    chart_frame.pack(pady=(10,40), anchor='center')
    chart_widget = None
    def chart():
        nonlocal chart_widget
        if chart_widget is None:
            courses = load_user_courses(username)
            course_names = [i.get("course_name", "Unknown") for i in courses]
            average_scores = [float(i.get("average_score", 0)) for i in courses]

            fig, ax = plt.subplots(figsize=(5.6, 3.68))
            ax.plot(course_names, average_scores, marker='o', color='red', linewidth=2)
            ax.set_ylim(0,10)
            ax.set_title("Điểm trung bình", fontsize=11, fontweight='bold')
            ax.set_xlabel("Môn học", fontsize=8)
            ax.set_ylabel("Điểm", fontsize=8)
            ax.grid(True, linestyle='--', alpha=0.6)
            for i, v in enumerate(average_scores):
                ax.text(i, v+0.1, f"{v:.1f}", ha='center', fontsize=8)
            canvas_chart = FigureCanvasTkAgg(fig, master=chart_frame)
            canvas_chart.draw()
            chart_widget = canvas_chart.get_tk_widget()
            chart_widget.pack(anchor='w', pady=(5,0))
        else:
            chart_widget.destroy()
            chart_widget = None
    buton_chart = Button(chart_frame, text='Biểu đồ trực quan', font=('Abadi', 10, 'bold'), bg="#3498db", command=chart)
    buton_chart.pack(padx=10 ,pady=(10, 5), anchor='center')

    # ==========================================================Frame comment==========================================================
    comment_frame = Frame(frame_content, bg="#f5f5f5")
    comment_frame.pack(padx=10, pady=(0, 20), fill='x', expand=True)
    comment_text = Text(comment_frame, height=10, wrap='word', font=('Arial', 10))
    comment_text.pack(fill='both', expand=True)
    def show_feedback():
        try:
            with open(STUDY_RESULT, 'r', encoding="utf8") as f:
                data = json.load(f)
                score_data_list = data.get(username, [])
        except:
            score_data_list = []
        score_data = {item.get("course_name", "Unknown"): float(item.get("average_score", 0)) 
                  for item in score_data_list}
        feeback = generate_feedback(username, score_data)
        comment_text.delete('0.0', END)
        comment_text.insert(END, feeback)
    button_feedback = Button(comment_frame, text="Hiển thị nhận xét", font=('Abadi', 10, 'bold'),bg="#f39c12", command=show_feedback)
    button_feedback.pack(pady=5)

    # ---- Back to main ----
    def back_to_main():
        lst_win.destroy()
        root.deiconify()
    Button(lst_win, text="⬅ Quay lại", font=('Arial', 12), bg="#f44336", fg="white", command=back_to_main).place(x=10, y=460)
    lst_win.protocol("WM_DELETE_WINDOW", back_to_main) 