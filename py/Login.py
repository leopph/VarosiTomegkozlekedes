import ContentPage
import tkinter
import tkinter.messagebox
import mysql.connector
import Entity
import Home




class LoginPage(ContentPage.ContentPage):
    def __init__(self, data, *args, **kwargs):
        ContentPage.ContentPage.__init__(self, data, *args, **kwargs)

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)

        self.title_text = tkinter.Label(self, text = "Bejelentkezés", font = (None, 24), bg = self["bg"])
        self.title_text.grid(row = 0, column = 0, columnspan = 2)

        self.username_entry = tkinter.Entry(self, bg = self["bg"])
        self.password_entry = tkinter.Entry(self, bg = self["bg"], show = "*")

        self.username_entry.grid(row = 1, column = 1, sticky = "SW")
        self.password_entry.grid(row = 2, column = 1, sticky = "NW")

        self.username_label = tkinter.Label(self, text = "Felhasználónév:", bg = self["bg"])
        self.password_label = tkinter.Label(self, text = "Jelszó:", bg = self["bg"])

        self.username_label.grid(row = 1, column = 0, sticky = "SE")
        self.password_label.grid(row = 2, column = 0, sticky = "NE")

        self.login_button = tkinter.Button(self, text = "Bejelentkezés", command = self.login, bg = self["bg"])
        self.login_button.grid(row = 3, column = 0, columnspan = 2)


    def login(self):
        if self.username_entry.get() == "" or self.password_entry == "":
            tkinter.messagebox.showwarning("Figyelem", "Kérem adja meg a felhasználónevét és jelszavát is!")

        else:
            connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
            cursor = connection.cursor()

            cursor.execute("select username, password, admin from user where username = %s", params = (self.username_entry.get(),))

            user = cursor.fetchone()

            if user is None:
                tkinter.messagebox.showerror("Hiba", "Hibás felhasználónév!")
            elif user[1] != self.password_entry.get():
                tkinter.messagebox.showerror("Hiba", "Hibás jelszó!")
            else:
                self.master.user = Entity.User(user[0], user[2])

                self.username_entry.delete(0, "end")
                self.password_entry.delete(0, "end")

                self.master.reload_existing_pages()
                self.master.load_new_page(Home.Home, None)

                tkinter.messagebox.showinfo("Siker", "Sikeres bejelentkezés!")

            connection.close()


    def refresh(self):
        pass
