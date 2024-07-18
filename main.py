import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from bidi import algorithm

ctk.set_appearance_mode("dark")

class LoginPage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(algorithm.get_display("ورود یا ثبت نام"))
        self.geometry("400x300")

        self.create_widgets()

    def create_widgets(self):
        self.username_label = ctk.CTkLabel(self, text=algorithm.get_display("نام کاربری"), font=("IRANSansXFaNum-Bold", 14), justify='right')
        self.username_label.pack(pady=(20, 5))

        self.username_entry = ctk.CTkEntry(self, width=200)
        self.username_entry.pack(pady=5)

        self.password_label = ctk.CTkLabel(self, text="رمز ورود", font=("IRANSansX", 14))
        self.password_label.pack(pady=5)

        self.password_entry = ctk.CTkEntry(self, width=200, show='*')
        self.password_entry.pack(pady=5)

        self.login_button = ctk.CTkButton(self, text="ورود",font=("IRANSansX", 14), command=self.check_login)
        self.login_button.pack(pady=20)

        self.bind('<Return>', self.login_wtih_enter)

        self.register_button = ctk.CTkButton(self, text="ثبت نام", font=("IRANSansX", 14), command=self.open_register)
        self.register_button.pack(pady=10)
    
    def login_wtih_enter(self , event):
        self.check_login()

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect('quiz_app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            if user[5] == 1:
                self.destroy()
                admin_panel = AdminPanel()
                admin_panel.mainloop()
            else:
                self.destroy()
                test_selection_page = TestSelectionPage(username)
                test_selection_page.mainloop()
        else:
            messagebox.showerror("خطا", "نام کاربری یا رمز ورود اشتباه است")

    def open_register(self):
        self.destroy()
        register_page = RegisterPage()
        register_page.mainloop()

class RegisterPage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ثبت نام")
        self.geometry("400x500")

        self.create_widgets()

    def create_widgets(self):
        self.first_name_label = ctk.CTkLabel(self, text="نام", font=("IRANSansX", 14))
        self.first_name_label.pack(pady=(20, 5))

        self.first_name_entry = ctk.CTkEntry(self, width=200)
        self.first_name_entry.pack(pady=5)

        self.last_name_label = ctk.CTkLabel(self, text="نام خانوادگی", font=("IRANSansX", 14))
        self.last_name_label.pack(pady=5)

        self.last_name_entry = ctk.CTkEntry(self, width=200)
        self.last_name_entry.pack(pady=5)

        self.username_label = ctk.CTkLabel(self, text="شماره تلفن", font=("IRANSansX", 14))
        self.username_label.pack(pady=5)

        self.username_entry = ctk.CTkEntry(self, width=200)
        self.username_entry.pack(pady=5)

        self.password_label = ctk.CTkLabel(self, text="رمز عبور", font=("IRANSansX", 14))
        self.password_label.pack(pady=5)

        self.password_entry = ctk.CTkEntry(self, width=200, show='*')
        self.password_entry.pack(pady=5)

        self.confirm_password_label = ctk.CTkLabel(self, text="تایید رمز عبور", font=("IRANSansX", 14))
        self.confirm_password_label.pack(pady=5)

        self.confirm_password_entry = ctk.CTkEntry(self, width=200, show='*')
        self.confirm_password_entry.pack(pady=5)

        self.register_button = ctk.CTkButton(self, text="ثبت نام", font=("IRANSansX", 14), command=self.register_user)
        self.register_button.pack(pady=20)

        self.login_button = ctk.CTkButton(self, text="بازکشت به صفحه ورود", font=("IRANSansX", 14), command=self.open_login)
        self.login_button.pack(pady=10)

    def register_user(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        conn = sqlite3.connect('quiz_app.db')
        cursor = conn.cursor()

        try:
            cursor.execute('INSERT INTO users (username, password, first_name, last_name) VALUES (?, ?, ?, ?)', (username, password, first_name, last_name))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful")
            self.open_login()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        finally:
            conn.close()

    def open_login(self):
        self.destroy()
        login_app = LoginPage()
        login_app.mainloop()

class TestSelectionPage(ctk.CTk):
    def __init__(self, username):
        super().__init__()
        self.title("Select Test")
        self.geometry("400x300")
        self.username = username

        self.create_widgets()

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text="یکی از تست ها را انتخاب کنید", font=("IRANSansX", 18, "bold"))
        self.title_label.pack(pady=20)

        self.bdi_button = ctk.CTkButton(self, text="BECK Test",font=("IRANSansX", 14), command=self.open_bdi_test)
        self.bdi_button.pack(pady=10)

        self.phq9_button = ctk.CTkButton(self, text="PHQ-9 Test",font=("IRANSansX", 14), command=self.open_phq9_test)
        self.phq9_button.pack(pady=10)

        self.gad7_button = ctk.CTkButton(self, text="GAD-7 Test",font=("IRANSansX", 14), command=self.open_gad7_test)
        self.gad7_button.pack(pady=10)

        self.mspss_button = ctk.CTkButton(self, text="MSPSS Test",font=("IRANSansX", 14), command=self.open_mspss_test)
        self.mspss_button.pack(pady=10)
    def open_bdi_test(self):
        self.destroy()
        bdi_ii_test = BDI_II_Test(self.username)
        bdi_ii_test.mainloop()

    def open_phq9_test(self):
        self.destroy()
        phq9_test = PHQ9_Test(self.username)
        phq9_test.mainloop()

    def open_gad7_test(self):
        self.destroy()
        gad7_test = GAD7_Test(self.username)
        gad7_test.mainloop()

    def open_mspss_test(self):
        self.destroy()
        mspss_test = MSPSS_Test(self.username)
        mspss_test.mainloop()

class BDI_II_Test(ctk.CTk):
    def __init__(self, username):
        super().__init__()
        self.title("BDI-II Test")
        self.geometry("600x400")

        self.username = username

        self.questions = [
            {
                "question": "من با امید و اشتیاق به آینده نگاه می کنم",
                "options": [
                    "کاملا مخالفم",
                    "مخالفم",
                    "نظری ندارم",
                    "موافقم",
                    "کاملا موافقم"
                ],
                "score": [1, 2, 3, 4, 5]
            },
            {
                "question": "چون نمی توانم هیچ کاری برای بهتر کردن اوضاع خود انجام دهم، شاید دست از تلاش هم بردارم",
                "options": [
                    "کاملا مخالفم",
                    "مخالفم",
                    "نظری ندارم",
                    "موافقم",
                    "کاملا موافقم"
                ],
                "score": [1, 2, 3, 4, 5]
            },
            # Add more questions as needed
        ]

        self.current_question_index = 0
        self.answers = {idx: ctk.IntVar() for idx in range(len(self.questions))}

        self.create_widgets()
        self.update_question()

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text="BDI-II Test", font=("IRANSansX", 18, "bold"))
        self.title_label.pack(pady=10)

        self.question_label = ctk.CTkLabel(self, text="", font=("IRANSansX", 14))
        self.question_label.pack(anchor="center", pady=(10, 5), expand=True)

        self.options_frame = ctk.CTkFrame(self)
        self.options_frame.pack(anchor="center", pady=10, expand=True)

        self.radio_buttons = []
        for i in range(1,6):
            rb = ctk.CTkRadioButton(self.options_frame, text="", variable=None, value=i)
            rb.pack(anchor="w", pady=5)  # Added padding to radio buttons
            self.radio_buttons.append(rb)

        self.previous_button = ctk.CTkButton(self, text="Previous", command=self.previous_question, state="disabled")
        self.previous_button.pack(side="left", padx=20, pady=20)

        self.next_button = ctk.CTkButton(self, text="Next", command=self.next_question)
        self.next_button.pack(side="left", padx=20, pady=20)

        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.calculate_score, state="disabled")
        self.submit_button.pack(side="right", padx=20, pady=20)

    def update_question(self):
        question_data = self.questions[self.current_question_index]
        self.question_label.configure(text=f"{self.current_question_index + 1}. {question_data['question']}")

        for idx, option in enumerate(question_data["options"]):
            self.radio_buttons[idx].configure(text=option, variable=self.answers[self.current_question_index])

        self.previous_button.configure(state="normal" if self.current_question_index > 0 else "disabled")
        self.next_button.configure(state="normal" if self.current_question_index < len(self.questions) - 1 else "disabled")
        self.submit_button.configure(state="normal" if self.current_question_index == len(self.questions) - 1 else "disabled")

    def next_question(self):
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
            self.update_question()

    def previous_question(self):
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.update_question()

    def calculate_score(self):
        total_score = sum(answer.get() for answer in self.answers.values())
        self.save_score(total_score)
        # messagebox.showinfo("تست کامل شد", f"امتیاز شما: {total_score}")
        self.return_to_selection()

    def save_score(self, score):
        conn = sqlite3.connect('quiz_app.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO results (username, score, test_type) VALUES (?, ?, ?)', (self.username, score, 'BDI-II'))
        conn.commit()
        conn.close()

    def return_to_selection(self):
        self.destroy()
        test_selection_page = TestSelectionPage(self.username)
        test_selection_page.mainloop()

