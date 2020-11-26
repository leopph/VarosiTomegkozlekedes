import tkinter
import tkinter.messagebox
import mysql.connector
import ContentPage
import Home
import Entity




class LoginPage(ContentPage.ContentPage):
    def __init__(self, data, *args, **kwargs) -> None:
        ContentPage.ContentPage.__init__(self, data, *args, **kwargs)

        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=1)

        self.main_frame = tkinter.Frame(master=self, bg=self["bg"])
        self.main_frame.grid(column=0, row=0, sticky="NESW")

        self.main_frame.columnconfigure(index=0, weight=1)
        self.main_frame.rowconfigure(index=0, weight=1)

        self.refresh()


    def refresh(self) -> None:
        for child in self.main_frame.winfo_children():
            child.destroy()

        if self.master.user is not None:

            self.main_frame.columnconfigure(index=1, weight=0)
            self.main_frame.rowconfigure(index=3, weight=0)

            tkinter.Label(master=self.main_frame, text="Ön már be van jelentkezve, " + self.master.user.name + ".", font = ("", 26), bg=self["bg"]).grid(column=0, row=0)

        else:
            self.main_frame.columnconfigure(1, weight = 1)
            self.main_frame.rowconfigure(index=3, weight=4)

            tkinter.Label(self.main_frame, text = "Bejelentkezés", font = ("", 26), bg = self["bg"]).grid(row = 0, column = 0, columnspan = 2)

            self.username_entry = tkinter.Entry(self.main_frame, bg = self["bg"])
            self.username_entry.grid(row = 1, column = 1, sticky = "SW")

            self.password_entry = tkinter.Entry(self.main_frame, bg = self["bg"], show = "*")
            self.password_entry.grid(row = 2, column = 1, sticky = "NW")

            tkinter.Label(self.main_frame, text = "Felhasználónév:", bg = self["bg"]).grid(row = 1, column = 0, sticky = "SE")
            tkinter.Label(self.main_frame, text = "Jelszó:", bg = self["bg"]).grid(row = 2, column = 0, sticky = "NE")

            tkinter.Button(self.main_frame, text = "Bejelentkezés", command = self.login, bg = self["bg"]).grid(row = 3, column = 0, columnspan = 2, sticky="N")


    def login(self) -> None:
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

            connection.close()
