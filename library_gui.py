import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from library_db import Database

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("800x600")
        self.root.config(bg="#f0f0f0")

        self.db = Database("library.db")

        # Title and Author labels and entry fields
        self.title_label = tk.Label(self.root, text="Title:", font=("Helvetica", 12), bg="#f0f0f0", fg="#333333")
        self.title_label.grid(row=0, column=0, padx=10, pady=(20, 5), sticky="e")
        self.title_var = tk.StringVar()
        self.title_entry = tk.Entry(self.root, textvariable=self.title_var, font=("Helvetica", 12))
        self.title_entry.grid(row=0, column=1, padx=10, pady=(20, 5))

        self.author_label = tk.Label(self.root, text="Author:", font=("Helvetica", 12), bg="#f0f0f0", fg="#333333")
        self.author_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.author_var = tk.StringVar()
        self.author_entry = tk.Entry(self.root, textvariable=self.author_var, font=("Helvetica", 12))
        self.author_entry.grid(row=1, column=1, padx=10, pady=5)

        # Add, Delete, Update, and Refresh buttons
        self.add_button = tk.Button(self.root, text="Add Book", command=self.add_book, font=("Helvetica", 12), bg="#4CAF50", fg="white")
        self.add_button.grid(row=2, column=1, pady=10, padx=(0, 10), sticky="ew")

        self.delete_button = tk.Button(self.root, text="Delete Book", command=self.remove_book, font=("Helvetica", 12), bg="#F44336", fg="white")
        self.delete_button.grid(row=3, column=1, pady=5, padx=(0, 10), sticky="ew")

        self.update_button = tk.Button(self.root, text="Update Status", command=self.update_status, font=("Helvetica", 12), bg="#2196F3", fg="white")
        self.update_button.grid(row=4, column=1, pady=5, padx=(0, 10), sticky="ew")

        self.refresh_button = tk.Button(self.root, text="Refresh", command=self.display_books, font=("Helvetica", 12), bg="#FF9800", fg="white")
        self.refresh_button.grid(row=5, column=1, pady=5, padx=(0, 10), sticky="ew")

        # Treeview to display book records
        self.tree = ttk.Treeview(self.root, columns=("ID", "Title", "Author", "Status"), show="headings")
        self.tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.tree.heading("Title", text="Title", anchor=tk.CENTER)
        self.tree.heading("Author", text="Author", anchor=tk.CENTER)
        self.tree.heading("Status", text="Status", anchor=tk.CENTER)
        self.tree.grid(row=0, column=2, rowspan=6, padx=10, pady=5, sticky="nsew")

        # Scrollbars for the treeview
        self.vsb = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.vsb.grid(row=0, column=3, rowspan=6, pady=5, sticky="ns")
        self.hsb = ttk.Scrollbar(self.root, orient="horizontal", command=self.tree.xview)
        self.hsb.grid(row=6, column=2, pady=5, sticky="ew")
        self.tree.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

        # Configure grid row and column weights
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        # Display initial book records
        self.display_books()

    def add_book(self):
        title = self.title_var.get()
        author = self.author_var.get()
        if title and author:
            self.db.add_book(title, author, "Available")
            messagebox.showinfo("Success", "Book added successfully!")
            self.clear_fields()
            self.display_books()
        else:
            messagebox.showerror("Error", "Please enter both title and author.")

    def remove_book(self):
        selected_item = self.tree.selection()
        if selected_item:
            book_id = self.tree.item(selected_item)['values'][0]
            self.db.delete_book(book_id)
            self.display_books()
            messagebox.showinfo("Success", "Book deleted successfully!")
        else:
            messagebox.showerror("Error", "Please select a book to delete.")

    def update_status(self):
        selected_item = self.tree.selection()
        if selected_item:
            book_id = self.tree.item(selected_item)['values'][0]
            new_status = simpledialog.askstring("Update Book", "Enter new status (Available/Issued):")
            if new_status:
                self.db.update_book_status(book_id, new_status)
                self.display_books()
        else:
            messagebox.showerror("Error", "Please select a book to update.")

    def display_books(self):
        self.clear_display()
        rows = self.db.fetch_all_books()
        for i, row in enumerate(rows, start=1):
            self.tree.insert("", "end", values=(row[0], row[1], row[2], row[3]))

    def clear_display(self):
        for record in self.tree.get_children():
            self.tree.delete(record)

    def clear_fields(self):
        self.title_var.set("")
        self.author_var.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