class PHQ9_Test(ctk.CTk):
    def __init__(self, username):
        super().__init__()
        self.title("PHQ-9 Test")
        self.geometry("600x400")

        self.username = username

        self.questions = [
            {
                "question": "علاقه کم، لذت بردن اندک در انجام کارها",
                "options": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "score": [1, 2, 3, 4]
            },
            {
                "question": "احساس غم، افسردگی و ناراحتی",
                "options": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "score": [1, 2, 3, 4]
            },
            # Add more questions as needed
        ]

        self.current_question_index = 0
        self.answers = {idx: ctk.IntVar() for idx in range(len(self.questions))}

        self.create_widgets()
        self.update_question()

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text="PHQ-9 Test", font=("IRANSansX", 18, "bold"))
        self.title_label.pack(pady=10)

        self.question_label = ctk.CTkLabel(self, text="", font=("IRANSansX", 14))
        self.question_label.pack(anchor="center", pady=(10, 5), expand=True)

        self.options_frame = ctk.CTkFrame(self)
        self.options_frame.pack(anchor="center", pady=10, expand=True)

        self.radio_buttons = []
        for i in range(4):
            rb = ctk.CTkRadioButton(self.options_frame, text="", variable=None, value=i)
            rb.pack(anchor="w", pady=5)  # Added padding to radio buttons
            self.radio_buttons.append(rb)

        self.previous_button = ctk.CTkButton(self, text="Previous", command=self.previous_question, state="disabled")
        self.previous_button.pack(side="left", padx=20, pady=20)

        self.next_button = ctk.CTkButton(self, text="Next", command=self.next_question)
        self.next_button.pack(side="left", padx=20, pady=20)

        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.calculate_score, state="disabled")
        self.submit_button.pack(side="right", padx=20, pady=20)

    def update_question(self):
        question_data = self.questions[self.current_question_index]
        self.question_label.configure(render_text=f"{self.current_question_index + 1}. {question_data['question']}")

        for idx, option in enumerate(question_data["options"]):
            self.radio_buttons[idx].configure(text=option, variable=self.answers[self.current_question_index])

        self.previous_button.configure(state="normal" if self.current_question_index > 0 else "disabled")
        self.next_button.configure(state="normal" if self.current_question_index < len(self.questions) - 1 else "disabled")
        self.submit_button.configure(state="normal" if self.current_question_index == len(self.questions) - 1 else "disabled")

    def next_question(self):
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
            self.update_question()

    def previous_question(self):
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.update_question()

    def calculate_score(self):
        total_score = sum(answer.get() for answer in self.answers.values())
        self.save_score(total_score)
        messagebox.showinfo("تست کامل شد", f"امتیاز شما: {total_score}")
        self.return_to_selection()

    def save_score(self, score):
        conn = sqlite3.connect('quiz_app.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO results (username, score, test_type) VALUES (?, ?, ?)', (self.username, score, 'PHQ-9'))
        conn.commit()
        conn.close()

    def return_to_selection(self):
        self.destroy()
        test_selection_page = TestSelectionPage(self.username)
        test_selection_page.mainloop()

