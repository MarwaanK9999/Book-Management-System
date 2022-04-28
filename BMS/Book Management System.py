import tkinter as tk
from tkinter import Button, Entry, Frame, Label, Listbox, Message, messagebox
from tkinter import *
from tkinter.constants import BOTTOM, END, LEFT, RIGHT, TOP
import tkinter.font as tkFont
import sqlite3
import datetime

directory = "G:/BMS/"

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(MainPage)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class MainPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        #setting title
        master.title("Main Menu")
        master.geometry("350x458")
        master.resizable(width=False, height=False)

        ft1 = tkFont.Font(family='Times', size=12)

        ft2 = tkFont.Font(family='Times', size=16)

        Message1 = Message(self, borderwidth="4px", font=ft2, fg="#333333", justify="left", text="Book Management System", width=400)
        Message1.grid(row=0, column=0, ipady=30)
        
        addBookButton = Button(self, bg="#01aaed", borderwidth="4px", font=ft1, fg="#000000", justify="center", text="Add Book", command=lambda: master.switch_frame(AddBook))
        addBookButton.grid(row=1, column=0, ipadx=128, ipady=10)

        issueBookButton = Button(self, bg="#01aaed", borderwidth="4px", font=ft1, fg="#000000", justify="center", text="Issue Book", command=lambda: master.switch_frame(IssueBook))
        issueBookButton.grid(row=2, column=0, ipadx=126, ipady=10)

        returnBookButton = Button(self, bg="#01aaed", borderwidth="4px", font=ft1, fg="#000000", justify="center", text="Return Book", command=lambda: master.switch_frame(ReturnBook))
        returnBookButton.grid(row=3, column=0, ipadx=122, ipady=10)

        viewBooksButton = Button(self, bg="#01aaed", borderwidth="4px", font=ft1, fg="#000000", justify="center", text="View Books", command=lambda: master.switch_frame(ViewBooks))
        viewBooksButton.grid(row=4, column=0, ipadx=122, ipady=10) 

        deleteBookButton = Button(self, bg="#01aaed", borderwidth="4px", font=ft1, fg="#000000", justify="center", text="Delete Book", command=lambda: master.switch_frame(DeleteBook))
        deleteBookButton.grid(row=5, column=0, ipadx=122, ipady=10)

        exitButton = Button(self, bg="#01aaed", borderwidth="4px", font=ft1, fg="#000000", justify="center", text="Exit", command=master.quit)
        exitButton.grid(row=6, column=0, ipadx=149, ipady=10)

