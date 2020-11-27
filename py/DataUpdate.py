import tkinter
import tkinter.ttk
import tkinter.messagebox
import mysql.connector
from mysql.connector.dbapi import Date
import ContentPage
from typing import Union
from datetime import timedelta


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

            tkinter.ttk.Button(master=self.content_frame, text="Vonal módosítása", command=self.modify_line).grid(column=0, row=0, sticky="E")
            tkinter.ttk.Button(master=self.content_frame, text="Megálló módosítása", command=self.modify_stop).grid(column=1, row=0)
            tkinter.ttk.Button(master=self.content_frame, text="Vezető módosítása", command=self.modify_driver).grid(column=2, row=0)
            tkinter.ttk.Button(master=self.content_frame, text="Járműtípus módosítása", command=self.modify_type).grid(column=3, row=0)
            tkinter.ttk.Button(master=self.content_frame, text="Jármű módosítása", command=self.modify_vehicle).grid(column=4, row=0)
            tkinter.ttk.Button(master=self.content_frame, text="Járat módosítása", command=self.modify_route).grid(column=5, row=0, sticky="W")

            self.form_frame = tkinter.Frame(self.content_frame, bg=self["bg"])
            self.form_frame.grid(column=0, row=1, columnspan=6, sticky="NESW")


    def modify_route(self) -> None:
        # SQL COMMUNICATION
        def send_update() -> None:
            connection = mysql.connector.connect(host=self.master.dbhost, database=self.master.dbname, user=self.master.dbuser, password=self.master.dbpwd)
            cursor = connection.cursor()

            try:
                sql = "DELETE FROM indul WHERE vonal_nev = %s and visszamenet = %s"
                cursor.execute(sql, (routes[selection][0], routes[selection][1]))

                if start_entries:
                    sql = "INSERT INTO indul(rendszam, vonal_nev, visszamenet, mikor) VALUES"

                    for entry in start_entries:
                        sql += "(\"{}\", \"{}\", {}, \"{}\"),".format(entry[1].get(), routes[selection][0], routes[selection][1], entry[0].get())
                    
                    cursor.execute(sql[:-1])

                sql = "DELETE FROM megall WHERE vonal_nev = %s and visszamenet = %s"
                cursor.execute(sql, (routes[selection][0], routes[selection][1]))

                if stop_entries:
                    sql = "INSERT INTO megall(vonal_nev, visszamenet, megallo_id, mikor) VALUES"

                    for entry in stop_entries:
                        sql += "(\"{}\", {}, {}, \"{}\"),".format(routes[selection][0], routes[selection][1], stop_options[entry[1].get()], entry[0].get())

                    cursor.execute(sql[:-1])

                connection.commit()

                for child in self.form_frame.winfo_children():
                    child.destroy()

                tkinter.messagebox.showinfo("Siker", "Sikeres frissítés!")

            except mysql.connector.Error as error:
                connection.rollback()
                tkinter.messagebox.showerror("Hiba", "Hiba történt a módosítás során!\n" + str(error))

            finally:
                connection.close()


        # OPEN MENU TO DISPLAY AND UPDATE THE ROUTE DATA
        def show_form() -> None:
            # REMOVE A STOP OR START ENTRY
            def remove_entry(entry: tuple[tkinter.ttk.Entry, tkinter.ttk.Combobox, tkinter.ttk.Button], list: Union[list[tuple[tkinter.ttk.Entry, tkinter.ttk.Combobox, tkinter.ttk.Button]], None]) -> None:
                for elem in entry:
                    elem.destroy()
                list.remove(entry)


            # ADD A NEW EMPTY ENTRY TO THE STARTS LIST
            def add_start_entry() -> None:
                nonlocal starts_rowcount

                time = tkinter.ttk.Entry(master=starts_frame)
                time.grid(row = starts_rowcount - 1, column=0)

                license_box = tkinter.ttk.Combobox(master=starts_frame, values=sorted(license_options.keys()), state="readonly")
                license_box.set(sorted(license_options.keys())[0])
                license_box.grid(row=starts_rowcount - 1, column=1)

                remove_button = tkinter.ttk.Button(master=starts_frame, text="Törlés")
                remove_button.config(command=lambda start=(time, license_box, remove_button): remove_entry(start, start_entries))
                remove_button.grid(row=starts_rowcount - 1, column=2)

                start_entries.append((time, license_box, remove_button))

                new_start_button.grid(row=starts_rowcount)

                starts_rowcount += 1


            # ADD A NEW EMPTY ENTRY TO THE STARTS LIST
            def add_stop_entry() -> None:
                nonlocal stops_rowcount

                time = tkinter.ttk.Entry(master=stops_frame)
                time.grid(row = stops_rowcount - 1, column=0)

                stop_box = tkinter.ttk.Combobox(master=stops_frame, values=sorted(stop_options.keys()), state="readonly")
                stop_box.set(sorted(stop_options.keys())[0])
                stop_box.grid(row=stops_rowcount - 1, column=1)

                remove_button = tkinter.ttk.Button(master=stops_frame, text="Törlés")
                remove_button.config(command=lambda stop=(time, stop_box, remove_button): remove_entry(stop, stop_entries))
                remove_button.grid(row=stops_rowcount - 1, column=2)

                stop_entries.append((time, stop_box, remove_button))

                new_stop_button.grid(row=stops_rowcount)

                stops_rowcount += 1

            
            # SAVING SELECTION BEFORE DESTROYING
            nonlocal selection
            selection = combobox.get()

            for child in self.form_frame.winfo_children():
                child.destroy()

            # FORM LABELS
            tkinter.Label(master=self.form_frame, text="Vonal száma: " + str(routes[selection][0]), bg=self["bg"], font=("", 16)).grid(row=0, column=0, columnspan=2)
            tkinter.Label(master=self.form_frame, text="Indulások", bg=self["bg"], font=("", 14)).grid(row=1, column=0)
            tkinter.Label(master=self.form_frame, text="Megállások", bg=self["bg"], font=("", 14)).grid(row=1, column=1)

            # OPENING DB CONNECTION
            connection = mysql.connector.connect(host=self.master.dbhost, database=self.master.dbname, user=self.master.dbuser, password=self.master.dbpwd)
            cursor = connection.cursor()

            # QUERY FOR ALL THE POSSIBLE LICENSE PLATE NUMBERS
            cursor.execute("SELECT rendszam, tipus_nev FROM jarmu")
            license_options: dict[str, str] = {str(license[0]) + " (" + str(license[1]) + ")": str(license[0]) for license in cursor.fetchall()}

            # QUERY FOR ALL THE POSSIBLE STOP NAMES AND THEIR IDS
            cursor.execute("SELECT id, nev FROM megallo")
            nonlocal stop_options
            stop_options = {str(stop[0]) + " (" + stop[1] + ")": stop[0] for stop in cursor.fetchall()}

            # QUERY FOR ALL STORED START DATA
            sql = "SELECT indul.rendszam, jarmu.tipus_nev, indul.mikor FROM indul INNER JOIN jarmu ON indul.rendszam = jarmu.rendszam WHERE vonal_nev = %s and visszamenet = %s order by mikor"
            cursor.execute(sql, (routes[selection][0], routes[selection][1]))
            starts_db_stored: list[tuple[str, str, timedelta]] = [(start[0], start[1], start[2]) for start in cursor.fetchall()]

            # FRAME TO HOLD ALL THE START ENTRIES
            starts_frame = tkinter.Frame(self.form_frame, bg=self["bg"])
            starts_frame.grid(row=2, column=0)
            
            # LIST OF ALL THE CURRENT START ENTRIES
            nonlocal start_entries
            start_entries = list()

            # CREATING ENTRIES FOR THE STORED START DATA AND ADDING THEM TO THE FRAME
            for start in starts_db_stored:
                time = tkinter.ttk.Entry(master=starts_frame)
                time.insert(0, start[2])
                time.grid(row = len(start_entries), column=0)

                license_box = tkinter.ttk.Combobox(master=starts_frame, values=sorted(license_options.keys()), state="readonly")
                license_box.set(start[0] + " (" + start[1] + ")")
                license_box.grid(row=len(start_entries), column=1)

                remove_button = tkinter.ttk.Button(master=starts_frame, text="Törlés")
                remove_button.config(command=lambda start=(time, license_box, remove_button): remove_entry(start, start_entries))
                remove_button.grid(row=len(start_entries), column=2)

                start_entries.append((time, license_box, remove_button))

            # BUTTON TO ADD A NEW EMPTY START ENTRY
            new_start_button = tkinter.ttk.Button(master=starts_frame, text="Új indulás", command=add_start_entry)
            new_start_button.grid(row=len(start_entries), column=0, columnspan=3)

            starts_rowcount = len(start_entries) + 1

            # QUERY FOR ALL STORED STOP DATA
            sql = "SELECT megall.megallo_id, megallo.nev, megall.mikor FROM megall INNER JOIN megallo ON megall.megallo_id = megallo.id WHERE megall.vonal_nev = %s and megall.visszamenet = %s order by megall.mikor"
            cursor.execute(sql, (routes[selection][0], routes[selection][1]))
            stops_db_stored = [(stop[0], stop[1], stop[2]) for stop in cursor.fetchall()]

            # FRAME TO ADD STOP ENTRIES TO
            stops_frame = tkinter.Frame(master=self.form_frame, bg=self["bg"])
            stops_frame.grid(row=2, column=1)

            # LIST OF ALL THE CURRENT STOP ENTRIES
            nonlocal stop_entries
            stop_entries = list()

            # CREATING ENTRIES FOR THE STORED STOP DATA AND ADDING THEM TO THE FRAME
            for stop in stops_db_stored:
                time = tkinter.ttk.Entry(master=stops_frame)
                time.insert(0, stop[2])
                time.grid(row = len(stop_entries), column=0)

                stop_box = tkinter.ttk.Combobox(master=stops_frame, values=sorted(stop_options.keys()), state="readonly")
                stop_box.set(str(stop[0]) + " (" + str(stop[1]) + ")")
                stop_box.grid(row=len(stop_entries), column=1)

                remove_button = tkinter.ttk.Button(master=stops_frame, text="Törlés")
                remove_button.config(command=lambda stop=(time, stop_box, remove_button): remove_entry(stop, stop_entries))
                remove_button.grid(row=len(stop_entries), column=2)

                stop_entries.append((time, stop_box, remove_button))

            # BUTTON TO ADD A NEW EMPTY STOP ENTRY
            new_stop_button = tkinter.ttk.Button(master=stops_frame, text="Új megállás", command=add_stop_entry)
            new_stop_button.grid(row=len(stop_entries), column=0, columnspan=3)

            stops_rowcount = len(stop_entries) + 1

            connection.close()

            tkinter.ttk.Button(master=self.form_frame, text="Módosítás", command=send_update).grid(row = 3, column=0, columnspan=2)


        # ACTUAL FUNCTION BODY START HERE
        for child in self.form_frame.winfo_children():
            child.destroy()

        self.form_frame.columnconfigure(index=0, weight=1)
        self.form_frame.columnconfigure(index=1, weight=1)

        connection = mysql.connector.connect(host=self.master.dbhost, database=self.master.dbname, user=self.master.dbuser, password=self.master.dbpwd)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM jarat")

        routes: dict[str, tuple[str, bool]] = {str(route[0]) + " (" + str("visszafelé" if route[1] else "odafelé") + ")": (route[0], route[1]) for route in cursor.fetchall()}

        connection.close()

        combobox = tkinter.ttk.Combobox(master=self.form_frame, values=sorted(routes.keys()), state="readonly")
        combobox.set(sorted(routes.keys())[0])
        combobox.grid(row=0, column=1, sticky="W")

        selection: str = combobox.get()
        stop_options: Union[dict[str, int], None] = None
        start_entries: Union[list[tuple[tkinter.ttk.Entry, tkinter.ttk.Combobox, tkinter.ttk.Button]], None] = None
        stop_entries: Union[list[tuple[tkinter.ttk.Entry, tkinter.ttk.Combobox, tkinter.ttk.Button]], None] = None

        tkinter.Label(master=self.form_frame, text="Válasszon járatot!", bg=self["bg"]).grid(row=0, column=0, sticky="E")
        tkinter.ttk.Button(master=self.form_frame, text="Kiválasztás", command=show_form).grid(row=1, column=0, columnspan=2)



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
            update_info = (tkinter.ttk.Entry(master=self.form_frame), tkinter.ttk.Entry(master=self.form_frame))
            update_info[0].grid(row=0, column=1, sticky="W")
            update_info[0].insert(0, query_result[0])
            update_info[1].grid(row=1, column=1, sticky="W")
            update_info[1].insert(0, query_result[1])

            

            tkinter.Label(master=self.form_frame, text="Név:", bg=self["bg"]).grid(column=0, row=0, sticky="E")
            tkinter.Label(master=self.form_frame, text="Hely:", bg=self["bg"]).grid(column=0, row=1, sticky="E")
            tkinter.ttk.Button(master=self.form_frame, text="Módosítás", command=send_update).grid(column=0, row=2, columnspan=2)

        
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

        update_info: Union[tuple[tkinter.ttk.Entry, tkinter.ttk.Entry], None] = None

        tkinter.Label(master=self.form_frame, text="Válasszon megállót!", bg=self["bg"]).grid(column=0, row=0, sticky="E")
        tkinter.ttk.OptionMenu(self.form_frame, stop_selection, stop_selection.get(), *stops).grid(column=1, row=0, sticky="W")
        tkinter.ttk.Button(master=self.form_frame, text="Kiválasztás", command=show_form).grid(column=0, row=1, columnspan=2)


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
            update_info = (tkinter.ttk.Entry(master=self.form_frame), tkinter.BooleanVar(master=self.form_frame), tkinter.StringVar(master=self.form_frame), tkinter.StringVar(master=self.form_frame))
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

            tkinter.ttk.OptionMenu(self.form_frame, update_info[1], update_info[1].get(), *[True, False]).grid(column=1, row=1, sticky="W")
            tkinter.ttk.OptionMenu(self.form_frame, update_info[2], update_info[2].get(), *types).grid(column=1, row=2, sticky="W")
            tkinter.ttk.OptionMenu(self.form_frame, update_info[3], update_info[3].get(), *drivers).grid(column=1, row=3, sticky="W")

            tkinter.Label(master=self.form_frame, text="Rendszám:", bg=self["bg"]).grid(column=0, row=0, sticky="E")
            tkinter.Label(master=self.form_frame, text="Alacsony padlós-e:", bg=self["bg"]).grid(column=0, row=1, sticky="E")
            tkinter.Label(master=self.form_frame, text="Típus:", bg=self["bg"]).grid(column=0, row=2, sticky="E")
            tkinter.Label(master=self.form_frame, text="Vezető száma:", bg=self["bg"]).grid(column=0, row=3, sticky="E")

            tkinter.ttk.Button(master=self.form_frame, text="Módosítás", command=send_update).grid(column=0, row=4, columnspan=2)




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

        update_info: Union[tuple[tkinter.ttk.Entry, tkinter.BooleanVar, tkinter.StringVar, tkinter.StringVar], None] = None

        tkinter.Label(master=self.form_frame, text="Rendszám:", bg=self["bg"]).grid(column=0, row=0, sticky="E")
        tkinter.ttk.OptionMenu(self.form_frame, license_selection, license_selection.get(), *licenses).grid(column=1, row=0, sticky="W")
        tkinter.ttk.Button(master=self.form_frame, text="Kiválasztás", command=show_form).grid(column=0, row=1, columnspan=2)


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
            update_info = (tkinter.ttk.Entry(master=self.form_frame), tkinter.BooleanVar(master=self.form_frame))
            update_info[0].grid(column=1, row=0, sticky="W")
            update_info[0].insert(0, type_choice.get())
            
            connection = mysql.connector.connect(host=self.master.dbhost, database=self.master.dbname, user=self.master.dbuser, password=self.master.dbpwd)
            cursor = connection.cursor()
            sql = "SELECT elektromos FROM jarmutipus WHERE nev = %s"
            cursor.execute(sql, (type_choice.get(),))

            update_info[1].set(cursor.fetchone()[0])
            tkinter.ttk.OptionMenu(self.form_frame, update_info[1], update_info[1].get(), *[True, False]).grid(column=1, row=1, sticky="W")

            tkinter.Label(master=self.form_frame, text="Típus neve:", bg=self["bg"]).grid(column=0, row=0, sticky="E")
            tkinter.Label(master=self.form_frame, text="Elektromos-e:", bg=self["bg"]).grid(column=0, row=1, sticky="E")
            tkinter.ttk.Button(master=self.form_frame, text="Módosítás", command=send_update).grid(column=0, row=2, columnspan=2)
            

            


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

        update_info: Union[tuple[tkinter.ttk.Entry, tkinter.BooleanVar], None] = None

        tkinter.ttk.OptionMenu(self.form_frame, type_choice, type_choice.get(), *types).grid(column=1, row=0, sticky="W")
        tkinter.Label(master=self.form_frame, text="Válasson típus!", bg=self["bg"]).grid(column=0, row=0, sticky="E")
        tkinter.ttk.Button(master=self.form_frame, text="Kiválasztás", command=show_form).grid(column=0, row=1, columnspan=2)

        
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
            update_info = (tkinter.ttk.Entry(master=self.form_frame), tkinter.ttk.Entry(master=self.form_frame), tkinter.ttk.Entry(master=self.form_frame), tkinter.ttk.Entry(self.form_frame))
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

            tkinter.ttk.Button(master=self.form_frame, text="Módosítás", command=send_update).grid(column=0, row=4, columnspan=2)


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

        update_info: Union[tuple[tkinter.ttk.Entry, tkinter.ttk.Entry, tkinter.ttk.Entry, tkinter.ttk.Entry], None] = None

        tkinter.Label(master=self.form_frame, text="Válasszon vezetőt!", bg=self["bg"]).grid(column=0, row=0, sticky="E")
        tkinter.ttk.OptionMenu(self.form_frame, driver_choice, driver_choice.get(), *drivers).grid(column=1, row=0, sticky="W")
        tkinter.ttk.Button(master=self.form_frame, text="Kiválasztás", command=show_form).grid(column=0, row=1, columnspan=2)


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
            update_info = (tkinter.ttk.Entry(master=self.form_frame), tkinter.ttk.Entry(master=self.form_frame))
            update_info[0].grid(column=1, row=0, sticky="W")
            update_info[1].grid(column=1, row=1, sticky="W")
            update_info[0].insert(0, line_choice.get())

            connection = mysql.connector.connect(host=self.master.dbhost, database=self.master.dbname, user=self.master.dbuser, password=self.master.dbpwd)
            cursor =connection.cursor()
            sql = "SELECT hossz FROM vonal WHERE nev = %s"
            cursor.execute(sql, (line_choice.get(),))
            update_info[1].insert(0, cursor.fetchone()[0])
            connection.close()

            tkinter.ttk.Button(master=self.form_frame, text="Módosítás", command=send_update).grid(column=0, row=2, columnspan=2)
            

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
        tkinter.ttk.OptionMenu(self.form_frame, line_choice, line_choice.get(), *lines).grid(column=1, row=0, sticky="W")
        tkinter.ttk.Button(master=self.form_frame, text="Kiválasztás", command=show_form).grid(column=0, row=1, columnspan=2)