class GAD7_Test(ctk.CTk):
    def __init__(self, username):
        super().__init__()
        self.title("GAD-7 Test")
        self.geometry("600x400")

        self.username = username

        self.questions = [
            {
                "question": "احساس عصبی بودن، اضطراب یا نزدیک مرز بودن",
                "options": [
                    "اصلا",
                    "چندین روز",
                    "بیش از نیمی از روز",
                    "تقریبا هر روز"
                ],
                "score": [0, 1, 2, 3]
            },
            {
                "question": "قادر نبودن به جلوگیری یا کنترل نگرانی",
                "options": [
                    "اصلا",
                    "چندین روز",
                    "بیش از نیمی از روز",
                    "تقریبا هر روز"
                ],
                "score": [0, 1, 2, 3]
            },
            # Add more questions as needed
        ]

        self.current_question_index = 0
        self.answers = {idx: ctk.IntVar() for idx in range(len(self.questions))}

        self.create_widgets()
        self.update_question()

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text="GAD-7 Test", font=("IRANSansX", 18, "bold"))
        self.title_label.pack(pady=10)

        self.question_label = ctk.CTkLabel(self, text="", font=("IRANSansX", 14))
        self.question_label.pack(anchor="center", pady=(10, 5), expand=True)

        self.options_frame = ctk.CTkFrame(self)
        self.options_frame.pack(anchor="center", pady=10, expand=True)

        self.radio_buttons = []
        for i in range(4):
            rb = ctk.CTkRadioButton(self.options_frame, text="", variable=None, value=i)
            rb.pack(anchor="w", pady=5)  # Added padding to radio buttons
            self.radio_buttons.append(rb)

        self.previous_button = ctk.CTkButton(self, text="Previous", command=self.previous_question, state="disabled")
        self.previous_button.pack(side="left", padx=20, pady=20)

        self.next_button = ctk.CTkButton(self, text="Next", command=self.next_question)
        self.next_button.pack(side="left", padx=20, pady=20)

        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.calculate_score, state="disabled")
        self.submit_button.pack(side="right", padx=20, pady=20)

    def update_question(self):
        question_data = self.questions[self.current_question_index]
        self.question_label.configure(text=f"{self.current_question_index + 1}. {question_data['question']}")

        for idx, option in enumerate(question_data["options"]):
            self.radio_buttons[idx].configure(text=option, variable=self.answers[self.current_question_index])

        self.previous_button.configure(state="normal" if self.current_question_index > 0 else "disabled")
        self.next_button.configure(state="normal" if self.current_question_index < len(self.questions) - 1 else "disabled")
        self.submit_button.configure(state="normal" if self.current_question_index == len(self.questions) - 1 else "disabled")

    def next_question(self):
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
            self.update_question()

    def previous_question(self):
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.update_question()

    def calculate_score(self):
        total_score = sum(answer.get() for answer in self.answers.values())
        self.save_score(total_score)
        messagebox.showinfo("تست کامل شد", f"امتیاز شما: {total_score}")
        self.return_to_selection()

    def save_score(self, score):
        conn = sqlite3.connect('quiz_app.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO results (username, score, test_type) VALUES (?, ?, ?)', (self.username, score, 'GAD-7'))
        conn.commit()
        conn.close()

    def return_to_selection(self):
        self.destroy()
        test_selection_page = TestSelectionPage(self.username)
        test_selection_page.mainloop()

