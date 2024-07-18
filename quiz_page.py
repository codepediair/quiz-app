import customtkinter as ctk
from db_helper import DBHelper

class QuizPage(ctk.CTk):
    def __init__(self, root, user):
        super().__init__(root)
        self.db = DBHelper()
        self.user = user
        self.score = 0
        self.current_question_index = 0
        self.questions = [
            {"question": "Question 1?", "answers": ["Answer 1", "Answer 2", "Answer 3", "Answer 4"], "correct": 0},
            {"question": "Question 2?", "answers": ["Answer 1", "Answer 2", "Answer 3", "Answer 4"], "correct": 1},
            # Add more questions here
        ]

        self.title("Quiz")
        self.geometry("600x400")

        self.question_label = ctk.CTkLabel(self, text=self.questions[self.current_question_index]["question"], wraplength=500)
        self.question_label.pack(pady=20)

        self.var = ctk.IntVar()
        self.radio_buttons = []
        for i in range(4):
            radio = ctk.CTkRadioButton(self, text=self.questions[self.current_question_index]["answers"][i], variable=self.var, value=i)
            radio.pack(pady=10)
            self.radio_buttons.append(radio)

        self.next_button = ctk.CTkButton(self, text="Next", command=self.next_question)
        self.next_button.pack(pady=10)

    def next_question(self):
        if self.var.get() == self.questions[self.current_question_index]["correct"]:
            self.score += 1

        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.update_question()
        else:
            self.db.insert_result(self.user[1], self.score, "Test Type")
            ctk.messagebox.showinfo("Quiz Completed", f"Your score is {self.score}")
            from home_page import HomePage
            self.destroy()
            home_page = HomePage(root, self.user)
            home_page.pack(expand=True, fill='both')

    def update_question(self):
        self.question_label.config(text=self.questions[self.current_question_index]["question"])
        for i, radio in enumerate(self.radio_buttons):
            radio.config(text=self.questions[self.current_question_index]["answers"][i])
