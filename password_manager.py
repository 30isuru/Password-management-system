import tkinter as tk
from tkinter import CENTER, Label, Button, Entry, Frame, Tk, END, Toplevel
from tkinter import ttk
from db_operations import DbOperation
import random
import string

class Root_window:
    def __init__(self, root, db):
        self.db = db
        self.root = root
        self.root.title("Password Manager")

        head_title = Label(self.root, text="Password Manager", width=30,
                           bg="yellow", font=('Arial', 15), padx=10, pady=10, justify=CENTER,
                           anchor="center")
        head_title.grid(columnspan=4, padx=140, pady=20)

        self.crud_frame = Frame(self.root, highlightbackground="black", highlightthickness=1, padx=10, pady=30)
        self.crud_frame.grid()

        self.create_entry_labels()
        self.create_entry_boxes()
        self.create_crud_buttons()
        self.search_entry = Entry(self.crud_frame, width=25, font=('Arial', 15))
        self.search_entry.grid(row=self.row_no, column=self.col_no)

        self.col_no += 1  # Increment the column number to position the button to the right
        search_button = Button(self.crud_frame, text="Search", bg="Yellow",
                               font=('Arial', 12), width=20, command=self.search_record)
        search_button.grid(row=self.row_no, column=self.col_no, padx=5, pady=5)

        self.create_record_tree()

        # Add an Exit button to the bottom right corner
        exit_button = Button(self.root, text="Exit", bg="red", fg="white", font=('Arial', 12), width=10, command=self.root.destroy)
        exit_button.place(relx=1, rely=1, anchor="se")

        # Add a "Generate Password" button
        self.col_no += 1
        generate_button = Button(self.crud_frame, text="Generate Password", bg="lightblue",
                                 font=('Arial', 12), width=20, command=self.generate_password)
        generate_button.grid(row=self.row_no, column=self.col_no, padx=5, pady=5)

        # Entry box to display the generated password
        self.col_no += 1
        self.generated_password_entry = Entry(self.crud_frame, width=15, background="lightgrey", font=('Arial', 15),
                                              justify=CENTER)
        self.generated_password_entry.grid(row=self.row_no, column=self.col_no, padx=5, pady=5)

        # Add a "Copy Generated Password" button
        self.col_no += 1
        copy_generated_password_button = Button(self.crud_frame, text="Copy Generated Password", bg="orange",
                                                font=('Arial', 12), width=20, command=self.copy_generated_password)
        copy_generated_password_button.grid(row=self.row_no, column=self.col_no, padx=5, pady=5)

    def create_entry_labels(self):
        self.col_no, self.row_no = 0, 0
        labels_info = ('ID', 'Website', 'Username', 'Password')
        for label_info in labels_info:
            Label(self.crud_frame, text=label_info, bg='brown', fg="white", font=('Arial', 15), padx=5,
                  pady=2).grid(row=self.row_no, column=self.col_no, padx=15, pady=2)
            self.col_no += 1

    def create_crud_buttons(self):
        self.row_no += 1
        self.col_no = 0
        buttons_info = (('Save', 'green', self.save_record), ('Update', 'blue', self.update_record),
                        ('Delete', 'red', self.delete_record),
                        ('PW Copy', 'violet', self.copy_password), ('Show All Records', 'Purple', self.show_record))
        for btn_info in buttons_info:
            if btn_info[0] == 'Show All Records':
                self.row_no += 1
                self.col_no = 0
            Button(self.crud_frame, text=btn_info[0], bg=btn_info[1], fg="black", font=('Arial', 10), padx=2,
                   pady=1, width=10, command=btn_info[2]).grid(row=self.row_no, column=self.col_no, padx=2, pady=3)
            self.col_no += 1

    def create_entry_boxes(self):
        self.row_no += 1
        self.entry_boxes = {}
        self.col_no = 0
        entry_width = 15  # Width for all entry boxes
        for i, label_text in enumerate(('ID', 'Website', 'Username', 'Password')):
            show = ""
            if i == 3:
                show = "*"
            entry_box = Entry(self.crud_frame, width=entry_width, background="lightgrey", font=('Arial', 15),
                              justify=CENTER, show=show)
            entry_box.grid(row=self.row_no, column=self.col_no, padx=2, pady=2)
            self.col_no += 1
            self.entry_boxes[label_text] = entry_box

    def save_record(self):
        website = self.entry_boxes['Website'].get()
        username = self.entry_boxes['Username'].get()
        password = self.entry_boxes['Password'].get()
    
        # Check if a record with the same website and username already exists
        existing_record = self.db.get_record_by_website_username(website, username)
    
        if existing_record:
            self.showmessage("Error", "This website and username already exists.")
        else:
            data = {'website': website, 'username': username, 'password': password}
            self.db.create_record(data)
            self.showmessage("Save", "Record is Saved")
            self.show_record()

    def update_record(self):
        ID = self.entry_boxes['ID'].get()
        website = self.entry_boxes['Website'].get()
        username = self.entry_boxes['Username'].get()
        password = self.entry_boxes['Password'].get()
        data = {'ID': ID, 'website': website, 'username': username, 'password': password}
        if ID:
            self.db.update_record(data)
            self.showmessage("Update", "Record is Updated")
        else:
            self.showmessage("Error", "Please select a record to update")
        self.show_record()

    def delete_record(self):
        ID = self.entry_boxes['ID'].get()
        if ID:
            self.db.delete_record(ID)
            self.showmessage("Delete", "Record is Deleted")
        else:
            self.showmessage("Error", "Please select a record to delete")
        self.show_record()

    def search_record(self):
        keyword = self.search_entry.get()
        if keyword:
            records = self.db.search_records(keyword)
            if records:
                self.show_record(records)
            else:
                self.showmessage("Search", "No matching records found")
        else:
            self.showmessage("Error", "Search keyword is empty")

    def show_record(self, records=None):
        for item in self.record_tree.get_children():
            self.record_tree.delete(item)
        if records is None:
            record_list = self.db.show_records()
        else:
            record_list = records
        for record in record_list:
            self.record_tree.insert('', END, values=(record[0], record[3], record[4], record[5]))

    def create_record_tree(self):
        columns = ('ID', 'Website', 'Username', 'Password')
        self.record_tree = ttk.Treeview(self.root, columns=columns, show='headings')
        self.record_tree.heading('ID', text="ID")
        self.record_tree.heading('Website', text="Website Name")
        self.record_tree.heading('Username', text="Username")
        self.record_tree.heading('Password', text="Password")
        self.record_tree['displaycolumns'] = ('Website', 'Username')

        def item_selected(event):
            for selected_item in self.record_tree.selection():
                item = self.record_tree.item(selected_item)['values']
                for entry_box, item_value in zip(self.entry_boxes.values(), item):
                    entry_box.delete(0, END)
                    entry_box.insert(0, item_value)

        self.record_tree.bind('<<TreeviewSelect>>', item_selected)
        self.record_tree.grid()

    def copy_password(self):
        password_to_copy = self.entry_boxes['Password'].get()
        if password_to_copy:
            self.root.clipboard_clear()
            self.root.clipboard_append(password_to_copy)
            self.showmessage("Copy", "Password Copied")
        else:
            self.showmessage("Error", "Box is Empty")

    def showmessage(self, title_box: str = None, message: str = None):
        root = Toplevel(self.root)
        background = 'green'
        if title_box == "Error":
            background = "red"
        root.geometry("200x50+600+300")
        root.title(title_box)
        Label(root, text=message, background=background,
              font=('Arial', 10), fg='white').pack(padx=4, pady=2)
        root.after(2000, root.destroy)  # Close the message after 2 seconds

    def generate_password(self):
        length = 10
        characters = string.ascii_letters + string.digits + string.punctuation + string.ascii_lowercase + string.ascii_uppercase + string.octdigits
        password = ''.join(random.choice(characters) for _ in range(length))
        self.generated_password_entry.delete(0, END)
        self.generated_password_entry.insert(0, password)

    def copy_generated_password(self):
        generated_password = self.generated_password_entry.get()
        if generated_password:
            self.root.clipboard_clear()
            self.root.clipboard_append(generated_password)
            self.showmessage("Copy Generated Password", "Generated Password Copied")

if __name__ == "__main__":
    db_class = DbOperation()
    db_class.create_table()

    root = Tk()
    root_class = Root_window(root, db_class)
    root.mainloop()