class MSPSS_Test(ctk.CTk):
    def __init__(self, username):
        super().__init__()
        self.title("MSPSS Test")
        self.geometry("600x400")

        self.username = username

        self.questions = [
            {
                "question": "خانواده ام مایلند تا در تصمیم گیری ها به من کمک کنند",
                "options": [
                    "کاملا موافقم",
                    "موافق",
                    "بی نظر",
                    "مخالف",
                    "کاملا مخالف",
                ],
                "score": [1, 2, 3, 4, 5]
            },
            {
                "question": "اعضای خانواده واقعا سعی می کنند تا به من کمک کنند",
                "options": [
                    "کاملا موافقم",
                    "موافق",
                    "بی نظر",
                    "مخالف",
                    "کاملا مخالف",
                ],
                "score": [1, 2, 3, 4, 5]
            },
            # Add more questions as needed
        ]

        self.current_question_index = 0
        self.answers = {idx: ctk.IntVar() for idx in range(len(self.questions))}

        self.create_widgets()
        self.update_question()

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text="MSPSS Test", font=("IRANSansX", 18, "bold"))
        self.title_label.pack(pady=10)

        self.question_label = ctk.CTkLabel(self, text="", font=("IRANSansX", 14))
        self.question_label.pack(anchor="center", pady=(10, 5), expand=True)

        self.options_frame = ctk.CTkFrame(self)
        self.options_frame.pack(anchor="center", pady=10, expand=True)

        self.radio_buttons = []
        for i in range(5):
            rb = ctk.CTkRadioButton(self.options_frame, text="", variable=None, value=i)
            rb.pack(anchor="w", pady=5)  # Added padding to radio buttons
            self.radio_buttons.append(rb)

        self.previous_button = ctk.CTkButton(self, text="Previous", command=self.previous_question, state="disabled")
        self.previous_button.pack(side="left", padx=20, pady=20)

        self.next_button = ctk.CTkButton(self, text="Next", command=self.next_question)
        self.next_button.pack(side="left", padx=20, pady=20)

        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.calculate_score, state="disabled")
        self.submit_button.pack(side="right", padx=20, pady=20)

    def update_question(self):
        question_data = self.questions[self.current_question_index]
        self.question_label.configure(text=f"{self.current_question_index + 1}. {question_data['question']}")

        for idx, option in enumerate(question_data["options"]):
            self.radio_buttons[idx].configure(text=option, variable=self.answers[self.current_question_index])

        self.previous_button.configure(state="normal" if self.current_question_index > 0 else "disabled")
        self.next_button.configure(state="normal" if self.current_question_index < len(self.questions) - 1 else "disabled")
        self.submit_button.configure(state="normal" if self.current_question_index == len(self.questions) - 1 else "disabled")

    def next_question(self):
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
            self.update_question()

    def previous_question(self):
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.update_question()

    def calculate_score(self):
        total_score = sum(answer.get() for answer in self.answers.values())
        self.save_score(total_score)
        messagebox.showinfo("تست کامل شد", f"امتیاز شما: {total_score}")
        self.return_to_selection()

    def save_score(self, score):
        conn = sqlite3.connect('quiz_app.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO results (username, score, test_type) VALUES (?, ?, ?)', (self.username, score, 'MSPSS'))
        conn.commit()
        conn.close()

    def return_to_selection(self):
        self.destroy()
        test_selection_page = TestSelectionPage(self.username)
        test_selection_page.mainloop()

