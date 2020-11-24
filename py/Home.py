import ContentPage
import tkinter
import Login
import Register
import DataInsert




class Home(ContentPage.ContentPage):
    def __init__(self, data, *args, **kwargs):
        ContentPage.ContentPage.__init__(self, data, *args, **kwargs)

        self.title_frame = None
        self.content_frame = None

        self.refresh()



    def refresh(self):
        if self.title_frame is not None and self.content_frame is not None:
            self.title_frame.destroy()
            self.content_frame.destroy()

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 3)
        self.columnconfigure(0, weight = 1)

        self.title_frame = tkinter.Frame(self, bg = self["bg"])
        self.title_frame.grid(row = 0, column = 0, sticky = "NESW")

        self.title_frame.columnconfigure(0, weight = 1)

        self.content_frame = tkinter.Frame(self, bg = self["bg"])
        self.content_frame.grid(row = 1, column = 0, sticky = "NESW")


        if self.master.user is None:
            tkinter.Label(self.title_frame, text = "Üdvözöljük!", font = (None, 24), bg = self["bg"]).grid(row = 0, column = 0, sticky = "NESW")

            self.content_frame.rowconfigure(0, weight = 1)
            self.content_frame.rowconfigure(1, weight = 2)
            self.content_frame.columnconfigure(0, weight = 1)

            tkinter.Button(self.content_frame, text = "Bejelentkezés", font = (None, 12), bg = self["bg"], command = lambda: self.master.load_new_page(Login.LoginPage, None)).grid(row = 0, column = 0, sticky = "S")
            tkinter.Button(self.content_frame, text = "Regisztráció", font = (None, 12), bg = self["bg"], command = lambda: self.master.load_new_page(Register.RegisterPage, None)).grid(row = 1, column = 0, sticky = "N")

        else:
            tkinter.Label(self.title_frame, text = "Üdvözöljük, " + self.master.user.name + "!", font = (None, 24), bg = self["bg"]).grid(row = 0, column = 0, sticky = "NESW")

            tkinter.Button(self.title_frame, text = "Kijelentkezés", font = (None, 12), bg = self["bg"], command = self.logout).grid(row = 1, column = 0)

            if self.master.user.is_admin:
                self.content_frame.columnconfigure(0, weight = 1)
                self.content_frame.rowconfigure(0, weight = 1)
                self.content_frame.rowconfigure(1, weight = 1)

                tkinter.Button(self.content_frame, text = "Adatok felvitele", font = (None, 12), bg = self["bg"], command = lambda: self.master.load_new_page(DataInsert.DataInsertPage, None)).grid(row = 0, column = 0)
                tkinter.Button(self.content_frame, text = "Adatok módosítása", font = (None, 12), bg = self["bg"]).grid(row = 1, column = 0)



    def logout(self):
        self.master.user = None
        self.master.reload_existing_pages()
