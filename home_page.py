import customtkinter as ctk
from quiz_page import QuizPage

class HomePage(ctk.CTk):
    def __init__(self, root, user):
        super().__init__(root)

        self.user = user
        self.title("Home")
        self.geometry("400x300")

        self.welcome_label = ctk.CTkLabel(self, text=f"Welcome, {user[3]} {user[4]}!")
        self.welcome_label.pack(pady=20)

        self.start_quiz_button = ctk.CTkButton(self, text="Start Quiz", command=self.start_quiz)
        self.start_quiz_button.pack(pady=10)
        
        self.admin_panel_button = ctk.CTkButton(self, text="Admin Panel", command=self.open_admin_panel)
        self.admin_panel_button.pack(pady=10)

    def start_quiz(self):
        self.destroy()
        quiz_page = QuizPage(root, self.user)
        quiz_page.pack(expand=True, fill='both')
    
    def open_admin_panel(self):
        if self.user[1] == "admin":
            from admin_panel import AdminPanel
            self.destroy()
            admin_panel = AdminPanel(root)
            admin_panel.pack(expand=True, fill='both')
        else:
            ctk.messagebox.showerror("Error", "Access Denied")
