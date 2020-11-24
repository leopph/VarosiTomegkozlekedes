import ContentPage
import tkinter
import tkinter.messagebox
import mysql.connector
import Entity




class RegisterPage(ContentPage.ContentPage):
    def __init__(self, data, *args, **kwargs):
        ContentPage.ContentPage.__init__(self, data, *args, **kwargs)

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 1)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)

        self.title_text = tkinter.Label(self, text = "Regisztráció", font = (None, 24), bg = self["bg"])
        self.title_text.grid(row = 0, column = 0, columnspan = 2)
        
        self.username_entry = tkinter.Entry(self, bg = self["bg"])
        self.password_entry = tkinter.Entry(self, bg = self["bg"], show = "*")
        self.password_confirm_entry = tkinter.Entry(self, bg = self["bg"], show = "*")
        self.email_entry = tkinter.Entry(self, bg = self["bg"])

        self.username_entry.grid(row = 1, column = 1, sticky = "W")
        self.password_entry.grid(row = 2, column = 1, sticky = "W")
        self.password_confirm_entry.grid(row = 3, column = 1, sticky = "W")
        self.email_entry.grid(row = 4, column = 1, sticky = "W")

        self.username_label = tkinter.Label(self, text = "Felhasználónév:", bg = self["bg"])
        self.password_label = tkinter.Label(self, text = "Jelszó:", bg = self["bg"])
        self.password_confirm_label = tkinter.Label(self, text = "Jelszó még egyszer:", bg = self["bg"])
        self.email_label = tkinter.Label(self, text = "E-mail cím:", bg = self["bg"])

        self.username_label.grid(row = 1, column = 0, sticky = "E")
        self.password_label.grid(row = 2, column = 0, sticky = "E")
        self.password_confirm_label.grid(row = 3, column = 0, sticky = "E")
        self.email_label.grid(row = 4, column = 0, sticky = "E")

        self.register_button = tkinter.Button(self, text = "Regisztráció", command = self.register, bg = self["bg"])
        self.register_button.grid(row = 5, column = 0, columnspan = 2)


    def register(self):
        connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
        cursor = connection.cursor()

        cursor.execute("select * from user where username = %s", params = (self.username_entry.get(),))

        if cursor.fetchall():
            tkinter.messagebox.showerror("Hiba", "A felhasználónév már foglalt!")
        elif self.password_entry.get() != self.password_confirm_entry.get():
            tkinter.messagebox.showerror("Hiba", "A megadott jelszavak nem egyeznek!")

        else:
            cursor.execute("INSERT INTO user(username, password, email) VALUES(%s, %s, %s)", params = (self.username_entry.get(), self.password_entry.get(), self.email_entry.get()))
            connection.commit()

            self.master.user = Entity.User(self.username_entry.get(), False)

            self.username_entry.delete(0, "end")
            self.password_entry.delete(0, "end")
            self.password_confirm_entry.delete(0, "end")
            self.email_entry.delete(0, "end")

            tkinter.messagebox.showinfo("Siker", "Sikeres regisztráció!")

        connection.close()

    
    def refresh(self):
        pass
