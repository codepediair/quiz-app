import customtkinter as ctk
from login_page import LoginPage

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("400x300")
    login_page = LoginPage(root)
    login_page.pack(expand=True, fill='both')
    root.mainloop()
