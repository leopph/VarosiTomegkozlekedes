import ContentPage
import tkinter
import tkinter.messagebox
import mysql.connector




class DataInsertPage(ContentPage.ContentPage):
    def __init__(self, data, *args, **kwargs) -> None:
        ContentPage.ContentPage.__init__(self, data, *args, **kwargs)

        self.title_frame = None
        self.content_frame = None

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
            self.rowconfigure(0, weight = 1)
            self.rowconfigure(1, weight = 9)
            self.columnconfigure(0, weight = 1)

            self.title_frame = tkinter.Frame(master=self, bg=self["bg"])
            self.title_frame.grid(column=0, row=0, sticky="NESW")

            self.title_frame.columnconfigure(0, weight = 1)

            tkinter.Label(self.title_frame, text = "Új adatok felvitele", bg = self["bg"], font = ("", 26)).grid(row = 0, column = 0, sticky = "NESW")
            tkinter.Label(self.title_frame, text = "Válassza ki a felvinni kívánt adatot!", bg = self["bg"], font = ("", 22)).grid(row = 1, column = 0, sticky = "NESW")

            self.content_frame = tkinter.Frame(self, bg = self["bg"])
            self.content_frame.grid(row = 1, column = 0, sticky = "NESW")

            self.content_frame.columnconfigure(0, weight = 1)
            self.content_frame.columnconfigure(5, weight = 1)

            tkinter.Button(self.content_frame, text = "Új vonal", bg = self["bg"], font = ("", 12), command = self.new_line).grid(row = 0, column = 0, sticky="E")
            tkinter.Button(self.content_frame, text = "Új megálló", bg = self["bg"], font = ("", 12), command = self.new_stop).grid(row = 0, column = 1)
            tkinter.Button(self.content_frame, text = "Új vezető", bg = self["bg"], font = ("", 12), command = self.new_driver).grid(row = 0, column = 2)
            tkinter.Button(self.content_frame, text = "Új járműtípus", bg = self["bg"], font = ("", 12), command = self.new_vehicle_type).grid(row = 0, column = 3)
            tkinter.Button(self.content_frame, text = "Új jármű", bg = self["bg"], font = ("", 12), command = self.new_vehicle).grid(row = 0, column = 4)
            tkinter.Button(self.content_frame, text = "Új járat", bg = self["bg"], font = ("", 12), command = self.new_route).grid(row = 0, column = 5, sticky="W")



    def new_driver(self) -> None:
        def process_new_driver() -> None:
            connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
            cursor = connection.cursor()
            sql = "INSERT INTO vezeto(vezetoi_szam, vezeteknev, keresztnev, szul_datum) VALUES(%s, %s, %s, %s)"

            try:
                cursor.execute(sql, (driver_number_entry.get(), last_name_entry.get(), first_name_entry.get(), birth_date_entry.get()))
                connection.commit()

                driver_number_entry.delete(0, "end")
                last_name_entry.delete(0, "end")
                first_name_entry.delete(0, "end")
                birth_date_entry.delete(0, "end")

                tkinter.messagebox.showinfo("Siker", "Sikeres adatfelvitel!")
                
            except mysql.connector.Error as error:
                connection.rollback()
                tkinter.messagebox.showerror("Hiba", "Hiba történt az adatfelvitel során. Kérjük ellenőrizze a megadott adatokat!\n" + str(error))

            finally:
                connection.close()


        form_frame = tkinter.Frame(self.content_frame, bg = self["bg"])
        form_frame.grid(row = 1, column = 0, columnspan=6, sticky = "NESW")

        form_frame.columnconfigure(0, weight = 1)
        form_frame.columnconfigure(1, weight = 1)

        driver_number_entry = tkinter.Entry(master=form_frame)
        last_name_entry = tkinter.Entry(master=form_frame)
        first_name_entry = tkinter.Entry(master=form_frame)
        birth_date_entry = tkinter.Entry(master=form_frame)

        driver_number_entry.grid(column=1, row=0, sticky="W")
        last_name_entry.grid(column=1, row=1, sticky="W")
        first_name_entry.grid(column=1, row=2, sticky="W")
        birth_date_entry.grid(column=1, row=3, sticky="W")

        tkinter.Label(master=form_frame, text="Vezetői szám:", bg=self["bg"]).grid(column=0, row=0, sticky="E")
        tkinter.Label(master=form_frame, text="Vezetéknév:", bg=self["bg"]).grid(column=0, row=1, sticky="E")
        tkinter.Label(master=form_frame, text="Keresztnév", bg=self["bg"]).grid(column=0, row=2, sticky="E")
        tkinter.Label(master=form_frame, text="Születési dátum:", bg=self["bg"]).grid(column=0, row=3, sticky="E")
        
        tkinter.Button(master=form_frame, text="Felvitel", command=process_new_driver).grid(column=0, row=4, columnspan=2)


    def new_stop(self) -> None:
        def process_new_stop() -> None:
            connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
            cursor = connection.cursor()

            try:
                sql = "INSERT INTO megallo(nev, hely) VALUES(%s, %s)"
                cursor.execute(sql, params = (stop_name_entry.get().strip(), location_entry.get().strip()))
                connection.commit()

                stop_name_entry.delete(0, "end")
                location_entry.delete(0, "end")

                tkinter.messagebox.showinfo("Siker", "Sikeres adatfelvitel!")

            except mysql.connector.Error as error:
                connection.rollback()
                tkinter.messagebox.showerror("Hiba", "Hiba történt az adatfelvitel során. Kérjük ellenőrizze a megadott adatokat!\n" + str(error))

            finally:
                connection.close()


        form_frame = tkinter.Frame(self.content_frame, bg = self["bg"])
        form_frame.grid(row = 1, column = 0, columnspan=6, sticky = "NESW")

        form_frame.columnconfigure(0, weight = 1)
        form_frame.columnconfigure(1, weight = 1)

        stop_name_entry = tkinter.Entry(form_frame)
        location_entry = tkinter.Entry(form_frame)

        stop_name_entry.grid(column = 1, row = 0, sticky="W")
        location_entry.grid(column = 1, row = 1, sticky="W")

        tkinter.Label(form_frame, text = "Név:", bg = self["bg"]).grid(row = 0, column = 0, sticky = "E")
        tkinter.Label(form_frame, text = "Hely:", bg = self["bg"]).grid(row = 1, column = 0, sticky = "E")

        tkinter.Button(form_frame, text = "Felvitel", bg = self["bg"], command = process_new_stop).grid(row = 2, column = 0, columnspan = 2)



    def new_line(self) -> None:
        def process_new_line() -> None:
            connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
            cursor = connection.cursor()

            try:
                sql = "INSERT INTO vonal VALUES(%s, %s)"
                cursor.execute(sql, params = (line_name_entry.get().strip(), length_entry.get().strip()))

                sql = "INSERT INTO jarat VALUES(%s, %s), (%s, %s)"
                cursor.execute(sql, params = (line_name_entry.get().strip(), 0, line_name_entry.get().strip(), 1))

                connection.commit()

                line_name_entry.delete(0, "end")
                length_entry.delete(0, "end")

                tkinter.messagebox.showinfo("Siker", "Sikeres adatfelvitel!")

            except mysql.connector.Error as error:
                connection.rollback()
                tkinter.messagebox.showerror("Hiba", "Hiba történt az adatfelvitel során. Kérjük ellenőrizze a megadott adatokat!\n" + str(error))

            finally:
                connection.close()


        form_frame = tkinter.Frame(self.content_frame, bg = self["bg"])
        form_frame.grid(row = 1, column = 0, columnspan=6, sticky = "NESW")

        form_frame.columnconfigure(0, weight = 1)
        form_frame.columnconfigure(1, weight = 1)

        line_name_entry = tkinter.Entry(form_frame)
        length_entry = tkinter.Entry(form_frame)

        line_name_entry.grid(column = 1, row = 0, sticky="W")
        length_entry.grid(column = 1, row = 1, sticky="W")

        tkinter.Label(form_frame, text = "Vonalnév:", bg = self["bg"]).grid(row = 0, column = 0, sticky = "E")
        tkinter.Label(form_frame, text = "Hossz:", bg = self["bg"]).grid(row = 1, column = 0, sticky = "E")

        tkinter.Button(form_frame, text = "Felvitel", bg = self["bg"], command = process_new_line).grid(row = 2, column = 0, columnspan = 2)



    def new_vehicle_type(self) -> None:
        def process_new_vehicle_type() -> None:
            connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
            cursor = connection.cursor()

            try:
                sql = "INSERT INTO jarmutipus(nev, elektromos) VALUES(%s, %s)"
                cursor.execute(sql, params = (name_entry.get().strip(), is_electric.get()))
                connection.commit()

                name_entry.delete(0, "end")
                is_electric.set(False)

                tkinter.messagebox.showinfo("Siker", "Sikeres adatfelvitel!")

            except mysql.connector.Error as error:
                connection.rollback()
                tkinter.messagebox.showerror("Hiba", "Hiba történt az adatfelvitel során. Kérjük ellenőrizze a megadott adatokat!\n" + str(error))

            finally:
                connection.close()

        form_frame = tkinter.Frame(self.content_frame, bg = self["bg"])
        form_frame.grid(row = 1, column = 0, columnspan=6, sticky = "NESW")

        form_frame.columnconfigure(0, weight = 1)
        form_frame.columnconfigure(1, weight = 1)

        name_entry = tkinter.Entry(form_frame)
        name_entry.grid(column = 1, row = 0, sticky="W")

        is_electric = tkinter.BooleanVar(form_frame)
        tkinter.OptionMenu(form_frame, is_electric, *[True, False]).grid(row = 1, column = 1, sticky="W")

        tkinter.Label(form_frame, text = "Típusnév:", bg = self["bg"]).grid(row = 0, column = 0, sticky = "E")
        tkinter.Label(form_frame, text = "Elektromos-e:", bg = self["bg"]).grid(row = 1, column = 0, sticky = "E")

        tkinter.Button(form_frame, text = "Felvitel", bg = self["bg"], command = process_new_vehicle_type).grid(row = 2, column = 0, columnspan = 2)



    def new_vehicle(self) -> None:
        def process_new_vehicle() -> None:
            connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
            cursor = connection.cursor()

            try:
                sql = "INSERT INTO jarmu(rendszam, alacsony_padlos, tipus_nev, vezetoi_szam) VALUES(%s, %s, %s, %s)"
                cursor.execute(sql, params = (license_entry.get().strip(), floor.get(), type_.get(), driver.get()))
                connection.commit()

                license_entry.delete(0, "end")
                floor.set(False)
                type_.set(type_name_entries[0])
                driver.set(driver_id_entries[0])

                tkinter.messagebox.showinfo("Siker", "Sikeres adatfelvitel!")

            except mysql.connector.Error as error:
                connection.rollback()
                tkinter.messagebox.showerror("Hiba", "Hiba történt az adatfelvitel során. Kérjük ellenőrizze a megadott adatokat!\n" + str(error))

            finally:
                connection.close()

        def get_foreign_key_entries() -> tuple[list[str], list[str]]:
            connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
            cursor = connection.cursor()

            sql = "SELECT vezetoi_szam FROM vezeto"
            cursor.execute(sql)
            drivers: list[str] = [driver_id[0] for driver_id in cursor.fetchall()]

            sql = "SELECT nev FROM jarmutipus"
            cursor.execute(sql)
            types: list[str] = [type[0] for type in cursor.fetchall()]

            connection.close()

            return drivers, types


        form_frame = tkinter.Frame(self.content_frame, bg = self["bg"])
        form_frame.grid(row = 1, column = 0, columnspan=6, sticky = "NESW")

        form_frame.columnconfigure(0, weight = 1)
        form_frame.columnconfigure(1, weight = 1)

        driver_id_entries, type_name_entries = get_foreign_key_entries()

        license_entry = tkinter.Entry(form_frame)
        license_entry.grid(column = 1, row = 0, sticky="W")

        floor = tkinter.BooleanVar(form_frame)
        floor.set(False)
        tkinter.OptionMenu(form_frame, floor, *[False, True]).grid(row = 1, column = 1, sticky="W")

        type_ = tkinter.StringVar(form_frame)
        type_.set(type_name_entries[0])
        tkinter.OptionMenu(form_frame, type_, *type_name_entries).grid(row = 2, column = 1, sticky="W")

        driver = tkinter.StringVar(form_frame)
        driver.set(driver_id_entries[0])
        tkinter.OptionMenu(form_frame, driver, *driver_id_entries).grid(row = 3, column = 1, sticky="W")

        tkinter.Label(form_frame, text = "Rendszám:", bg = self["bg"]).grid(row = 0, column = 0, sticky = "E")
        tkinter.Label(form_frame, text = "Alacsony padlós-e:", bg = self["bg"]).grid(row = 1, column = 0, sticky = "E")
        tkinter.Label(form_frame, text = "Jármű típus:", bg = self["bg"]).grid(row = 2, column = 0, sticky = "E")
        tkinter.Label(form_frame, text = "Vezető száma:", bg = self["bg"]).grid(row = 3, column = 0, sticky = "E")

        tkinter.Button(form_frame, text = "Felvitel", bg = self["bg"], command = process_new_vehicle).grid(row = 4, column = 0, columnspan = 2)

        

    def new_route(self) -> None:
        def process_new_route() -> None:
            connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
            cursor = connection.cursor()

            try:
                for i in range(2):
                    if i in [start[2].get() for start in starts] + [stop[2].get() for stop in stops]:
                        cursor.execute("INSERT INTO jarat(vonal_nev, visszamenet) VALUES(%s, %s)", (line.get(), i))

                if starts:
                    sql = "INSERT INTO indul(rendszam, vonal_nev, visszamenet, mikor) VALUES"
                    for start in starts:
                        sql += "(\"{}\", \"{}\", {}, \"{}\"),".format(start[1].get(), line.get(), start[2].get(), start[0].get().strip())
                    cursor.execute(sql[:-1])

                if stops:
                    sql2 = "INSERT INTO megall(vonal_nev, visszamenet, megallo_id, mikor) VALUES"
                    for stop in stops:
                        sql2 += "(\"{}\", {}, {}, \"{}\"),".format(line.get(), stop[2].get(), stop_id_entries[stop[1].get()], stop[0].get().strip())
                    cursor.execute(sql2[:-1])

                connection.commit()

                line.set(line_entries[0])
                
                for start in starts:
                    start[0].delete(0, "end")
                    start[1].set(license_entries[0])
                    start[2].set(False)

                for stop in stops:
                    stop[0].delete(0, "end")
                    stop[1].set(sorted(stop_id_entries)[0])
                    stop[2].set(False)

                if starts or stops:
                    tkinter.messagebox.showinfo("Siker", "Sikeres adatfelvitel!")

            except mysql.connector.Error as error:
                connection.rollback()
                tkinter.messagebox.showerror("Hiba", "Hiba történt az adatfelvitel során. Kérjük ellenőrizze a megadott adatokat!\n" + str(error))

            finally:
                connection.close()


        def get_foreign_key_entries() -> tuple[list[str], list[str], dict[str, int]]:
            connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
            cursor = connection.cursor()

            sql = "SELECT nev FROM vonal WHERE nev NOT IN (SELECT DISTINCT vonal_nev FROM jarat)"
            cursor.execute(sql)
            lines: list[str] = [line[0] for line in cursor.fetchall()]

            sql = "SELECT rendszam FROM jarmu"
            cursor.execute(sql)
            licenses: list[str] = [license[0] for license in cursor.fetchall()]

            sql = "SELECT id, nev FROM megallo"
            cursor.execute(sql)
            stop_ids: dict[str, int] = {str(stop_id[0]) + " (" + stop_id[1] + ")": stop_id[0] for stop_id in cursor.fetchall()}

            connection.close()

            return lines, licenses, stop_ids

        def expand_starts_menu() -> None:
            new_start_button.grid(row = len(starts) + 1, column = 0, columnspan=3)

            time_entry = tkinter.Entry(starts_frame)
            time_entry.grid(row = len(starts), column = 0)

            license = tkinter.StringVar(starts_frame)
            license.set(license_entries[0])
            tkinter.OptionMenu(starts_frame, license, *license_entries).grid(row = len(starts), column = 1)

            direction = tkinter.BooleanVar(starts_frame)
            direction.set(False)
            tkinter.OptionMenu(starts_frame, direction, *[True, False]).grid(row = len(starts), column = 2)

            starts.append((time_entry, license, direction))


        def expand_stops_menu() -> None:
            new_stop_button.grid(row = len(stops) + 1, column = 0, columnspan=3)

            time_entry = tkinter.Entry(stops_frame)
            time_entry.grid(row = len(stops), column = 0)

            stop_id = tkinter.StringVar(stops_frame)
            stop_id.set(sorted(stop_id_entries.keys())[0])
            tkinter.OptionMenu(stops_frame, stop_id, *stop_id_entries.keys()).grid(row = len(stops), column = 1)

            direction = tkinter.BooleanVar(stops_frame)
            direction.set(False)
            tkinter.OptionMenu(stops_frame, direction, *[True, False]).grid(row = len(stops), column = 2)

            stops.append((time_entry, stop_id, direction))


        form_frame = tkinter.Frame(self.content_frame, bg = self["bg"])
        form_frame.grid(row = 1, column = 0, columnspan=6, sticky = "NESW")

        form_frame.columnconfigure(0, weight = 1)
        form_frame.columnconfigure(1, weight = 1)
        form_frame.columnconfigure(2, weight = 1)

        tkinter.Label(form_frame, text = "Vonal száma", bg=self["bg"], font=("", 14)).grid(row = 0, column = 0)
        tkinter.Label(form_frame, text = "Indulások", bg=self["bg"], font=("", 14)).grid(row = 0, column = 1)
        tkinter.Label(form_frame, text = "Megállások", bg=self["bg"], font=("", 14)).grid(row = 0, column = 2)

        line_entries, license_entries, stop_id_entries = get_foreign_key_entries()

        line = tkinter.StringVar(form_frame)
        line.set(line_entries[0])
        tkinter.OptionMenu(form_frame, line, *line_entries).grid(row = 1, column = 0, sticky="n")

        starts = list()
        starts_frame = tkinter.Frame(form_frame, bg=self["bg"])
        starts_frame.grid(row = 1, column = 1)

        new_start_button = tkinter.Button(starts_frame, text = "Új indulás")
        new_start_button.configure(command = expand_starts_menu)
        new_start_button.grid(row = 0, column = 0, columnspan=3)

        stops = list()
        stops_frame = tkinter.Frame(form_frame, bg=self["bg"])
        stops_frame.grid(row = 1, column = 2)

        new_stop_button = tkinter.Button(stops_frame, text = "Új megállás")
        new_stop_button.configure(command = expand_stops_menu)
        new_stop_button.grid(row = 0, column = 0, columnspan=3)

        tkinter.Button(form_frame, text = "Felvitel", bg = self["bg"], command = process_new_route).grid(row = 2, column = 0, columnspan = 3)
