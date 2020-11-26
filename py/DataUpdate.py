import tkinter
import tkinter.messagebox
import mysql.connector
from mysql.connector.dbapi import Date
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
            tkinter.Label(master=self.title_frame, text="Válassza ki a módosítani kívánt típust!", bg=self["bg"], font=("", 22)).grid(column=0, row=1)

            self.content_frame = tkinter.Frame(master=self, bg=self["bg"])
            self.content_frame.grid(column=0, row=1,sticky="NESW")

            self.content_frame.columnconfigure(index=0, weight=1)
            self.content_frame.columnconfigure(index=5, weight=1)
            self.content_frame.rowconfigure(index=1, weight=1)

            tkinter.Button(master=self.content_frame, text="Vonal módosítása", command=self.modify_line).grid(column=0, row=0, sticky="E")
            tkinter.Button(master=self.content_frame, text="Megálló módosítása", command=self.modify_stop).grid(column=1, row=0)
            tkinter.Button(master=self.content_frame, text="Vezető módosítása", command=self.modify_driver).grid(column=2, row=0)
            tkinter.Button(master=self.content_frame, text="Járműtípus módosítása", command=self.modify_type).grid(column=3, row=0)
            tkinter.Button(master=self.content_frame, text="Jármű módosítása", command=self.modify_vehicle).grid(column=4, row=0)
            tkinter.Button(master=self.content_frame, text="Járat módosítása", command=self.modify_route).grid(column=5, row=0, sticky="W")

            self.form_frame = tkinter.Frame(self.content_frame, bg=self["bg"])
            self.form_frame.grid(column=0, row=1, columnspan=6, sticky="NESW")


    def modify_route(self) -> None:
        pass


    def modify_stop(self) -> None:
        def send_update() -> None:
            connection = mysql.connector.connect(host=self.master.dbhost, database=self.master.dbname, user=self.master.dbuser, password=self.master.dbpwd)
            cursor = connection.cursor()
            sql = "UPDATE megallo SET nev = %s, hely = %s WHERE id = %s"
            
            try:
                cursor.execute(sql, (update_info[0].get(), update_info[1].get(), stops[stop_selection.get()]))
                connection.commit()

                tkinter.messagebox.showinfo("Siker", "Sikeres frissítés!")

                for child in self.form_frame.winfo_children():
                    child.destroy()

            except mysql.connector.Error as error:
                connection.rollback()
                tkinter.messagebox.showerror("Hiba", "Hiba történt a módosítás során!\n" + str(error))

            finally:
                connection.close()


        def show_form() -> None:
            for child in self.form_frame.winfo_children():
                child.destroy()

            self.form_frame.columnconfigure(index=0, weight=1)
            self.form_frame.columnconfigure(index=1, weight=1)

            connection = mysql.connector.connect(host=self.master.dbhost, database=self.master.dbname, user=self.master.dbuser, password=self.master.dbpwd)
            cursor = connection.cursor()
            sql = "SELECT nev, hely FROM megallo WHERE id = %s"
            cursor.execute(sql, (stop_selection.get(),))
            query_result: tuple[str, str] = cursor.fetchone()
            connection.close()

            nonlocal update_info
            update_info = (tkinter.Entry(master=self.form_frame), tkinter.Entry(master=self.form_frame))
            update_info[0].grid(row=0, column=1, sticky="W")
            update_info[0].insert(0, query_result[0])
            update_info[1].grid(row=1, column=1, sticky="W")
            update_info[1].insert(0, query_result[1])

            

            tkinter.Label(master=self.form_frame, text="Név:", bg=self["bg"]).grid(column=0, row=0, sticky="E")
            tkinter.Label(master=self.form_frame, text="Hely:", bg=self["bg"]).grid(column=0, row=1, sticky="E")
            tkinter.Button(master=self.form_frame, text="Módosítás", command=send_update).grid(column=0, row=2, columnspan=2)

        
        for child in self.form_frame.winfo_children():
            child.destroy()

        self.form_frame.columnconfigure(index=0, weight=1)
        self.form_frame.columnconfigure(index=1, weight=1)

        connection = mysql.connector.connect(host=self.master.dbhost, database=self.master.dbname, user=self.master.dbuser, password=self.master.dbpwd)
        cursor = connection.cursor()
        sql = "SELECT id, nev FROM megallo"
        cursor.execute(sql)

        stops: dict[str, int] = {str(stop[0]) + " (" + str(stop[1]) + ")": stop[0] for stop in cursor.fetchall()}

        stop_selection = tkinter.StringVar(master=self.form_frame)
        stop_selection.set(sorted(stops.keys())[0])

        update_info: Union[tuple[tkinter.Entry, tkinter.Entry], None] = None

        tkinter.Label(master=self.form_frame, text="Válasszon megállót!", bg=self["bg"]).grid(column=0, row=0, sticky="E")
        tkinter.OptionMenu(self.form_frame, stop_selection, *stops).grid(column=1, row=0, sticky="W")
        tkinter.Button(master=self.form_frame, text="Kiválasztás", command=show_form).grid(column=0, row=1, columnspan=2)


    def modify_vehicle(self) -> None:
        def send_update() -> None:
            connection = mysql.connector.connect(host=self.master.dbhost, database=self.master.dbname, user=self.master.dbuser, password=self.master.dbpwd)
            cursor = connection.cursor()
            sql = "UPDATE jarmu SET rendszam = %s, alacsony_padlos =%s, tipus_nev = %s, vezetoi_szam = %s WHERE rendszam = %s"

            try:
                cursor.execute(sql, (update_info[0].get(), update_info[1].get(), update_info[2].get(), update_info[3].get(), license_selection.get()))
                connection.commit()

                tkinter.messagebox.showinfo("Siker", "Sikeres frissítés!")

                for child in self.form_frame.winfo_children():
                    child.destroy()

            except mysql.connector.Error as error:
                connection.rollback()
                tkinter.messagebox.showerror("Hiba", "Hiba történt a módosítás során!\n" + str(error))

            finally:
                connection.close()


        def show_form() -> None:
            for child in self.form_frame.winfo_children():
                child.destroy()

            self.form_frame.columnconfigure(index=0, weight=1)
            self.form_frame.columnconfigure(index=1, weight=1)

            nonlocal update_info
            update_info = (tkinter.Entry(master=self.form_frame), tkinter.BooleanVar(master=self.form_frame), tkinter.StringVar(master=self.form_frame), tkinter.StringVar(master=self.form_frame))
            update_info[0].grid(column=1, row=0, sticky="W")
            update_info[0].insert(0, license_selection.get())

            connection = mysql.connector.connect(host=self.master.dbhost, database=self.master.dbname, user=self.master.dbuser, password=self.master.dbpwd)
            cursor = connection.cursor()
            sql = "SELECT alacsony_padlos, tipus_nev, vezetoi_szam FROM jarmu WHERE rendszam = %s"
            cursor.execute(sql, (license_selection.get(),))
            query_result: tuple[bool, str, str] = cursor.fetchone()

            for i in range(1, 4):
                update_info[i].set(query_result[i-1])


            sql = "SELECT vezetoi_szam FROM vezeto"
            cursor.execute(sql)
            drivers: list[str] = [driver[0] for driver in cursor.fetchall()]

            sql = "SELECT nev FROM jarmutipus"
            cursor.execute(sql)
            types: list[str] = [type_[0] for type_ in cursor.fetchall()]

            connection.close()

            tkinter.OptionMenu(self.form_frame, update_info[1], *[True, False]).grid(column=1, row=1, sticky="W")
            tkinter.OptionMenu(self.form_frame, update_info[2], *types).grid(column=1, row=2, sticky="W")
            tkinter.OptionMenu(self.form_frame, update_info[3], *drivers).grid(column=1, row=3, sticky="W")

            tkinter.Label(master=self.form_frame, text="Rendszám:", bg=self["bg"]).grid(column=0, row=0, sticky="E")
            tkinter.Label(master=self.form_frame, text="Alacsony padlós-e:", bg=self["bg"]).grid(column=0, row=1, sticky="E")
            tkinter.Label(master=self.form_frame, text="Típus:", bg=self["bg"]).grid(column=0, row=2, sticky="E")
            tkinter.Label(master=self.form_frame, text="Vezető száma:", bg=self["bg"]).grid(column=0, row=3, sticky="E")

            tkinter.Button(master=self.form_frame, text="Módosítás", command=send_update).grid(column=0, row=4, columnspan=2)




        for child in self.form_frame.winfo_children():
            child.destroy()

        self.form_frame.columnconfigure(index=0, weight = 1)
        self.form_frame.columnconfigure(index=1, weight = 1)

        connection = mysql.connector.connect(host=self.master.dbhost, database=self.master.dbname, user=self.master.dbuser, password=self.master.dbpwd)
        cursor = connection.cursor()
        sql = "SELECT rendszam FROM jarmu"
        cursor.execute(sql)

        licenses: list[str] = [license[0] for license in cursor.fetchall()]

        license_selection = tkinter.StringVar(master=self.form_frame)
        license_selection.set(licenses[0])

        update_info: Union[tuple[tkinter.Entry, tkinter.BooleanVar, tkinter.StringVar, tkinter.StringVar], None] = None

        tkinter.Label(master=self.form_frame, text="Rendszám:", bg=self["bg"]).grid(column=0, row=0, sticky="E")
        tkinter.OptionMenu(self.form_frame, license_selection, *licenses).grid(column=1, row=0, sticky="W")
        tkinter.Button(master=self.form_frame, text="Kiválasztás", command=show_form).grid(column=0, row=1, columnspan=2)


    def modify_type(self) -> None:
        def send_update() -> None:
            connection = mysql.connector.connect(host=self.master.dbhost, database=self.master.dbname, user=self.master.dbuser, password=self.master.dbpwd)
            cursor = connection.cursor()
            sql = "UPDATE jarmutipus SET nev = %s, elektromos = %s WHERE nev = %s"

            try:
                cursor.execute(sql, (update_info[0].get(), update_info[1].get(), type_choice.get()))
                connection.commit()

                tkinter.messagebox.showinfo("Siker", "Sikeres frissítés!")

                for child in self.form_frame.winfo_children():
                    child.destroy()

            except mysql.connector.Error as error:
                connection.rollback()
                tkinter.messagebox.showerror("Hiba", "Hiba történt a módosítás során!\n" + str(error))

            finally:
                connection.close()

        
        def show_form() -> None:
            for child in self.form_frame.winfo_children():
                child.destroy()

            self.form_frame.columnconfigure(index=0, weight=1)
            self.form_frame.columnconfigure(index=1, weight=1)

            nonlocal update_info
            update_info = (tkinter.Entry(master=self.form_frame), tkinter.BooleanVar(master=self.form_frame))
            update_info[0].grid(column=1, row=0, sticky="W")
            update_info[0].insert(0, type_choice.get())
            
            connection = mysql.connector.connect(host=self.master.dbhost, database=self.master.dbname, user=self.master.dbuser, password=self.master.dbpwd)
            cursor = connection.cursor()
            sql = "SELECT elektromos FROM jarmutipus WHERE nev = %s"
            cursor.execute(sql, (type_choice.get(),))

            update_info[1].set(cursor.fetchone()[0])
            tkinter.OptionMenu(self.form_frame, update_info[1], *[True, False]).grid(column=1, row=1, sticky="W")

            tkinter.Label(master=self.form_frame, text="Típus neve:", bg=self["bg"]).grid(column=0, row=0, sticky="E")
            tkinter.Label(master=self.form_frame, text="Elektromos-e:", bg=self["bg"]).grid(column=0, row=1, sticky="E")
            tkinter.Button(master=self.form_frame, text="Módosítás", command=send_update).grid(column=0, row=2, columnspan=2)
            

            


        for child in self.form_frame.winfo_children():
            child.destroy()

        
        connection = mysql.connector.connect(host=self.master.dbhost, database=self.master.dbname, user=self.master.dbuser, password=self.master.dbpwd)
        cursor = connection.cursor()
        sql = "SELECT nev FROM jarmutipus"
        cursor.execute(sql)

        types: list[str] = [type_[0] for type_ in cursor.fetchall()]

        type_choice = tkinter.StringVar(master=self.form_frame)
        type_choice.set(types[0])

        self.form_frame.columnconfigure(index=0, weight=1)
        self.form_frame.columnconfigure(index=1, weight=1)

        update_info: Union[tuple[tkinter.Entry, tkinter.BooleanVar], None] = None

        tkinter.OptionMenu(self.form_frame, type_choice, *types).grid(column=1, row=0, sticky="W")
        tkinter.Label(master=self.form_frame, text="Válasson típus!", bg=self["bg"]).grid(column=0, row=0, sticky="E")
        tkinter.Button(master=self.form_frame, text="Kiválasztás", command=show_form).grid(column=0, row=1, columnspan=2)

        
    def modify_driver(self) -> None:
        def send_update() -> None:
            connection = mysql.connector.connect(host=self.master.dbhost, database=self.master.dbname, user=self.master.dbuser, password=self.master.dbpwd)
            cursor = connection.cursor()
            sql = "UPDATE vezeto SET vezetoi_szam = %s, vezeteknev = %s, keresztnev = %s, szul_datum = %s WHERE vezetoi_szam = %s"

            try:
                cursor.execute(sql, (update_info[0].get(), update_info[1].get(), update_info[2].get(), update_info[3].get(), drivers[driver_choice.get()]))
                connection.commit()

                tkinter.messagebox.showinfo("Siker", "Sikeres módosítás!")

                for child in self.form_frame.winfo_children():
                    child.destroy()

            except mysql.connector.Error as error:
                connection.rollback()
                tkinter.messagebox.showerror("Hiba", "Hiba történt a módosítás során!\n" + str(error))

            finally:
                connection.close()

        
        def show_form() -> None:
            for child in self.form_frame.winfo_children():
                child.destroy()

            self.form_frame.columnconfigure(index=0, weight=1)
            self.form_frame.columnconfigure(index=1, weight=1)

            tkinter.Label(master=self.form_frame, text="Vezetői szám:", bg=self["bg"]).grid(column=0, row=0, sticky="E")
            tkinter.Label(master=self.form_frame, text="Vezetéknév:", bg=self["bg"]).grid(column=0, row=1, sticky="E")
            tkinter.Label(master=self.form_frame, text="Keresztnév:", bg=self["bg"]).grid(column=0, row=2, sticky="E")
            tkinter.Label(master=self.form_frame, text="Születési dátum:", bg=self["bg"]).grid(column=0, row=3, sticky="E")

            nonlocal update_info
            update_info = (tkinter.Entry(master=self.form_frame), tkinter.Entry(master=self.form_frame), tkinter.Entry(master=self.form_frame), tkinter.Entry(self.form_frame))
            update_info[0].grid(column=1, row=0, sticky="W")
            update_info[1].grid(column=1, row=1, sticky="W")
            update_info[2].grid(column=1, row=2, sticky="W")
            update_info[3].grid(column=1, row=3, sticky="W")
            update_info[0].insert(0, drivers[driver_choice.get()])

            connection = mysql.connector.connect(host=self.master.dbhost, database=self.master.dbname, user=self.master.dbuser, password=self.master.dbpwd)
            cursor = connection.cursor()
            cursor.execute("SELECT vezeteknev, keresztnev, szul_datum FROM vezeto WHERE vezetoi_szam = %s", (drivers[driver_choice.get()],))
            query_result: tuple[str, str, Date] = cursor.fetchone()
            connection.close()

            for i in range(1, 4):
                update_info[i].insert(0, query_result[i-1])

            tkinter.Button(master=self.form_frame, text="Módosítás", command=send_update).grid(column=0, row=4, columnspan=2)


        for child in self.form_frame.winfo_children():
            child.destroy()

        connection = mysql.connector.connect(host=self.master.dbhost, database=self.master.dbname, user=self.master.dbuser, password=self.master.dbpwd)
        cursor = connection.cursor()
        sql = "SELECT vezetoi_szam, vezeteknev, keresztnev FROM vezeto"
        cursor.execute(sql)

        drivers: dict[str, str] = {str(driver[0]) + " (" + str(driver[1] + " " + str(driver[2]) + ")"): driver[0] for driver in cursor.fetchall()}

        driver_choice = tkinter.StringVar(master=self.form_frame)
        driver_choice.set(sorted(drivers.keys())[0])

        self.form_frame.columnconfigure(index=0, weight=1)
        self.form_frame.columnconfigure(index=1, weight=1)

        update_info: Union[tuple[tkinter.Entry, tkinter.Entry, tkinter.Entry, tkinter.Entry], None] = None

        tkinter.Label(master=self.form_frame, text="Válasszon vezetőt!", bg=self["bg"]).grid(column=0, row=0, sticky="E")
        tkinter.OptionMenu(self.form_frame, driver_choice, *drivers).grid(column=1, row=0, sticky="W")
        tkinter.Button(master=self.form_frame, text="Kiválasztás", command=show_form).grid(column=0, row=1, columnspan=2)


    def modify_line(self) -> None:
        def send_update() -> None:
            connection = mysql.connector.connect(host=self.master.dbhost, database=self.master.dbname, user=self.master.dbuser, password=self.master.dbpwd)
            cursor = connection.cursor()
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
            

        def show_form() -> None:
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

        lines: list[str] = [line[0] for line in cursor.fetchall()]

        line_choice = tkinter.StringVar(master=self.form_frame)
        line_choice.set(lines[0])

        self.form_frame.columnconfigure(index=0, weight=1)
        self.form_frame.columnconfigure(index=1, weight=1)

        update_info: Union[tuple[tkinter.Entry, tkinter.Entry], None] = None

        tkinter.Label(master=self.form_frame, text="Válassza ki a vonalat!", bg=self["bg"]).grid(column=0, row=0, sticky="E")
        tkinter.OptionMenu(self.form_frame, line_choice, *lines).grid(column=1, row=0, sticky="W")
        tkinter.Button(master=self.form_frame, text="Kiválasztás", command=show_form).grid(column=0, row=1, columnspan=2)
