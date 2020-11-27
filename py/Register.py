import tkinter
import tkinter.ttk
import tkinter.messagebox
import mysql.connector
import ContentPage
import Entity




class RegisterPage(ContentPage.ContentPage):
    def __init__(self, data, *args, **kwargs):
        ContentPage.ContentPage.__init__(self, data, *args, **kwargs)

        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=1)

        self.main_frame = tkinter.Frame(master=self, bg=self["bg"])
        self.main_frame.grid(row=0, column=0, sticky="NESW")

        self.main_frame.columnconfigure(index=0, weight=1)
        self.main_frame.rowconfigure(index=0, weight=1)

        self.refresh()


    def refresh(self):
        for child in self.main_frame.winfo_children():
            child.destroy()

        if self.master.user is not None:
            self.main_frame.columnconfigure(index=1, weight=0)
            self.main_frame.rowconfigure(index=5, weight=0)

            tkinter.Label(master=self.main_frame, text="Ön már be van jelentkezve, " + self.master.user.name + ".", font = ("", 26), bg=self["bg"]).grid(column=0, row=0)

        else:
            self.main_frame.columnconfigure(index=1, weight=1)
            self.main_frame.rowconfigure(index=5, weight=4)

            tkinter.Label(self.main_frame, text = "Regisztráció", font = ("", 26), bg = self["bg"]).grid(row = 0, column = 0, columnspan=2)
            
            self.username_entry = tkinter.ttk.Entry(self.main_frame)
            self.username_entry.grid(row = 1, column = 1, sticky = "W")

            self.password_entry = tkinter.ttk.Entry(self.main_frame, show = "*")
            self.password_entry.grid(row = 2, column = 1, sticky = "W")

            self.password_confirm_entry = tkinter.ttk.Entry(self.main_frame, show = "*")
            self.password_confirm_entry.grid(row = 3, column = 1, sticky = "W")

            self.email_entry = tkinter.ttk.Entry(self.main_frame)
            self.email_entry.grid(row = 4, column = 1, sticky = "W")

            tkinter.Label(self.main_frame, text = "Felhasználónév:", bg = self["bg"]).grid(row = 1, column = 0, sticky = "E")
            tkinter.Label(self.main_frame, text = "Jelszó:", bg = self["bg"]).grid(row = 2, column = 0, sticky = "E")
            tkinter.Label(self.main_frame, text = "Jelszó még egyszer:", bg = self["bg"]).grid(row = 3, column = 0, sticky = "E")
            tkinter.Label(self.main_frame, text = "E-mail cím:", bg = self["bg"]).grid(row = 4, column = 0, sticky = "E")

            tkinter.ttk.Button(self.main_frame, text = "Regisztráció", command = self.register).grid(row = 5, column = 0, columnspan = 2, sticky="N")


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