class AddBook(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        #setting title
        master.title("Add Book")
        master.geometry("400x204")
        master.resizable(width=False, height=False)

        ft1 = tkFont.Font(family='Times', size=12)

        bookNameLabel = Label(self, borderwidth="4px", font=ft1, fg="#333333", justify="right", text="Enter Book Name:")
        bookNameLabel.grid(row = 0, column = 0, ipadx= 2, ipady= 5)

        bookNameEntry = Entry(self, bg="#ffffff", borderwidth="1px", font=ft1, fg="#333333", justify="center")
        bookNameEntry.grid(row=0, column=1, ipadx=2, ipady=5)

        bookAuthorLabel = Label(self, borderwidth="4px", font=ft1, fg="#333333", justify="right", text="Enter Book Author Name:")
        bookAuthorLabel.grid(row = 1, column = 0, ipadx= 2, ipady= 5)

        bookAuthorEntry = Entry(self, bg="#ffffff", borderwidth="1px", font=ft1, fg="#333333", justify="center")
        bookAuthorEntry.grid(row=1, column=1, ipadx=2, ipady=5)

        addBookButton = Button(self, bg="#01aaed", borderwidth="4px", font=ft1, fg="#000000", justify="center", text="Add Book", command=lambda: self.AddBook(bookNameEntry.get(), bookAuthorEntry.get()))
        addBookButton.grid(row=2, columnspan=2, ipadx=154, ipady=10)  

        mainMenuButton = Button(self, bg="#01aaed", borderwidth="4px", font=ft1, fg="#000000", justify="center", text="Main Menu", command=lambda: master.switch_frame(MainPage))
        mainMenuButton.grid(row=3, columnspan=2, ipadx=151, ipady=10)

    def AddBook(self, book_name, book_author):
        try:
            sqliteConnection = sqlite3.connect(directory + 'BookInformation.db')
            cursor = sqliteConnection.cursor()

            sqlite_insert_with_param = """INSERT INTO Books_In_Stock
                                (book_name, author_name) 
                                VALUES (?, ?);"""

            data_tuple = (book_name, book_author)
            cursor.execute(sqlite_insert_with_param, data_tuple)
            sqliteConnection.commit()
            messagebox.showinfo(title="Success", message="Book added successfully.")

            cursor.close()

        except sqlite3.Error as error:
            messagebox.showerror(title="Error", message="Failed to insert data. \n" + error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()

class IssueBook(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        #setting title
        master.title("Issue Book")
        master.geometry("400x454")
        master.resizable(width=False, height=False)

        global Message1
        global menuText
        global bookID
        global clientName

        ft1 = tkFont.Font(family='Times', size=12)
        
        availableBooksLabel = Label(self, borderwidth="4px", font=ft1, fg="#333333", justify="right", text="Select Available Book:")
        availableBooksLabel.grid(row = 0, column = 0, ipadx= 2, ipady= 5)

        self.PopulateAvailableBooks()

        menuText= StringVar()
        menuText.set("Select A Book ID")

        menu = OptionMenu(self, menuText, *(bookID))
        menu.grid(row=0, column=1, ipadx=10)

        Message1 = Message(self, borderwidth="4px", font=ft1, fg="#333333", justify="left", text="Select A Book ID and click \n'Show Book' the button to \nview book details.", width= 350)
        Message1.grid(row=1, columnspan=2, ipady=60)

        clientNameLabel = Label(self, borderwidth="4px", font=ft1, fg="#333333", justify="right", text="Enter Client Name:")
        clientNameLabel.grid(row = 2, column = 0, ipadx= 2, ipady= 5)

        clientName = Entry(self, bg="#ffffff", borderwidth="1px", font=ft1, fg="#333333", justify="center")
        clientName.grid(row=2, column=1, ipadx=2, ipady=5)

        showBookButton = Button(self, bg="#01aaed", borderwidth="4px", font=ft1, fg="#000000",justify="center", text="Show Book Details", command=lambda: self.ChangeLabelContents(int(menuText.get())))
        showBookButton.grid(row=3, columnspan=2, ipadx=128, ipady=10)

        issueBookButton = Button(self, bg="#01aaed", borderwidth="4px", font=ft1, fg="#000000",justify="center", text="Issue Book", command=lambda: self.IssueBook(int(menuText.get())))
        issueBookButton.grid(row=4, columnspan=2, ipadx=153, ipady=10)

        mainMenubutton = Button(self, bg="#01aaed", borderwidth="4px", font=ft1, fg="#000000", justify="center", text="Main Menu", command=lambda: master.switch_frame(MainPage))
        mainMenubutton.grid(row=5, columnspan=2, ipadx=152, ipady=10)

    def PopulateAvailableBooks(self):
        global menuText
        global bookID
        try:
            sqliteConnection = sqlite3.connect(directory + "BookInformation.db")
            cursor = sqliteConnection.cursor()

            bookID = []

            sqlite_select_query = """SELECT * from Books_In_Stock"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            for row in records:
                bookID.append(row[0])

            cursor.close()

        except sqlite3.Error as error:
            messagebox.showerror(title="Error", message="There are no books in stock. \n" + error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()

    def ChangeLabelContents(self, id):
        global Message1
        try:
            sqliteConnection = sqlite3.connect(directory + "BookInformation.db")
            cursor = sqliteConnection.cursor()

            sqlite_select_query = """SELECT * from Books_In_Stock where book_id = ?"""
            cursor.execute(sqlite_select_query, (id,))
            record = cursor.fetchone()
            labeltext = "Book ID: " + str(record[0]) + "\n" + "Book Name: " + str(
                record[1]) + "\n" + "Author Name: " + str(record[2])
            Message1.config(text=labeltext)
            cursor.close()

        except sqlite3.Error as error:
            messagebox.showerror(title="Error", message="Failed to read data. \n" + error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()

    def IssueBook(self, id):
        global clientName
        try:
            sqliteConnection = sqlite3.connect(directory + "BookInformation.db")
            cursor = sqliteConnection.cursor()

            sqlite_select_query = """SELECT * from Books_In_Stock where book_id = ?"""
            cursor.execute(sqlite_select_query, (id,))
            record = cursor.fetchone()
            book_id = record[0]
            book_name = record[1]
            author_name = record[2]
            cursor.close()

            sqliteConnection = sqlite3.connect(directory + "BookInformation.db")
            cursor = sqliteConnection.cursor()

            sql_update_query = """DELETE from Books_In_Stock where book_id = ?"""
            cursor.execute(sql_update_query, (id,))
            sqliteConnection.commit()
            cursor.close()

            issued_client = str(clientName.get())

            issue_date = datetime.date.today()

            self.Insert_Issued_Book(book_id, book_name, author_name, str(issued_client), issue_date)
            
        except sqlite3.Error as error:
            messagebox.showerror(title="Error", message="Failed to read data, \n" + error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()

    def Insert_Issued_Book(self, book_id, book_name, book_author, client, date):
        try:
            sqliteConnection = sqlite3.connect(directory + 'BookInformation.db')
            cursor = sqliteConnection.cursor()

            sqlite_insert_with_param = """INSERT INTO Books_Issued_Out
                                (book_id, book_name, author_name, issued_to, date_issued) 
                                VALUES (?, ?, ?, ?, ?);"""

            data_tuple = (book_id, book_name, book_author, client, date)
            cursor.execute(sqlite_insert_with_param, data_tuple)
            sqliteConnection.commit()
            messagebox.showinfo(title="Success", message="Book issued successfully.")
            self.PopulateAvailableBooks()
            menuText = StringVar()
            menuText.set("Select A Book ID")

            menu = OptionMenu(self, menuText, *(bookID))
            menu.grid(row=0, column=1, ipadx=10)
            cursor.close()

        except sqlite3.Error as error:
            messagebox.showerror(title="Error", message="Failed to read data. \n" + error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()

class ReturnBook(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        #setting title
        master.title("Return Book")
        master.geometry("400x415")
        master.resizable(width=False, height=False)

        global Message1
        global menuText
        global bookID

        ft1 = tkFont.Font(family='Times', size=12)

        availableBooksLabel = Label(self, borderwidth="4px", font=ft1,
                                    fg="#333333", justify="right", text="Select Available Book:")
        availableBooksLabel.grid(row=0, column=0, ipadx=2, ipady=5)

        self.PopulateAvailableBooks()

        menuText= StringVar()
        menuText.set("Select Any Language")

        menu = OptionMenu(self, menuText, *(bookID))
        menu.grid(row=0, column=1, ipadx=10)

        Message1 = Message(self, borderwidth="4px", font=ft1, fg="#333333", justify="left",
                           text="Select A Book ID and click \n'Show Book' the button to \nview book details.", width=350)
        Message1.grid(row=1, columnspan=2, ipady=60)

        showBookButton = Button(self, bg="#01aaed", borderwidth="4px", font=ft1, fg="#000000",
                                  justify="center", text="Show Book Details", command=lambda: self.ChangeLabelContents(int(menuText.get())))
        showBookButton.grid(row=2, columnspan=2, ipadx=129, ipady= 10)

        returnBookButton = Button(self, bg="#01aaed", borderwidth="4px", font=ft1, fg="#000000", justify="center", text="Return Book", command=lambda: self.ReturnBook(int(menuText.get())))
        returnBookButton.grid(row=3, columnspan=2, ipadx=148, ipady= 10)  

        mainMenuButton = Button(self, bg="#01aaed", borderwidth="4px", font=ft1, fg="#000000", justify="center", text="Main Menu", command=lambda: master.switch_frame(MainPage))
        mainMenuButton.grid(row=4, columnspan=2, ipadx=152, ipady= 10)

    def PopulateAvailableBooks(self):
        global menuText
        global bookID
        try:
            sqliteConnection = sqlite3.connect(directory + "BookInformation.db")
            cursor = sqliteConnection.cursor()

            bookID = []

            sqlite_select_query = """SELECT * from Books_Issued_Out"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            for row in records:
                bookID.append(row[0])

            cursor.close()

        except sqlite3.Error as error:
            messagebox.showerror(title="Error", message="There are no books to return. \n" + error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()

    def ChangeLabelContents(self, id):
        global Message1
        try:
            sqliteConnection = sqlite3.connect(directory + "BookInformation.db")
            cursor = sqliteConnection.cursor()

            sqlite_select_query = """SELECT * from Books_Issued_Out where book_id = ?"""
            cursor.execute(sqlite_select_query, (id,))
            record = cursor.fetchone()
            labeltext = "Book ID: " + str(record[0]) + "\n" + "Book Name: " + str(
                record[1]) + "\n" + "Author Name: " + str(record[2])
            Message1.config(text=labeltext)
            cursor.close()

        except sqlite3.Error as error:
            messagebox.showerror(title="Error", message="Failed to read data. \n" + error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()

    def ReturnBook(self, id):
        global clientName
        try:
            sqliteConnection = sqlite3.connect(directory + "BookInformation.db")
            cursor = sqliteConnection.cursor()

            sqlite_select_query = """SELECT * from Books_Issued_Out where book_id = ?"""
            cursor.execute(sqlite_select_query, (id,))
            record = cursor.fetchone()
            book_id = record[0]
            book_name = record[1]
            author_name = record[2]
            issued_client = record[3]
            issued_date = record[4]
            cursor.close()

            sqliteConnection = sqlite3.connect(directory + "BookInformation.db")
            cursor = sqliteConnection.cursor()

            sql_update_query = """DELETE from Books_Issued_Out where book_id = ?"""
            cursor.execute(sql_update_query, (id,))
            sqliteConnection.commit()
            cursor.close()

            return_date = datetime.date.today()

            self.Insert_Issued_Book(
                book_id, book_name, author_name, issued_date, return_date, issued_client)

        except sqlite3.Error as error:
            messagebox.showerror(title="Error", message="Failed to read data. \n" + error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()

    def Insert_Issued_Book(self, book_id, book_name, book_author, last_issue_date, last_return_date, client):
        try:
            sqliteConnection = sqlite3.connect(directory + 'BookInformation.db')
            cursor = sqliteConnection.cursor()

            sqlite_insert_with_param = """INSERT INTO Books_In_Stock
                                (book_id, book_name, author_name, last_issue_date, last_return_date, last_issued_to) 
                                VALUES (?, ?, ?, ?, ?, ?);"""

            data_tuple = (book_id, book_name, book_author,
                          last_issue_date, last_return_date, client)
            cursor.execute(sqlite_insert_with_param, data_tuple)
            sqliteConnection.commit()
            messagebox.showinfo(title="Success", message="Book returned successfully.")
            self.PopulateAvailableBooks()
            menuText = StringVar()
            menuText.set("Select A Book ID")

            menu = OptionMenu(self, menuText, *(bookID))
            menu.grid(row=0, column=1, ipadx=10)
            cursor.close()

            cursor.close()

        except sqlite3.Error as error:
            messagebox.showerror(title="Error", message="Failed to read data. \n" + error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()

class ViewBooks(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        #setting title
        master.title("View Books")
        master.geometry("600x666")
        master.resizable(width=False, height=False)

        global viewDetails
        global menuText
        global bookID

        ft1 = tkFont.Font(family='Times', size=12)

        availableBooksLabel = Label(self, borderwidth="4px", font=ft1, fg="#333333", justify="right", text="Select Available Book:")
        availableBooksLabel.grid(row = 0, column = 0, ipadx= 2, ipady= 5)

        self.PopulateAvailableBooks()

        menuText = StringVar()
        menuText.set("Select Book ID")

        menu = OptionMenu(self, menuText, *(bookID))
        menu.grid(row=0, column=1, ipadx=10)

        viewDetails = Listbox(self, font=ft1, justify="left")
        viewDetails.grid(row=1, columnspan=2, pady=10, ipadx=150, ipady=110)

        viewDetails.delete(0, END)

        viewButton = Button(self, bg="#01aaed", borderwidth="4px", font=ft1, fg="#000000",justify="center", text="View Book", command=lambda: self.ViewSingleBook(int(menuText.get())))
        viewButton.grid(row=2, columnspan=2, ipadx=253, ipady=10)

        viewAllButton = Button(self, bg="#01aaed", borderwidth="4px", font=ft1, fg="#000000", justify="center", text="View All Books", command=lambda: self.ViewAllBooks())
        viewAllButton.grid(row=3, columnspan=2, ipadx=239, ipady=10)

        mainMenuButton = Button(self, bg="#01aaed", borderwidth="4px", font=ft1, fg="#000000", justify="center", text="Main Menu", command=lambda: master.switch_frame(MainPage))
        mainMenuButton.grid(row=4, columnspan=2, ipadx=252, ipady=10)

    def PopulateAvailableBooks(self):
        global menuText
        global bookID
        try:
            sqliteConnection = sqlite3.connect(directory + "BookInformation.db")
            cursor = sqliteConnection.cursor()

            bookID = []

            sqlite_select_query = """SELECT * from Books_In_Stock"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            for row in records:
                bookID.append(row[0])

            cursor.close()

        except sqlite3.Error as error:
            messagebox.showerror(title="Error", message="Failed to read data. \n" + str(error))
            print(error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()

    def ViewSingleBook(self, id):
        global viewDetails
        viewDetails.delete(0, END)
        try:
            sqliteConnection = sqlite3.connect(directory + "BookInformation.db")
            cursor = sqliteConnection.cursor()

            sqlite_select_query = """SELECT * from Books_In_Stock where book_id = ?"""
            cursor.execute(sqlite_select_query, (id,))
            record = cursor.fetchone()
            viewDetails.insert(END, "Book Details:")
            viewDetails.insert(END, " ")
            viewDetails.insert(END, "Book ID: " + str(record[0]))
            viewDetails.insert(END, "Book Name: " + str(record[1]))
            viewDetails.insert(END, "Book Author: " + str(record[2]))
            viewDetails.insert(END, "Last Issue Date: " + str(record[3]))
            viewDetails.insert(END, "Last Return Date: " + str(record[4]))
            viewDetails.insert(END, "Last Issued To: " + str(record[5]))
            cursor.close()

        except sqlite3.Error as error:
            messagebox.showerror(title="Error", message="Failed to read data. \n" + str(error))
        finally:
            if sqliteConnection:
                sqliteConnection.close()

    def ViewAllBooks(self):
        global viewDetails
        viewDetails.delete(0, END)
        try:
            sqliteConnection = sqlite3.connect(directory + "BookInformation.db")
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")

            sqlite_select_query = """SELECT * from Books_In_Stock"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            viewDetails.insert(END, "Book Details:")
            viewDetails.insert(END, " ")
            for row in records:
                viewDetails.insert(END, "Book ID: " + str(row[0]))
                viewDetails.insert(END, "Book Name: " + str(row[1]))
                viewDetails.insert(END, "Book Author: " + str(row[2]))
                viewDetails.insert(END, "Last Issue Date: " + str(row[3]))
                viewDetails.insert(END, "Last Return Date: " + str(row[4]))
                viewDetails.insert(END, "Last Issued To: " + str(row[5]))
                viewDetails.insert(END, " ")
            cursor.close()

        except sqlite3.Error as error:
            messagebox.showerror(title="Error", message="Failed to read data. \n" + error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()

class DeleteBook(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        #setting title
        master.title("Delete Book")
        master.geometry("400x415")
        master.resizable(width=False, height=False)

        global Message1
        global menuText
        global bookID

        ft1 = tkFont.Font(family='Times', size=12)

        availableBooksLabel = Label(self, borderwidth="4px", font=ft1,
                                    fg="#333333", justify="right", text="Select Available Book:")
        availableBooksLabel.grid(row=0, column=0, ipadx=2, ipady=5)

        self.PopulateAvailableBooks()

        menuText = StringVar()
        menuText.set("Select Book ID")

        menu = OptionMenu(self, menuText, *(bookID))
        menu.grid(row=0, column=1, ipadx=10)
        
        Message1 = Message(self, borderwidth="4px", font=ft1, fg="#333333", justify="left", text="Select A Book ID and click \n'Show Book' the button to \nview book details.", width=350)
        Message1.grid(row=1, columnspan=2, ipady=60)
        
        showBookButton = Button(self, bg="#01aaed", borderwidth="4px", font=ft1, fg="#000000", justify="center", text="Show Book Details", command=lambda: self.ChangeLabelContents(int(menuText.get())))
        showBookButton.grid(row=2, columnspan=2, ipadx=129, ipady=10)

        deleteBookButton = Button(self, bg="#01aaed", borderwidth="4px", font=ft1, fg="#000000", justify="center", text="Delete Book", command=lambda: self.DeleteBooks(int(menuText.get())))
        deleteBookButton.grid(row=3, columnspan=2, ipadx=149, ipady=10)

        mainMenuButton = Button(self, bg="#01aaed", borderwidth="4px", font=ft1, fg="#000000", justify="center", text="Main Menu", command=lambda: master.switch_frame(MainPage))
        mainMenuButton.grid(row=4, columnspan=2, ipadx=152, ipady=10)

    def PopulateAvailableBooks(self):
        global menuText
        global bookID
        try:
            sqliteConnection = sqlite3.connect(directory + "BookInformation.db")
            cursor = sqliteConnection.cursor()
            bookID = []

            sqlite_select_query = """SELECT * from Books_In_Stock"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            for row in records:
                bookID.append(row[0])

            cursor.close()
            
        except sqlite3.Error as error:
            messagebox.showerror(title="Error", message="Failed to read data. \n" + error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()

    def ChangeLabelContents(self, id):
        global Message1
        try:
            sqliteConnection = sqlite3.connect(directory + "BookInformation.db")
            cursor = sqliteConnection.cursor()
            sqlite_select_query = """SELECT * from Books_In_Stock where book_id = ?"""
            cursor.execute(sqlite_select_query, (id,))
            record = cursor.fetchone()
            labeltext = "Book ID: " + str(record[0]) + "\n" + "Book Name: " + str(record[1]) + "\n" + "Author Name: " + str(record[2])
            Message1.config(text=labeltext)
            cursor.close()

        except sqlite3.Error as error:
            messagebox.showerror(title="Error", message="Failed to read data. \n" + error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()

    def DeleteBooks(self, id):
        try:
            sqliteConnection = sqlite3.connect(directory + "BookInformation.db")
            cursor = sqliteConnection.cursor()

            sql_update_query = """DELETE from Books_In_Stock where book_id = ?"""
            cursor.execute(sql_update_query, (id,))
            sqliteConnection.commit()
            messagebox.showinfo(title="Success", message="Book deleted successfully.")
            self.PopulateAvailableBooks()
            menuText = StringVar()
            menuText.set("Select A Book ID")

            menu = OptionMenu(self, menuText, *(bookID))
            menu.grid(row=0, column=1, ipadx=10)
            cursor.close()

        except sqlite3.Error as error:
            messagebox.showerror(title="Error", message="Failed to read data. \n" + error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
