import ContentPage
import tkinter
import Login
import Register
import DataInsert
import DataUpdate
import DataDelete




class Home(ContentPage.ContentPage):
    def __init__(self, data, *args, **kwargs) -> None:
        ContentPage.ContentPage.__init__(self, data, *args, **kwargs)

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)

        self.main_frame = tkinter.Frame(self, bg = self["bg"])
        self.main_frame.grid(row = 0, column = 0, sticky = "NESW")

        self.main_frame.columnconfigure(index=0, weight=1)
        self.main_frame.rowconfigure(index=0, weight=1)
        self.main_frame.rowconfigure(index=4, weight=4)

        self.refresh()


    def refresh(self) -> None:
        if self.main_frame is not None:
            for child in self.main_frame.winfo_children():
                child.destroy()

        if self.master.user is None:
            tkinter.Label(self.main_frame, text = "Üdvözöljük!", font = ("", 26), bg = self["bg"]).grid(row = 0, column = 0, sticky="S")
            tkinter.Button(self.main_frame, text = "Bejelentkezés", font = ("", 12), bg = self["bg"], command = lambda: self.master.load_new_page(Login.LoginPage, None)).grid(row = 1, column = 0)
            tkinter.Button(self.main_frame, text = "Regisztráció", font = ("", 12), bg = self["bg"], command = lambda: self.master.load_new_page(Register.RegisterPage, None)).grid(row = 2, column = 0)

        else:
            tkinter.Label(self.main_frame, text = "Üdvözöljük, " + self.master.user.name + "!", font = ("", 24), bg = self["bg"]).grid(row = 0, column = 0, sticky="S")
            tkinter.Button(self.main_frame, text = "Kijelentkezés", font = ("", 12), bg = self["bg"], command = self.logout).grid(row = 4, column = 0, sticky="N")

            if self.master.user.is_admin:
                tkinter.Button(self.main_frame, text = "Adatok felvitele", font = ("", 12), bg = self["bg"], command = lambda: self.master.load_new_page(DataInsert.DataInsertPage, None)).grid(row = 1, column = 0)
                tkinter.Button(self.main_frame, text = "Adatok módosítása", font = ("", 12), bg = self["bg"], command = lambda: self.master.load_new_page(DataUpdate.DataUpdatePage, None)).grid(row = 2, column = 0)
                tkinter.Button(self.main_frame, text = "Adatok törlése", font = ("", 12), bg = self["bg"], command = lambda: self.master.load_new_page(DataDelete.DataDeletePage, None)).grid(row = 3, column = 0)



    def logout(self):
        self.master.user = None
        self.master.reload_existing_pages()
