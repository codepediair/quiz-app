import customtkinter as ctk
from tkinter import messagebox
from db_helper import DBHelper
from register_page import RegisterPage
from home_page import HomePage

class LoginPage(ctk.CTk):
    def __init__(self, root):
        super().__init__(root)
        self.db = DBHelper()

        self.title("Login")
        self.geometry("400x300")

        self.username_label = ctk.CTkLabel(self, text="Username")
        self.username_label.pack(pady=10)
        self.username_entry = ctk.CTkEntry(self)
        self.username_entry.pack(pady=10)

        self.password_label = ctk.CTkLabel(self, text="Password")
        self.password_label.pack(pady=10)
        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.pack(pady=10)

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_button.pack(pady=10)
        
        self.register_button = ctk.CTkButton(self, text="Register", command=self.open_register_page)
        self.register_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = self.db.get_user(username, password)

        if user:
            messagebox.showinfo("Success", f"Welcome {user[3]}!")
            self.destroy()
            home_page = HomePage(root, user)
            home_page.pack(expand=True, fill='both')
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def open_register_page(self):
        self.destroy()
        register_page = RegisterPage(root)
        register_page.pack(expand=True, fill='both')
