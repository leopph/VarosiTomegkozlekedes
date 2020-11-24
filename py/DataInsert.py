import ContentPage
import tkinter
import tkinter.messagebox
import mysql.connector




class DataInsertPage(ContentPage.ContentPage):
    def __init__(self, data, *args, **kwargs):
        ContentPage.ContentPage.__init__(self, data, *args, **kwargs)

        self.title_frame = None
        self.content_frame = None

        self.refresh()



    def refresh(self):
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 9)
        self.columnconfigure(0, weight = 1)

        self.title_frame = tkinter.Frame(self, bg = self["bg"])
        self.title_frame.grid(column = 0, row = 0, sticky = "NESW")

        if self.master.user is None or not self.master.user.is_admin:
            self.title_frame.rowconfigure(0, weight = 1)
            self.title_frame.columnconfigure(0, weight = 1)

            tkinter.Label(self.title_frame, text = "Ez az oldal csak adminisztrátorok számára érhető el!", bg = self["bg"], font = (None, 24)).grid(row = 0, column = 0, sticky = "NESW")

        else:
            self.title_frame.rowconfigure(0, weight = 1)
            self.title_frame.columnconfigure(0, weight = 1)

            tkinter.Label(self.title_frame, text = "Új adatok felvitele", bg = self["bg"], font = (None, 24)).grid(row = 0, column = 0, sticky = "NESW")

            self.content_frame = tkinter.Frame(self, bg = self["bg"])
            self.content_frame.grid(row = 1, column = 0, sticky = "NESW")

            self.content_frame.columnconfigure(0, weight = 1)
            self.content_frame.rowconfigure(0, weight = 1)
            self.content_frame.rowconfigure(1, weight = 1)
            self.content_frame.rowconfigure(2, weight = 1)
            self.content_frame.rowconfigure(3, weight = 1)
            self.content_frame.rowconfigure(4, weight = 1)
            self.content_frame.rowconfigure(5, weight = 1)
            self.content_frame.rowconfigure(6, weight = 20)

            tkinter.Label(self.content_frame, text = "Válassza ki a felvinni kívánt adatot!", bg = self["bg"], font = (None, 16)).grid(row = 0, column = 0, sticky = "NESW")

            tkinter.Button(self.content_frame, text = "Új járat", bg = self["bg"], font = (None, 12), command = self.new_route).grid(row = 1, column = 0)
            tkinter.Button(self.content_frame, text = "Új jármű", bg = self["bg"], font = (None, 12), command = self.new_vehicle).grid(row = 2, column = 0)
            tkinter.Button(self.content_frame, text = "Új járműtípus", bg = self["bg"], font = (None, 12), command = self.new_vehicle_type).grid(row = 3, column = 0)
            tkinter.Button(self.content_frame, text = "Új vonal", bg = self["bg"], font = (None, 12), command = self.new_line).grid(row = 4, column = 0)
            tkinter.Button(self.content_frame, text = "Új megálló", bg = self["bg"], font = (None, 12), command = self.new_stop).grid(row = 5, column = 0)



    def new_stop(self):
        def process_new_stop():
            connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
            cursor = connection.cursor()

            try:
                sql = "INSERT INTO megallo(nev, hely) VALUES(%s, %s)"

                data = (self.content_frame.form_frame.stop_name_entry.get().strip(), self.content_frame.form_frame.location_entry.get().strip())

                cursor.execute(sql, params = data)

                connection.commit()

                self.content_frame.form_frame.stop_name_entry.delete(0, "end")
                self.content_frame.form_frame.location_entry.delete(0, "end")

                tkinter.messagebox.showinfo("Siker", "Sikeres adatfelvitel!")

            except mysql.connector.Error as error:
                connection.rollback()
                tkinter.messagebox.showerror("Hiba", "Hiba történt az adatfelvitel során. Kérjük ellenőrizze a beírt adatokat!\n" + str(error))

            finally:
                connection.close()


        self.content_frame.form_frame = tkinter.Frame(self.content_frame, bg = self["bg"])
        self.content_frame.form_frame.grid(row = 6, column = 0, sticky = "NESW")

        self.content_frame.form_frame.columnconfigure(0, weight = 1)
        self.content_frame.form_frame.columnconfigure(1, weight = 9)
        self.content_frame.form_frame.rowconfigure(0, weight = 1)
        self.content_frame.form_frame.rowconfigure(1, weight = 1)

        self.content_frame.form_frame.stop_name_entry = tkinter.Entry(self.content_frame.form_frame)
        self.content_frame.form_frame.location_entry = tkinter.Entry(self.content_frame.form_frame)

        self.content_frame.form_frame.stop_name_entry.grid(column = 1, row = 0, sticky="WE")
        self.content_frame.form_frame.location_entry.grid(column = 1, row = 1, sticky="WE")

        tkinter.Label(self.content_frame.form_frame, text = "Név:", bg = self["bg"]).grid(row = 0, column = 0, sticky = "E")
        tkinter.Label(self.content_frame.form_frame, text = "Hely:", bg = self["bg"]).grid(row = 1, column = 0, sticky = "E")

        tkinter.Button(self.content_frame.form_frame, text = "Felvitel", bg = self["bg"], command = process_new_stop).grid(row = 4, column = 0, columnspan = 2)



    def new_line(self):
        def process_new_line():
            connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
            cursor = connection.cursor()

            try:
                sql = "INSERT INTO vonal VALUES(%s, %s)"

                data = (self.content_frame.form_frame.line_name_entry.get().strip(), self.content_frame.form_frame.length_entry.get().strip())

                cursor.execute(sql, params = data)

                sql = "INSERT INTO jarat VALUES(%s, %s), (%s, %s)"

                cursor.execute(sql, params = (self.content_frame.form_frame.line_name_entry.get().strip(), 0, self.content_frame.form_frame.line_name_entry.get().strip(), 1))

                connection.commit()

                self.content_frame.form_frame.line_name_entry.delete(0, "end")
                self.content_frame.form_frame.length_entry.delete(0, "end")

                tkinter.messagebox.showinfo("Siker", "Sikeres adatfelvitel!")

            except mysql.connector.Error as error:
                connection.rollback()
                tkinter.messagebox.showerror("Hiba", "Hiba történt az adatfelvitel során. Kérjük ellenőrizze a beírt adatokat!\n" + str(error))

            finally:
                connection.close()


        self.content_frame.form_frame = tkinter.Frame(self.content_frame, bg = self["bg"])
        self.content_frame.form_frame.grid(row = 6, column = 0, sticky = "NESW")

        self.content_frame.form_frame.columnconfigure(0, weight = 1)
        self.content_frame.form_frame.columnconfigure(1, weight = 9)
        self.content_frame.form_frame.rowconfigure(0, weight = 1)
        self.content_frame.form_frame.rowconfigure(1, weight = 1)

        self.content_frame.form_frame.line_name_entry = tkinter.Entry(self.content_frame.form_frame)
        self.content_frame.form_frame.length_entry = tkinter.Entry(self.content_frame.form_frame)

        self.content_frame.form_frame.line_name_entry.grid(column = 1, row = 0, sticky="WE")
        self.content_frame.form_frame.length_entry.grid(column = 1, row = 1, sticky="WE")

        tkinter.Label(self.content_frame.form_frame, text = "Vonalnév:", bg = self["bg"]).grid(row = 0, column = 0, sticky = "E")
        tkinter.Label(self.content_frame.form_frame, text = "Hossz:", bg = self["bg"]).grid(row = 1, column = 0, sticky = "E")

        tkinter.Button(self.content_frame.form_frame, text = "Felvitel", bg = self["bg"], command = process_new_line).grid(row = 4, column = 0, columnspan = 2)



    def new_vehicle_type(self):
        def process_new_vehicle_type():
            connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
            cursor = connection.cursor()

            try:
                sql = "INSERT INTO jarmutipus(nev, elektromos) VALUES(%s, %s)"

                data = (self.content_frame.form_frame.name_entry.get().strip(), self.content_frame.form_frame.electric_entry.get().strip())

                cursor.execute(sql, params = data)

                connection.commit()

                self.content_frame.form_frame.name_entry.delete(0, "end")
                self.content_frame.form_frame.electric_entry.delete(0, "end")

                tkinter.messagebox.showinfo("Siker", "Sikeres adatfelvitel!")

            except mysql.connector.Error as error:
                connection.rollback()
                tkinter.messagebox.showerror("Hiba", "Hiba történt az adatfelvitel során. Kérjük ellenőrizze a beírt adatokat!\n" + str(error))

            finally:
                connection.close()

        
        self.content_frame.form_frame = tkinter.Frame(self.content_frame, bg = self["bg"])
        self.content_frame.form_frame.grid(row = 6, column = 0, sticky = "NESW")

        self.content_frame.form_frame.columnconfigure(0, weight = 1)
        self.content_frame.form_frame.columnconfigure(1, weight = 9)
        self.content_frame.form_frame.rowconfigure(0, weight = 1)
        self.content_frame.form_frame.rowconfigure(1, weight = 1)

        self.content_frame.form_frame.name_entry = tkinter.Entry(self.content_frame.form_frame)
        self.content_frame.form_frame.electric_entry = tkinter.Entry(self.content_frame.form_frame)

        self.content_frame.form_frame.name_entry.grid(column = 1, row = 0, sticky="WE")
        self.content_frame.form_frame.electric_entry.grid(column = 1, row = 1, sticky="WE")

        tkinter.Label(self.content_frame.form_frame, text = "Típusnév:", bg = self["bg"]).grid(row = 0, column = 0, sticky = "E")
        tkinter.Label(self.content_frame.form_frame, text = "Elektromos-e:", bg = self["bg"]).grid(row = 1, column = 0, sticky = "E")

        tkinter.Button(self.content_frame.form_frame, text = "Felvitel", bg = self["bg"], command = process_new_vehicle_type).grid(row = 4, column = 0, columnspan = 2)



    def new_vehicle(self):
        def process_new_vehicle():
            connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
            cursor = connection.cursor()

            try:
                sql = "INSERT INTO jarmu(rendszam, alacsony_padlos, tipus_nev, vezetoi_szam) VALUES(%s, %s, %s, %s)"
                data = (self.content_frame.form_frame.license_entry.get().strip(), self.content_frame.form_frame.disabled_friendly_entry.get().strip(), self.content_frame.form_frame.tipus_entry.get().strip(), self.content_frame.form_frame.driver_entry.get().strip())

                cursor.execute(sql, params = data)

                connection.commit()

                self.content_frame.form_frame.license_entry.delete(0, "end")
                self.content_frame.form_frame.disabled_friendly_entry.delete(0, "end")
                self.content_frame.form_frame.tipus_entry.delete(0, "end")
                self.content_frame.form_frame.driver_entry.delete(0, "end")

                tkinter.messagebox.showinfo("Siker", "Sikeres adatfelvitel!")

            except mysql.connector.Error as error:
                connection.rollback()
                tkinter.messagebox.showerror("Hiba", "Hiba történt az adatfelvitel során. Kérjük ellenőrizze a beírt adatokat!\n" + str(error))

            finally:
                connection.close()


        self.content_frame.form_frame = tkinter.Frame(self.content_frame, bg = self["bg"])
        self.content_frame.form_frame.grid(row = 6, column = 0, sticky = "NESW")

        self.content_frame.form_frame.columnconfigure(0, weight = 1)
        self.content_frame.form_frame.columnconfigure(1, weight = 9)
        self.content_frame.form_frame.rowconfigure(0, weight = 1)
        self.content_frame.form_frame.rowconfigure(1, weight = 1)
        self.content_frame.form_frame.rowconfigure(2, weight = 1)
        self.content_frame.form_frame.rowconfigure(3, weight = 1)
        self.content_frame.form_frame.rowconfigure(4, weight = 1)

        self.content_frame.form_frame.license_entry = tkinter.Entry(self.content_frame.form_frame)
        self.content_frame.form_frame.disabled_friendly_entry = tkinter.Entry(self.content_frame.form_frame)
        self.content_frame.form_frame.tipus_entry = tkinter.Entry(self.content_frame.form_frame)
        self.content_frame.form_frame.driver_entry = tkinter.Entry(self.content_frame.form_frame)

        self.content_frame.form_frame.license_entry.grid(column = 1, row = 0, sticky="WE")
        self.content_frame.form_frame.disabled_friendly_entry.grid(column = 1, row = 1, sticky="WE")
        self.content_frame.form_frame.tipus_entry.grid(column = 1, row = 2, sticky="WE")
        self.content_frame.form_frame.driver_entry.grid(column = 1, row = 3, sticky="WE")

        tkinter.Label(self.content_frame.form_frame, text = "Rendszám:", bg = self["bg"]).grid(row = 0, column = 0, sticky = "E")
        tkinter.Label(self.content_frame.form_frame, text = "Alacsony padlós-e:", bg = self["bg"]).grid(row = 1, column = 0, sticky = "E")
        tkinter.Label(self.content_frame.form_frame, text = "Jármű típus:", bg = self["bg"]).grid(row = 2, column = 0, sticky = "E")
        tkinter.Label(self.content_frame.form_frame, text = "Sofőr száma:", bg = self["bg"]).grid(row = 3, column = 0, sticky = "E")

        tkinter.Button(self.content_frame.form_frame, text = "Felvitel", bg = self["bg"], command = process_new_vehicle).grid(row = 4, column = 0, columnspan = 2)

        

    def new_route(self):
        def process_new_route():
            connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
            cursor = connection.cursor()

            line = self.content_frame.form_frame.line_entry.get()

            try:
                sql = "INSERT INTO indul(rendszam, vonal_nev, visszamenet, mikor) VALUES"

                for start in self.content_frame.form_frame.starts_entry.get().split(";"):
                    start = start.split(",")
                    sql += "(\"{}\", \"{}\", {}, \"{}\"),".format(start[1].strip(), line.strip(), start[2].strip(), start[0].strip())

                cursor.execute(sql[:-1])

                sql2 = "INSERT INTO megall(vonal_nev, visszamenet, megallo_id, mikor) VALUES"

                for stop in self.content_frame.form_frame.stops_entry.get().split(";"):
                    stop = stop.split(",")
                    sql2 += "(\"{}\", {}, {}, \"{}\"),".format(line.strip(), stop[2].strip(), stop[1].strip(), stop[0].strip())

                cursor.execute(sql2[:-1])

                connection.commit()

                self.content_frame.form_frame.line_entry.delete(0, "end")
                self.content_frame.form_frame.starts_entry.delete(0, "end")
                self.content_frame.form_frame.stops_entry.delete(0, "end")

                tkinter.messagebox.showinfo("Siker", "Sikeres adatfelvitel!")

            except mysql.connector.Error as error:
                connection.rollback()
                tkinter.messagebox.showerror("Hiba", "Hiba történt az adatfelvitel során. Kérjük ellenőrizze a beírt adatokat!\n" + str(error))

            finally:
                connection.close()


        self.content_frame.form_frame = tkinter.Frame(self.content_frame, bg = self["bg"])
        self.content_frame.form_frame.grid(row = 6, column = 0, sticky = "NESW")

        self.content_frame.form_frame.columnconfigure(0, weight = 1)
        self.content_frame.form_frame.columnconfigure(1, weight = 9)
        self.content_frame.form_frame.rowconfigure(0, weight = 1)
        self.content_frame.form_frame.rowconfigure(1, weight = 1)
        self.content_frame.form_frame.rowconfigure(2, weight = 1)
        self.content_frame.form_frame.rowconfigure(3, weight = 1)

        self.content_frame.form_frame.line_entry = tkinter.Entry(self.content_frame.form_frame)
        self.content_frame.form_frame.starts_entry = tkinter.Entry(self.content_frame.form_frame)
        self.content_frame.form_frame.stops_entry = tkinter.Entry(self.content_frame.form_frame)

        self.content_frame.form_frame.line_entry.grid(column = 1, row = 0, sticky="WE")
        self.content_frame.form_frame.starts_entry.grid(column = 1, row = 1, sticky="WE")
        self.content_frame.form_frame.stops_entry.grid(column = 1, row = 2, sticky="WE")

        tkinter.Label(self.content_frame.form_frame, text = "Vonal száma:", bg = self["bg"]).grid(row = 0, column = 0, sticky = "E")
        tkinter.Label(self.content_frame.form_frame, text = "Indulások (a kívánt formátum: ÓÓ:PP:MM,Rendszám,Visszamenet-e;):", bg = self["bg"]).grid(row = 1, column = 0, sticky = "E")
        tkinter.Label(self.content_frame.form_frame, text = "Megállások (a kívánt formátum: ÓÓ:PP::MM,MegállóID,Visszamenet-e;):", bg = self["bg"]).grid(row = 2, column = 0, sticky = "E")

        tkinter.Button(self.content_frame.form_frame, text = "Felvitel", bg = self["bg"], command = process_new_route).grid(row = 3, column = 0, columnspan = 2)