# Admin Panel
class AdminPanel(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("پنل مدیریت")
        self.geometry("800x600")

        self.filter_frame = ctk.CTkFrame(self)
        self.filter_frame.pack(pady=20)

        self.filter_label = ctk.CTkLabel(self.filter_frame, text="Filter by:")
        self.filter_label.grid(row=0, column=0, padx=10, pady=5)

        self.test_name_var = ctk.StringVar()
        self.test_name_var.trace_add("write", self.filter_results)
        self.test_name_entry = ctk.CTkEntry(self.filter_frame, textvariable=self.test_name_var)
        self.test_name_entry.grid(row=0, column=1, padx=10, pady=5)

        self.results_tree = ttk.Treeview(self, columns=("Username", "Score", "Test Type"))
        self.results_tree.heading("#0", text="ID")
        self.results_tree.column("#0", width=50)
        self.results_tree.heading("Username", text="Username")
        self.results_tree.heading("Score", text="Score")
        self.results_tree.heading("Test Type", text="Test Type")
        self.results_tree.pack(padx=20, pady=10, fill="both", expand=True)

        self.load_results()

    def load_results(self):
        conn = sqlite3.connect('quiz_app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM results')
        results = cursor.fetchall()
        conn.close()

        self.results_tree.delete(*self.results_tree.get_children())

        for result in results:
            self.results_tree.insert("", "end", text=result[0], values=(result[1], result[2], result[3]))

    def filter_results(self, *args):
        filter_value = self.test_name_var.get()

        conn = sqlite3.connect('quiz_app.db')
        cursor = conn.cursor()
        if filter_value:
            cursor.execute('SELECT * FROM results WHERE test_type LIKE ? OR username LIKE ?', (f'%{filter_value}%',f'%{filter_value}%'))
        else:
            cursor.execute('SELECT * FROM results')
        filtered_results = cursor.fetchall()
        conn.close()

        self.results_tree.delete(*self.results_tree.get_children())

        for result in filtered_results:
            self.results_tree.insert("", "end", text=result[0], values=(result[1], result[2], result[3]))

# Database setup
def setup_database():
    conn = sqlite3.connect('quiz_app.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        first_name TEXT,
        last_name TEXT,
        is_admin INTEGER DEFAULT 0
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        score INTEGER,
        test_type TEXT,
        FOREIGN KEY(username) REFERENCES users(username)
    )
    ''')

    # Add a default admin user
    cursor.execute('SELECT * FROM users WHERE username = ?', ('admin',))
    admin_exists = cursor.fetchone()
    if not admin_exists:
        cursor.execute('INSERT INTO users (username, password, first_name, last_name, is_admin) VALUES (?, ?, ?, ?, ?)', ('admin', 'admin', 'Admin', 'User', 1))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
    app = LoginPage()
    app.mainloop()
