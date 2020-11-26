import tkinter
import tkinter.messagebox
import mysql.connector
import ContentPage
from typing import Union


class DataUpdatePage(ContentPage.ContentPage):
    def __init__(self, data, *args, **kwargs) -> None:
        ContentPage.ContentPage.__init__(self, data, *args, **kwargs)

        self.title_frame: Union[tkinter.Frame, None] = None
        self.content_frame: Union[tkinter.Frame, None] = None

        self.refresh()


    def refresh(self) -> None:
        if self.title_frame is not None:
            for child in self.title_frame.winfo_children():
                child.destroy()

        if self.content_frame is not None:
            for child in self.content_frame.winfo_children():
                child.destroy()

        if self.master.user is None or not self.master.user.is_admin:
            self.title_frame = tkinter.Frame(master=self, bg=self["bg"])
            self.title_frame.grid(column=0, row=0, sticky="NESW")
            self.title_frame.columnconfigure(index=0, weight=1)
            tkinter.Label(master=self.title_frame, text="Ez az oldal csak adminisztrátorok számára érhető el!", bg=self["bg"], font=("", 26)).grid(column=0, row=0, sticky="NESW")
            

        else:
            self.rowconfigure(index=0, weight=1)
            self.rowconfigure(index=1, weight=9)
            self.columnconfigure(index=0, weight=1)

            self.title_frame = tkinter.Frame(master=self, bg=self["bg"])
            self.title_frame.grid(column=0, row=0, sticky="NESW")

            self.title_frame.columnconfigure(index=0, weight=1)

            tkinter.Label(master=self.title_frame, text="Adatok módosítása", bg=self["bg"], font=("", 26)).grid(column=0, row=0)
            tkinter.Label(master=self.title_frame, text="Válassza ki a módosítani kívánt típust!", bg=self["bg"], font=("", 20)).grid(column=0, row=1)

            self.content_frame = tkinter.Frame(master=self, bg=self["bg"])
            self.content_frame.grid(column=0, row=1,sticky="NESW")

            self.content_frame.columnconfigure(index=0, weight=1)
            self.content_frame.columnconfigure(index=1, weight=1)
            self.content_frame.columnconfigure(index=2, weight=1)
            self.content_frame.columnconfigure(index=3, weight=1)
            self.content_frame.columnconfigure(index=4, weight=1)
            self.content_frame.rowconfigure(index=1, weight=1)

            tkinter.Button(master=self.content_frame, text="Vonal módosítása", command=self.modify_line).grid(column=0, row=0)
            tkinter.Button(master=self.content_frame, text="Vezető módosítása").grid(column=1, row=0)
            tkinter.Button(master=self.content_frame, text="Járműtípus módosítása").grid(column=2, row=0)
            tkinter.Button(master=self.content_frame, text="Jármű módosítása").grid(column=3, row=0)
            tkinter.Button(master=self.content_frame, text="Járat módosítása").grid(column=4, row=0)

            self.form_frame = tkinter.Frame(self.content_frame, bg=self["bg"])
            self.form_frame.grid(column=0, row=1, columnspan=5, sticky="NESW")


    def modify_line(self):
        def send_update():
            connection = mysql.connector.connect(host=self.master.dbhost, database=self.master.dbname, user=self.master.dbuser, password=self.master.dbpwd)
            cursor =connection.cursor()
            sql = "UPDATE vonal SET nev = %s, hossz = %s WHERE nev = %s"
            
            try:
                cursor.execute(sql, (update_info[0].get(), update_info[1].get(), line_choice.get()))
                connection.commit()
                tkinter.messagebox.showinfo("Siker", "Sikeres frissítés!")

                for child in self.form_frame.winfo_children():
                    child.destroy()

            except mysql.connector.Error as error:
                connection.rollback()
                tkinter.messagebox.showerror("Hiba", "Hiba történt a módosítás során!\n" + str(error))

            finally:
                connection.close()
            

        def show_form():
            for child in self.form_frame.winfo_children():
                child.destroy()
            
            self.form_frame.columnconfigure(index=0, weight=1)
            self.form_frame.columnconfigure(index=1, weight=1)

            tkinter.Label(master=self.form_frame, text="Név:", bg=self["bg"]).grid(column=0, row=0, sticky="E")
            tkinter.Label(master=self.form_frame, text="Hossz:", bg= self["bg"]).grid(column=0, row=1, sticky="E")

            nonlocal update_info
            update_info = (tkinter.Entry(master=self.form_frame), tkinter.Entry(master=self.form_frame))
            update_info[0].grid(column=1, row=0, sticky="W")
            update_info[1].grid(column=1, row=1, sticky="W")
            update_info[0].insert(0, line_choice.get())

            connection = mysql.connector.connect(host=self.master.dbhost, database=self.master.dbname, user=self.master.dbuser, password=self.master.dbpwd)
            cursor =connection.cursor()
            sql = "SELECT hossz FROM vonal WHERE nev = %s"
            cursor.execute(sql, (line_choice.get(),))
            update_info[1].insert(0, cursor.fetchone()[0])
            connection.close()

            tkinter.Button(master=self.form_frame, text="Módosítás", command=send_update).grid(column=0, row=2, columnspan=2)
            

        for child in self.form_frame.winfo_children():
            child.destroy()

        connection = mysql.connector.connect(host=self.master.dbhost, database=self.master.dbname, user=self.master.dbuser, password=self.master.dbpwd)
        cursor = connection.cursor()
        sql = "SELECT nev FROM vonal"
        cursor.execute(sql)

        lines = [line[0] for line in cursor.fetchall()]

        line_choice = tkinter.StringVar(master=self.form_frame)
        line_choice.set(lines[0])

        self.form_frame.columnconfigure(index=0, weight=1)
        self.form_frame.columnconfigure(index=1, weight=1)

        update_info: Union[tuple[tkinter.Entry, tkinter.Entry], None] = None

        tkinter.Label(master=self.form_frame, text="Válassza ki a vonalat!", bg=self["bg"]).grid(column=0, row=0, sticky="E")
        tkinter.OptionMenu(self.form_frame, line_choice, *lines).grid(column=1, row=0, sticky="W")
        tkinter.Button(master=self.form_frame, text="Megnyitás", command=show_form).grid(column=0, row=1, columnspan=2)
        

