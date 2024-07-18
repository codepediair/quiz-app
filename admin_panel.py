import customtkinter as ctk
from db_helper import DBHelper

class AdminPanel(ctk.CTk):
    def __init__(self, root):
        super().__init__(root)
        self.db = DBHelper()

        self.title("Admin Panel")
        self.geometry("600x400")

        self.filter_test_label = ctk.CTkLabel(self, text="Filter by Test")
        self.filter_test_label.pack(pady=5)
        self.filter_test_entry = ctk.CTkEntry(self)
        self.filter_test_entry.pack(pady=5)

        self.filter_username_label = ctk.CTkLabel(self, text="Filter by Username")
        self.filter_username_label.pack(pady=5)
        self.filter_username_entry = ctk.CTkEntry(self)
        self.filter_username_entry.pack(pady=5)

        self.filter_button = ctk.CTkButton(self, text="Filter", command=self.filter_results)
        self.filter_button.pack(pady=10)

        self.results_listbox = ctk.CTkListbox(self, width=500, height=200)
        self.results_listbox.pack(pady=20)

        self.load_results()

    def load_results(self):
        results = self.db.get_results()
        self.display_results(results)

    def filter_results(self):
        filter_test = self.filter_test_entry.get()
        filter_username = self.filter_username_entry.get()
        results = self.db.get_results(filter_test, filter_username)
        self.display_results(results)

    def display_results(self, results):
        self.results_listbox.delete(0, ctk.END)
        for result in results:
            self.results_listbox.insert(ctk.END, f"ID: {result[0]}, Username: {result[1]}, Score: {result[2]}, Test: {result[3]}")
