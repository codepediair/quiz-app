import customtkinter as ctk
from tkinter import messagebox
from db_helper import DBHelper
from login_page import LoginPage

class RegisterPage(ctk.CTk):
    def __init__(self, root):
        super().__init__(root)
        self.db = DBHelper()

        self.title("Register")
        self.geometry("400x400")

        self.username_label = ctk.CTkLabel(self, text="Username")
        self.username_label.pack(pady=10)
        self.username_entry = ctk.CTkEntry(self)
        self.username_entry.pack(pady=10)

        self.password_label = ctk.CTkLabel(self, text="Password")
        self.password_label.pack(pady=10)
        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.pack(pady=10)

        self.first_name_label = ctk.CTkLabel(self, text="First Name")
        self.first_name_label.pack(pady=10)
        self.first_name_entry = ctk.CTkEntry(self)
        self.first_name_entry.pack(pady=10)

        self.last_name_label = ctk.CTkLabel(self, text="Last Name")
        self.last_name_label.pack(pady=10)
        self.last_name_entry = ctk.CTkEntry(self)
        self.last_name_entry.pack(pady=10)

        self.register_button = ctk.CTkButton(self, text="Register", command=self.register)
        self.register_button.pack(pady=10)
        
        self.back_button = ctk.CTkButton(self, text="Back to Login", command=self.back_to_login)
        self.back_button.pack(pady=10)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()

        if self.db.insert_user(username, password, first_name, last_name):
            messagebox.showinfo("Success", "Registration successful!")
            self.destroy()
            login_page = LoginPage(root)
            login_page.pack(expand=True, fill='both')
        else:
            messagebox.showerror("Error", "Username already exists")

    def back_to_login(self):
        self.destroy()
        login_page = LoginPage(root)
        login_page.pack(expand=True, fill='both')
