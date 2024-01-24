import tkinter as tk
from tkinter import Label, Entry, Button, messagebox
from password_manager import DbOperation, Root_window  # Import DbOperation and Root_window from your previous code

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Page")
        self.root.geometry("500x300+100+100")

        # Label with color
        self.label_username = Label(self.root, text="Username:", fg="blue",font=('Arial', 15))
        self.label_username.pack(pady=10)

        self.entry_username = Entry(self.root,font=('Arial', 15),bg="lightgrey")
        self.entry_username.pack(pady=5)

        # Label with color
        self.label_password = Label(self.root, text="Password:", fg="blue",font=('Arial', 15))
        self.label_password.pack()

        self.entry_password = Entry(self.root, show="*",font=('Arial', 15),bg="lightgrey")
        self.entry_password.pack(pady=5)

        self.login_button = Button(self.root, text="Login", command=self.login,font=('Arial', 15),fg="black")
        self.login_button.pack(pady=10)

        self.exit_button = Button(self.root, text="Exit", command=self.root.quit,font=('Arial', 15),fg="black")
        self.exit_button.pack(pady=10)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Perform authentication here (e.g., check credentials against a database)
        # For this example, I'll assume the username is "admin" and the password is "password"
        if username == "admin" and password == "1234":
            self.root.destroy()  # Close the login window
            self.open_password_manager()
        else:
            # Show an error message for incorrect credentials
            messagebox.showerror("Login Error", "Incorrect username or password")

    def open_password_manager(self):
        root = tk.Tk()
        db_class = DbOperation()  # You need to initialize DbOperation here
        db_class.create_table()
        root_class = Root_window(root, db_class)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    login_page = LoginPage(root)
    root.mainloop()
