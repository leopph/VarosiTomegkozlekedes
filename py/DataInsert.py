import ContentPage
import tkinter
import tkinter.ttk
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

            tkinter.ttk.Button(self.content_frame, text = "Új vonal", command = self.new_line).grid(row = 0, column = 0, sticky="E")
            tkinter.ttk.Button(self.content_frame, text = "Új megálló", command = self.new_stop).grid(row = 0, column = 1)
            tkinter.ttk.Button(self.content_frame, text = "Új vezető", command = self.new_driver).grid(row = 0, column = 2)
            tkinter.ttk.Button(self.content_frame, text = "Új járműtípus", command = self.new_vehicle_type).grid(row = 0, column = 3)
            tkinter.ttk.Button(self.content_frame, text = "Új jármű", command = self.new_vehicle).grid(row = 0, column = 4)
            tkinter.ttk.Button(self.content_frame, text = "Új járat", command = self.new_route).grid(row = 0, column = 5, sticky="W")



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

        driver_number_entry = tkinter.ttk.Entry(master=form_frame)
        last_name_entry = tkinter.ttk.Entry(master=form_frame)
        first_name_entry = tkinter.ttk.Entry(master=form_frame)
        birth_date_entry = tkinter.ttk.Entry(master=form_frame)

        driver_number_entry.grid(column=1, row=0, sticky="W")
        last_name_entry.grid(column=1, row=1, sticky="W")
        first_name_entry.grid(column=1, row=2, sticky="W")
        birth_date_entry.grid(column=1, row=3, sticky="W")

        tkinter.Label(master=form_frame, text="Vezetői szám:", bg=self["bg"]).grid(column=0, row=0, sticky="E")
        tkinter.Label(master=form_frame, text="Vezetéknév:", bg=self["bg"]).grid(column=0, row=1, sticky="E")
        tkinter.Label(master=form_frame, text="Keresztnév", bg=self["bg"]).grid(column=0, row=2, sticky="E")
        tkinter.Label(master=form_frame, text="Születési dátum:", bg=self["bg"]).grid(column=0, row=3, sticky="E")
        
        tkinter.ttk.Button(master=form_frame, text="Felvitel", command=process_new_driver).grid(column=0, row=4, columnspan=2)


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

        stop_name_entry = tkinter.ttk.Entry(form_frame)
        location_entry = tkinter.ttk.Entry(form_frame)

        stop_name_entry.grid(column = 1, row = 0, sticky="W")
        location_entry.grid(column = 1, row = 1, sticky="W")

        tkinter.Label(form_frame, text = "Név:", bg = self["bg"]).grid(row = 0, column = 0, sticky = "E")
        tkinter.Label(form_frame, text = "Hely:", bg = self["bg"]).grid(row = 1, column = 0, sticky = "E")

        tkinter.ttk.Button(form_frame, text = "Felvitel", command = process_new_stop).grid(row = 2, column = 0, columnspan = 2)



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

        line_name_entry = tkinter.ttk.Entry(form_frame)
        length_entry = tkinter.ttk.Entry(form_frame)

        line_name_entry.grid(column = 1, row = 0, sticky="W")
        length_entry.grid(column = 1, row = 1, sticky="W")

        tkinter.Label(form_frame, text = "Vonalnév:", bg = self["bg"]).grid(row = 0, column = 0, sticky = "E")
        tkinter.Label(form_frame, text = "Hossz:", bg = self["bg"]).grid(row = 1, column = 0, sticky = "E")

        tkinter.ttk.Button(form_frame, text = "Felvitel", command = process_new_line).grid(row = 2, column = 0, columnspan = 2)



    def new_vehicle_type(self) -> None:
        def process_new_vehicle_type() -> None:
            connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
            cursor = connection.cursor()

            try:
                sql = "INSERT INTO jarmutipus(nev, elektromos) VALUES(%s, %s)"
                cursor.execute(sql, params = (name_entry.get().strip(),electric_options[is_electric.get()]))
                connection.commit()

                name_entry.delete(0, "end")
                is_electric.set(sorted(electric_options)[0])

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

        name_entry = tkinter.ttk.Entry(form_frame)
        name_entry.grid(column = 1, row = 0, sticky="W")

        electric_options = {"Igen": True, "Nem": False}

        is_electric = tkinter.StringVar(form_frame)
        is_electric.set(sorted(electric_options)[0])
        tkinter.ttk.OptionMenu(form_frame, is_electric, is_electric.get(), *electric_options).grid(row = 1, column = 1, sticky="W")

        tkinter.Label(form_frame, text = "Típusnév:", bg = self["bg"]).grid(row = 0, column = 0, sticky = "E")
        tkinter.Label(form_frame, text = "Elektromos-e:", bg = self["bg"]).grid(row = 1, column = 0, sticky = "E")

        tkinter.ttk.Button(form_frame, text = "Felvitel", command = process_new_vehicle_type).grid(row = 2, column = 0, columnspan = 2)



    def new_vehicle(self) -> None:
        def process_new_vehicle() -> None:
            connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
            cursor = connection.cursor()

            try:
                sql = "INSERT INTO jarmu(rendszam, alacsony_padlos, tipus_nev, vezetoi_szam) VALUES(%s, %s, %s, %s)"
                cursor.execute(sql, params = (license_entry.get().strip(), floor_options[floor.get()], type_.get(), driver_id_entries[driver.get()]))
                connection.commit()

                license_entry.delete(0, "end")
                floor.set(sorted(floor_options)[0])
                type_.set(type_name_entries[0])
                driver.set(sorted(driver_id_entries.keys())[0])

                tkinter.messagebox.showinfo("Siker", "Sikeres adatfelvitel!")

            except mysql.connector.Error as error:
                connection.rollback()
                tkinter.messagebox.showerror("Hiba", "Hiba történt az adatfelvitel során. Kérjük ellenőrizze a megadott adatokat!\n" + str(error))

            finally:
                connection.close()

        def get_foreign_key_entries() -> tuple[dict[str, str], list[str]]:
            connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
            cursor = connection.cursor()

            sql = "SELECT vezetoi_szam, vezeteknev, keresztnev FROM vezeto"
            cursor.execute(sql)
            drivers: dict[str, str] = {str(driver[0]) + " (" + str(driver[1]) + " " + str(driver[2]) + ")": driver[0] for driver in cursor.fetchall()}

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

        license_entry = tkinter.ttk.Entry(form_frame)
        license_entry.grid(column = 1, row = 0, sticky="W")

        floor_options = {"Igen": True, "Nem": False}

        floor = tkinter.StringVar(form_frame)
        floor.set(sorted(floor_options)[0])
        tkinter.ttk.OptionMenu(form_frame, floor, floor.get(), *floor_options).grid(row = 1, column = 1, sticky="W")

        type_ = tkinter.StringVar(form_frame)
        type_.set(type_name_entries[0])
        tkinter.ttk.OptionMenu(form_frame, type_, type_.get(), *type_name_entries).grid(row = 2, column = 1, sticky="W")

        driver = tkinter.StringVar(form_frame)
        driver.set(sorted(driver_id_entries.keys())[0])
        tkinter.ttk.OptionMenu(form_frame, driver, driver.get(), *driver_id_entries).grid(row = 3, column = 1, sticky="W")

        tkinter.Label(form_frame, text = "Rendszám:", bg = self["bg"]).grid(row = 0, column = 0, sticky = "E")
        tkinter.Label(form_frame, text = "Alacsony padlós-e:", bg = self["bg"]).grid(row = 1, column = 0, sticky = "E")
        tkinter.Label(form_frame, text = "Jármű típus:", bg = self["bg"]).grid(row = 2, column = 0, sticky = "E")
        tkinter.Label(form_frame, text = "Vezető száma:", bg = self["bg"]).grid(row = 3, column = 0, sticky = "E")

        tkinter.ttk.Button(form_frame, text = "Felvitel", command = process_new_vehicle).grid(row = 4, column = 0, columnspan = 2)

        

    def new_route(self) -> None:
        def process_new_route() -> None:
            connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
            cursor = connection.cursor()

            try:
                for i in range(2):
                    if i in [direction_options[start[2].get()] for start in starts] + [direction_options[stop[2].get()] for stop in stops]:
                        cursor.execute("INSERT INTO jarat(vonal_nev, visszamenet) VALUES(%s, %s)", (line.get(), i))

                if starts:
                    sql = "INSERT INTO indul(rendszam, vonal_nev, visszamenet, mikor) VALUES"
                    for start in starts:
                        sql += "(\"{}\", \"{}\", {}, \"{}\"),".format(start[1].get(), line.get(), direction_options[start[2].get()], start[0].get().strip())
                    cursor.execute(sql[:-1])

                if stops:
                    sql2 = "INSERT INTO megall(vonal_nev, visszamenet, megallo_id, mikor) VALUES"
                    for stop in stops:
                        sql2 += "(\"{}\", {}, {}, \"{}\"),".format(line.get(), direction_options[stop[2].get()], stop_id_entries[stop[1].get()], stop[0].get().strip())
                    cursor.execute(sql2[:-1])

                connection.commit()

                line.set(line_entries[0])
                
                for start in starts:
                    start[0].delete(0, "end")
                    start[1].set(sorted(license_entries.keys())[0])
                    start[2].set(sorted(direction_options.keys())[0])

                for stop in stops:
                    stop[0].delete(0, "end")
                    stop[1].set(sorted(stop_id_entries)[0])
                    stop[2].set(sorted(direction_options.keys())[0])

                if starts or stops:
                    tkinter.messagebox.showinfo("Siker", "Sikeres adatfelvitel!")

            except mysql.connector.Error as error:
                connection.rollback()
                tkinter.messagebox.showerror("Hiba", "Hiba történt az adatfelvitel során. Kérjük ellenőrizze a megadott adatokat!\n" + str(error))

            finally:
                connection.close()


        def get_foreign_key_entries() -> tuple[list[str], dict[str, str], dict[str, int]]:
            connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
            cursor = connection.cursor()

            sql = "SELECT nev FROM vonal WHERE nev NOT IN (SELECT DISTINCT vonal_nev FROM jarat WHERE visszamenet = 0) and nev NOT IN (SELECT DISTINCT vonal_nev FROM jarat WHERE visszamenet = 1)"
            cursor.execute(sql)
            lines: list[str] = [line[0] for line in cursor.fetchall()]

            sql = "SELECT rendszam, tipus_nev FROM jarmu"
            cursor.execute(sql)
            licenses: dict[str, str] = {str(license[0]) + " (" + license[1] + ")": license[0] for license in cursor.fetchall()}

            sql = "SELECT id, nev FROM megallo"
            cursor.execute(sql)
            stop_ids: dict[str, int] = {str(stop_id[0]) + " (" + stop_id[1] + ")": stop_id[0] for stop_id in cursor.fetchall()}

            connection.close()

            return lines, licenses, stop_ids

        def expand_starts_menu() -> None:
            new_start_button.grid(row = len(starts) + 1, column = 0, columnspan=3)

            time_entry = tkinter.ttk.Entry(starts_frame)
            time_entry.grid(row = len(starts), column = 0)

            license = tkinter.StringVar(starts_frame)
            license.set(sorted(license_entries.keys())[0])
            tkinter.ttk.OptionMenu(starts_frame, license, license.get(), *license_entries).grid(row = len(starts), column = 1)

            direction = tkinter.StringVar(starts_frame)
            direction.set(sorted(direction_options.keys())[0])
            tkinter.ttk.OptionMenu(starts_frame, direction, direction.get(), *direction_options).grid(row = len(starts), column = 2)

            starts.append((time_entry, license, direction))


        def expand_stops_menu() -> None:
            new_stop_button.grid(row = len(stops) + 1, column = 0, columnspan=3)

            time_entry = tkinter.ttk.Entry(stops_frame)
            time_entry.grid(row = len(stops), column = 0)

            stop_id = tkinter.StringVar(stops_frame)
            stop_id.set(sorted(stop_id_entries.keys())[0])
            tkinter.ttk.OptionMenu(stops_frame, stop_id, stop_id.get(), *stop_id_entries.keys()).grid(row = len(stops), column = 1)

            direction = tkinter.StringVar(stops_frame)
            direction.set(sorted(direction_options.keys())[0])
            tkinter.ttk.OptionMenu(stops_frame, direction, direction.get(), *direction_options).grid(row = len(stops), column = 2)

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
        tkinter.ttk.OptionMenu(form_frame, line, line.get(), *line_entries).grid(row = 1, column = 0, sticky="n")

        starts = list()
        starts_frame = tkinter.Frame(form_frame, bg=self["bg"])
        starts_frame.grid(row = 1, column = 1)

        new_start_button = tkinter.ttk.Button(starts_frame, text = "Új indulás")
        new_start_button.configure(command = expand_starts_menu)
        new_start_button.grid(row = 0, column = 0, columnspan=3)

        stops = list()
        stops_frame = tkinter.Frame(form_frame, bg=self["bg"])
        stops_frame.grid(row = 1, column = 2)

        new_stop_button = tkinter.ttk.Button(stops_frame, text = "Új megállás")
        new_stop_button.configure(command = expand_stops_menu)
        new_stop_button.grid(row = 0, column = 0, columnspan=3)

        direction_options = {"Visszamenet": True, "Odamenet": False}

        tkinter.ttk.Button(form_frame, text = "Felvitel", command = process_new_route).grid(row = 2, column = 0, columnspan = 3)
