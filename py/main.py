import tkinter
import tkinter.messagebox
import mysql.connector




class User:
    def __init__(self, name: str, is_admin: bool):
        self._name = name
        self._is_admin = is_admin

    
    @property
    def name(self):
        return self._name

    @property
    def is_admin(self):
        return self._is_admin




class Route:
    def __init__(self, name: str, is_returning: bool, type: str, dep_time):
        self._name = name
        self._is_returning = is_returning
        self.type = type
        self._dep_time = dep_time

    
    @property
    def name(self):
        return self._name

    @property
    def is_returning(self):
        return self._is_returning

    @property
    def departure(self):
        return self._dep_time




class Stop:
    def __init__(self, name: str, location: str):
        self._name = name
        self._location = location

    
    @property
    def name(self):
        return self._name

    @property
    def location(self):
        return self._location




class ContentPage(tkinter.Frame):
    def __init__(self, data, *args, **kwargs):
        tkinter.Frame.__init__(self, *args, **kwargs)
        self.data = data




class Home(ContentPage):
    def __init__(self, data, *args, **kwargs):
        ContentPage.__init__(self, data, *args, **kwargs)

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

            tkinter.Button(self.content_frame, text = "Bejelentkezés", font = (None, 12), bg = self["bg"], command = lambda: self.master.load_new_page("LoginPage", None)).grid(row = 0, column = 0, sticky = "S")
            tkinter.Button(self.content_frame, text = "Regisztráció", font = (None, 12), bg = self["bg"], command = lambda: self.master.load_new_page("RegisterPage", None)).grid(row = 1, column = 0, sticky = "N")

        else:
            tkinter.Label(self.title_frame, text = "Üdvözöljük, " + self.master.user.name + "!", font = (None, 24), bg = self["bg"]).grid(row = 0, column = 0, sticky = "NESW")

            tkinter.Button(self.title_frame, text = "Kijelentkezés", font = (None, 12), bg = self["bg"], command = self.logout).grid(row = 1, column = 0)

            if self.master.user.is_admin:
                self.content_frame.columnconfigure(0, weight = 1)
                self.content_frame.rowconfigure(0, weight = 1)
                self.content_frame.rowconfigure(1, weight = 1)

                tkinter.Button(self.content_frame, text = "Adatok felvitele", font = (None, 12), bg = self["bg"], command = lambda: self.master.load_new_page("DataInsertPage", None)).grid(row = 0, column = 0)
                tkinter.Button(self.content_frame, text = "Adatok módosítása", font = (None, 12), bg = self["bg"], command = lambda: self.master.load_new_page("DataUpdatePage", None)).grid(row = 1, column = 0)


    def logout(self):
        self.master.user = None
        self.master.reload_existing_pages()

    

class DataInsertPage(ContentPage):
    def __init__(self, data, *args, **kwargs):
        ContentPage.__init__(self, data, *args, **kwargs)

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
            connection = mysql.connector.connect(host = dbhost, database = dbname, user = dbuser, password = dbpwd)
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
            connection = mysql.connector.connect(host = dbhost, database = dbname, user = dbuser, password = dbpwd)
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
            connection = mysql.connector.connect(host = dbhost, database = dbname, user = dbuser, password = dbpwd)
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
            connection = mysql.connector.connect(host = dbhost, database = dbname, user = dbuser, password = dbpwd)
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
            connection = mysql.connector.connect(host = dbhost, database = dbname, user = dbuser, password = dbpwd)
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

        

        
class SearchResults(ContentPage):
    def __init__(self, data, *args, **kwargs):
        ContentPage.__init__(self, data, *args, **kwargs)

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 9)

        title_frame = tkinter.Frame(master = self, bg = self["bg"])
        title_frame.grid(row = 0, sticky = "NESW")

        title_frame.rowconfigure(0, weight = 1)
        title_frame.columnconfigure(0, weight = 1)

        tkinter.Label(master = title_frame, text = data["from"].capitalize() + " - " + data["to"].capitalize(), font = (None, 24), bg = self["bg"]).grid(row = 0, column = 0, sticky = "NESW")
    

        result_frame = tkinter.Frame(master = self, bg = self["bg"])
        result_frame.grid(row = 1, sticky = "NESW")

        result_frame.columnconfigure(0, weight = 4)
        result_frame.columnconfigure(1, weight = 4)
        result_frame.columnconfigure(2, weight = 4)
        result_frame.columnconfigure(3, weight = 1)

        grid_row_count = 0
        for route_id, datalist in data["results"].items():
            for data in datalist:
                route = Route(route_id, data[0], data[3], data[1])

                tkinter.Label(result_frame, text = route.name, font = (None, 12), bg = "LightSkyBlue2").grid(row = grid_row_count, column = 0, sticky = "NESW")
                tkinter.Label(result_frame, text = route.type, font = (None, 12), bg = "LightSkyBlue2").grid(row = grid_row_count, column = 1, sticky = "NESW")
                tkinter.Label(result_frame, text = route.departure + data[2], font = (None, 12), bg = "LightSkyBlue2").grid(row = grid_row_count, column = 2, sticky = "NESW")
                tkinter.Button(result_frame, text = "Részletek", command = lambda route = route: self.route_details(route), bg = "dark slate blue", fg = "snow").grid(row = grid_row_count, column = 3, sticky = "NESW")

                grid_row_count += 1

    
    def route_details(self, route: Route):
        connection = mysql.connector.connect(host = dbhost, database = dbname, user = dbuser, password = dbpwd)
        cursor = connection.cursor()

        sql = '''select megallo.nev, megallo.hely, addtime(megall.mikor, indul.mikor) from megall
                inner join megallo on megall.megallo_id = megallo.id
                inner join indul on megall.visszamenet = indul.visszamenet and megall.vonal_nev = indul.vonal_nev
                where megall.vonal_nev = %s and megall.visszamenet = %s and indul.mikor = %s
                order by addtime(indul.mikor, megall.mikor)'''

        cursor.execute(operation = sql, params = (route.name, route.is_returning, route.departure))

        data = {"route": route, "stops": list()}

        for row in cursor.fetchall():
            data["stops"].append((Stop(row[0], row[1]), row[2]))

        connection.close()

        self.master.load_new_page("RouteResults", data)

    
    def refresh(self):
        pass




class RouteResults(ContentPage):
    def __init__(self, data, *args, **kwargs):
        ContentPage.__init__(self, data, *args, **kwargs)

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 9)


        title_frame = tkinter.Frame(self, bg = self["bg"])
        title_frame.grid(row = 0, column = 0, sticky = "NESW")

        title_frame.rowconfigure(0, weight = 1)
        title_frame.columnconfigure(0, weight = 1)

        tkinter.Label(title_frame, text = data["route"].name + " jelzésű " + data["route"].type, font = (None, 24), bg = self["bg"]).grid(row = 0, sticky = "NESW")

        result_frame = tkinter.Frame(self, bg = self["bg"])
        result_frame.grid(row = 1, sticky = "NESW")

        result_frame.columnconfigure(0, weight = 4)
        result_frame.columnconfigure(1, weight = 4)
        result_frame.columnconfigure(2, weight = 4)
        result_frame.columnconfigure(3, weight = 1)

        grid_row_count = 0
        for stop, time in data["stops"]:
            tkinter.Label(result_frame, text = time, font = (None, 12)).grid(row = grid_row_count, column = 0, sticky = "NESW")
            tkinter.Label(result_frame, text = stop.name, font = (None, 12)).grid(row = grid_row_count, column = 1, sticky = "NESW")
            tkinter.Label(result_frame, text = stop.location, font = (None, 12)).grid(row = grid_row_count, column = 2, sticky = "NESW")
            tkinter.Button(result_frame, text = "Részletek", font = (None, 12), command = lambda stop = stop: self.stop_details(stop)).grid(row = grid_row_count, column = 3, sticky = "NESW")

            grid_row_count += 1


    def stop_details(self, stop: Stop):
        connection = mysql.connector.connect(host = dbhost, database = dbname, user = dbuser, password = dbpwd)
        cursor = connection.cursor()

        giga_sql = '''select alkerdes2.vonal, alkerdes2.visszamenet, tipus_nev, indul.mikor, alkerdes2.erkezik_vizsgalt_megallohoz, alkerdes2.megallo_nev from
                    (select alkerdes.vonal, alkerdes.visszamenet, alkerdes.mikor as erkezik_vizsgalt_megallohoz, menetrend.mikor as erkezik_megallohoz, menetrend.megallo_nev from
                    (select menetrend.vonal, menetrend.visszamenet, menetrend.mikor from menetrend
                    where lower(menetrend.megallo_nev) = %s) as alkerdes
                    inner join menetrend on alkerdes.vonal = menetrend.vonal and alkerdes.visszamenet = menetrend.visszamenet) as alkerdes2
                    inner join indul on alkerdes2.vonal = indul.vonal_nev and alkerdes2.visszamenet = indul.visszamenet
                    inner join jarmu on jarmu.rendszam = indul.rendszam
                    where alkerdes2.erkezik_megallohoz = (select max(menetrend2.mikor) from menetrend as menetrend2 where menetrend2.vonal = alkerdes2.vonal)
                    order by addtime(alkerdes2.erkezik_vizsgalt_megallohoz, indul.mikor)'''

        cursor.execute(operation = giga_sql, params = (stop.name,))

        data = {"stop": stop, "routes": list()}

        for row in cursor.fetchall():
            data["routes"].append({"route": Route(row[0], row[1], row[2], row[3]), "misc": (row[4], row[5])})

        connection.close()

        self.master.load_new_page("StopDetails", data)

    
    def refresh(self):
        pass




class StopDetails(ContentPage):
    def __init__(self, data, *args, **kwargs):
        ContentPage.__init__(self, data, *args, **kwargs)

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 9)

        title_frame = tkinter.Frame(self, bg = self["bg"])
        title_frame.grid(row = 0, column = 0, sticky = "NESW")

        title_frame.rowconfigure(0, weight = 3)
        title_frame.rowconfigure(1, weight = 1)
        title_frame.columnconfigure(0, weight = 1)

        tkinter.Label(title_frame, text = data["stop"].name, font = (None, 24), bg = self["bg"]).grid(row = 0, sticky = "NESW")
        tkinter.Label(title_frame, text = data["stop"].location, font = (None, 20), bg = self["bg"]).grid(row = 1, sticky = "NESW")

        results_frame = tkinter.Frame(self, bg = self["bg"])
        results_frame.grid(row = 1, sticky = "NESW")

        results_frame.columnconfigure(0, weight = 1)
        results_frame.columnconfigure(1, weight = 1)
        results_frame.columnconfigure(2, weight = 1)
        results_frame.columnconfigure(3, weight = 1)


        grid_row_count = 0
        for elem in data["routes"]:
           tkinter.Label(results_frame, text = elem["route"].name + " jelzésű " + elem["route"].type, font = (None, 12)).grid(row = grid_row_count, column = 0, sticky = "NESW")
           tkinter.Label(results_frame, text = elem["misc"][1].capitalize() + " felé", font = (None, 12)).grid(row = grid_row_count, column = 1, sticky = "NESW")
           tkinter.Label(results_frame, text = elem["route"].departure + elem["misc"][0], font = (None, 12)).grid(row = grid_row_count, column = 2, sticky = "NESW")
           tkinter.Button(results_frame, text = "Részletek", font = (None, 12), command = lambda route = elem["route"]: self.route_details(route)).grid(row = grid_row_count, column = 3, sticky = "NESW")

           grid_row_count += 1


    def route_details(self, route):
        connection = mysql.connector.connect(host = dbhost, database = dbname, user = dbuser, password = dbpwd)
        cursor = connection.cursor()

        sql = '''select megallo.nev, megallo.hely, addtime(megall.mikor, indul.mikor) from megall
                inner join megallo on megall.megallo_id = megallo.id
                inner join indul on megall.visszamenet = indul.visszamenet and megall.vonal_nev = indul.vonal_nev
                where megall.vonal_nev = %s and megall.visszamenet = %s and indul.mikor = %s
                order by addtime(indul.mikor, megall.mikor)'''

        cursor.execute(operation = sql, params = (route.name, route.is_returning, route.departure))

        data = {"route": route, "stops": list()}

        for row in cursor.fetchall():
            data["stops"].append((Stop(row[0], row[1]), row[2]))

        connection.close()

        self.master.load_new_page("RouteResults", data)


    def refresh(self):
        pass





class RegisterPage(ContentPage):
    def __init__(self, data, *args, **kwargs):
        ContentPage.__init__(self, data, *args, **kwargs)

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 1)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)

        self.title_text = tkinter.Label(self, text = "Regisztráció", font = (None, 24), bg = self["bg"])
        self.title_text.grid(row = 0, column = 0, columnspan = 2)
        
        self.username_entry = tkinter.Entry(self, bg = self["bg"])
        self.password_entry = tkinter.Entry(self, bg = self["bg"], show = "*")
        self.password_confirm_entry = tkinter.Entry(self, bg = self["bg"], show = "*")
        self.email_entry = tkinter.Entry(self, bg = self["bg"])

        self.username_entry.grid(row = 1, column = 1, sticky = "W")
        self.password_entry.grid(row = 2, column = 1, sticky = "W")
        self.password_confirm_entry.grid(row = 3, column = 1, sticky = "W")
        self.email_entry.grid(row = 4, column = 1, sticky = "W")

        self.username_label = tkinter.Label(self, text = "Felhasználónév:", bg = self["bg"])
        self.password_label = tkinter.Label(self, text = "Jelszó:", bg = self["bg"])
        self.password_confirm_label = tkinter.Label(self, text = "Jelszó még egyszer:", bg = self["bg"])
        self.email_label = tkinter.Label(self, text = "E-mail cím:", bg = self["bg"])

        self.username_label.grid(row = 1, column = 0, sticky = "E")
        self.password_label.grid(row = 2, column = 0, sticky = "E")
        self.password_confirm_label.grid(row = 3, column = 0, sticky = "E")
        self.email_label.grid(row = 4, column = 0, sticky = "E")

        self.register_button = tkinter.Button(self, text = "Regisztráció", command = self.register, bg = self["bg"])
        self.register_button.grid(row = 5, column = 0, columnspan = 2)


    def register(self):
        connection = mysql.connector.connect(host = dbhost, database = dbname, user = dbuser, password = dbpwd)
        cursor = connection.cursor()

        cursor.execute("select * from user where username = %s", params = (self.username_entry.get(),))

        if cursor.fetchall():
            tkinter.messagebox.showerror("Hiba", "A felhasználónév már foglalt!")
        elif self.password_entry.get() != self.password_confirm_entry.get():
            tkinter.messagebox.showerror("Hiba", "A megadott jelszavak nem egyeznek!")

        else:
            cursor.execute("INSERT INTO user(username, password, email) VALUES(%s, %s, %s)", params = (self.username_entry.get(), self.password_entry.get(), self.email_entry.get()))
            connection.commit()

            self.master.user = User(self.username_entry.get(), False)

            self.username_entry.delete(0, "end")
            self.password_entry.delete(0, "end")
            self.password_confirm_entry.delete(0, "end")
            self.email_entry.delete(0, "end")

            tkinter.messagebox.showinfo("Siker", "Sikeres regisztráció!")

        connection.close()

    
    def refresh(self):
        pass
        



class LoginPage(ContentPage):
    def __init__(self, data, *args, **kwargs):
        ContentPage.__init__(self, data, *args, **kwargs)

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)

        self.title_text = tkinter.Label(self, text = "Bejelentkezés", font = (None, 24), bg = self["bg"])
        self.title_text.grid(row = 0, column = 0, columnspan = 2)

        self.username_entry = tkinter.Entry(self, bg = self["bg"])
        self.password_entry = tkinter.Entry(self, bg = self["bg"], show = "*")

        self.username_entry.grid(row = 1, column = 1, sticky = "SW")
        self.password_entry.grid(row = 2, column = 1, sticky = "NW")

        self.username_label = tkinter.Label(self, text = "Felhasználónév:", bg = self["bg"])
        self.password_label = tkinter.Label(self, text = "Jelszó:", bg = self["bg"])

        self.username_label.grid(row = 1, column = 0, sticky = "SE")
        self.password_label.grid(row = 2, column = 0, sticky = "NE")

        self.login_button = tkinter.Button(self, text = "Bejelentkezés", command = self.login, bg = self["bg"])
        self.login_button.grid(row = 3, column = 0, columnspan = 2)


    def login(self):
        if self.username_entry.get() == "" or self.password_entry == "":
            tkinter.messagebox.showwarning("Figyelem", "Kérem adja meg a felhasználónevét és jelszavát is!")

        else:
            connection = mysql.connector.connect(host = dbhost, database = dbname, user = dbuser, password = dbpwd)
            cursor = connection.cursor()

            cursor.execute("select username, password, admin from user where username = %s", params = (self.username_entry.get(),))

            user = cursor.fetchone()

            if user is None:
                tkinter.messagebox.showerror("Hiba", "Hibás felhasználónév!")
            elif user[1] != self.password_entry.get():
                tkinter.messagebox.showerror("Hiba", "Hibás jelszó!")
            else:
                self.master.user = User(user[0], user[2])

                self.username_entry.delete(0, "end")
                self.password_entry.delete(0, "end")

                self.master.reload_existing_pages()
                self.master.load_new_page("Home", None)

                tkinter.messagebox.showinfo("Siker", "Sikeres bejelentkezés!")

            connection.close()


    def refresh(self):
        pass




class Header(tkinter.Frame):
    def __init__(self, *args, **kwargs):
        tkinter.Frame.__init__(self, *args, **kwargs)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 2)
        self.columnconfigure(3, weight = 4)
        self.columnconfigure(4, weight = 2)
        self.columnconfigure(5, weight = 4)
        self.columnconfigure(6, weight = 1)
        self.columnconfigure(7, weight = 1)


        self._backbutton = tkinter.Button(self, text = "Vissza", command = self.master.load_previous_page, bg = "DarkOliveGreen3")
        self._backbutton.grid(row = 0, column = 0, sticky = "NESW")

        self._nextbutton = tkinter.Button(self, text = "Előre", command = self.master.load_next_page, bg = "DarkOliveGreen3")
        self._nextbutton.grid(row = 0, column = 1, sticky = "NESW")

        self.from_stop_label = tkinter.Label(self, text = "Honnan:", bg = self["bg"], fg = "snow", font = (None, 10))
        self.from_stop_label.grid(row = 0, column = 2, sticky = "E")

        self.from_stop = tkinter.Entry(self)
        self.from_stop.grid(row = 0, column = 3, sticky = "W")

        self.to_stop_label = tkinter.Label(self, text = "Hová:", bg = self["bg"], fg = "snow", font = (None, 10))
        self.to_stop_label.grid(row = 0, column = 4, sticky = "E")

        self.to_stop = tkinter.Entry(self)
        self.to_stop.grid(row = 0, column = 5, sticky = "W")

        self.search_button = tkinter.Button(self, text = "Keresés", command = self.search, bg = "thistle3")
        self.search_button.grid(row = 0, column = 6)

        self.home_button = tkinter.Button(self, text = "Főoldal", command = lambda: self.master.load_new_page("Home", None), bg = "DarkOliveGreen3")
        self.home_button.grid(row = 0, column = 7)

    
    @property
    def backbutton(self):
        return self._backbutton

    @property
    def nextbutton(self):
        return self._nextbutton


    def search(self):
        from_stop = self.from_stop.get().strip()
        to_stop = self.to_stop.get().strip()

        if from_stop == "" or to_stop == "":
            tkinter.messagebox.showwarning(title = "Figyelem!", message = "Kérem adja meg az indulási- és célállomását!")

        else:
            connection = mysql.connector.connect(host = dbhost, database = dbname, user = dbuser, password = dbpwd)
            cursor = connection.cursor()

            monster_sql = '''select indul.vonal_nev, indul.visszamenet, indul.mikor, alkerdes3.mikor, jarmu.tipus_nev from indul
                    inner join jarmu on jarmu.rendszam = indul.rendszam
                    inner join (select menetrend.vonal, menetrend.visszamenet, menetrend.mikor from menetrend
                    inner join (select vonal, visszamenet, mikor from menetrend where megallo_nev = %s) as alkerdes1 on alkerdes1.vonal = menetrend.vonal and menetrend.visszamenet = alkerdes1.visszamenet
                    inner join (select vonal, visszamenet, mikor from menetrend where megallo_nev = %s) as alkerdes2 on alkerdes2.vonal = menetrend.vonal and menetrend.visszamenet = alkerdes2.visszamenet
                    where megallo_nev = %s
                    and menetrend.vonal in (select DISTINCT vonal from menetrend where megallo_nev = %s)
                    and alkerdes1.mikor < alkerdes2.mikor) as alkerdes3 on alkerdes3.vonal = indul.vonal_nev and alkerdes3.visszamenet = indul.visszamenet
                    order by addtime(indul.mikor, alkerdes3.mikor)'''

            cursor.execute(operation = monster_sql, params = (from_stop, to_stop, from_stop, to_stop))
            rows = cursor.fetchall()

            if not rows:
                tkinter.messagebox.showerror(title = "Hiba", message = "Ezen az útvonalon nem jár egy járat sem!")

            else:
                data = {"from": from_stop, "to": to_stop, "results": dict()}

                for row in rows:
                    if row[0] not in data["results"]:
                        data["results"][row[0]] = list()
                    data["results"][row[0]].append((row[1], row[2], row[3], row[4]))

                self.master.load_new_page("SearchResults", data)

            connection.close()

            self.from_stop.delete(0, "end")
            self.to_stop.delete(0, "end")




class App(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.geometry("640x360")
        self.title("Városi Tömegközlekedés")

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 2)
        self.rowconfigure(1, weight = 98)

        self.user = None

        self.header = Header(self, bg = "slate blue")
        self.header.grid(row = 0, sticky = "NESW")

        self.content_pages = ["Home", "LoginPage", "RegisterPage", "SearchResults", "RouteResults", "StopDetails", "DataInsertPage", "DataUpdatePage"]
        self.loaded_pages = list()

        self.current_page = None
        self.load_new_page("Home", None)

        self.header.backbutton["state"] = "disabled"
        self.header.nextbutton["state"] = "disabled"

        
    def load_new_page(self, page: str, data: dict):
        if page in self.content_pages:
            if self.current_page is not None and self.loaded_pages.index(self.current_page) != len(self.loaded_pages) - 1:
                del self.loaded_pages[self.loaded_pages.index(self.current_page) + 1:]

            self.current_page = globals()[page](data, self, bg = "snow")
            self.current_page.grid(row = 1, sticky = "NESW")
            self.loaded_pages.append(self.current_page)

            self.header.backbutton["state"] = "normal"
            self.header.nextbutton["state"] = "disabled"

    
    def load_previous_page(self):
        current_index = self.loaded_pages.index(self.current_page)

        if current_index - 1 >= 0:
            self.current_page = self.loaded_pages[current_index - 1]
            self.current_page.tkraise()

            self.header.backbutton["state"] = "disabled" if current_index - 1 == 0 else "normal"
            self.header.nextbutton["state"] = "normal"


    def load_next_page(self):
        current_index = self.loaded_pages.index(self.current_page)

        if current_index + 1 < len(self.loaded_pages):
            self.current_page = self.loaded_pages[current_index + 1]
            self.current_page.tkraise()

            self.header.backbutton["state"] = "normal"
            self.header.nextbutton["state"] = "disabled" if current_index + 1 == len(self.loaded_pages) - 1 else "normal"


    def reload_existing_pages(self):
        for page in self.loaded_pages:
            page.refresh()




if __name__ == "__main__":
    dbhost = "localhost"
    dbname = "varosi_tomegkozlekedes"
    dbuser = "root"
    dbpwd = ""

    App().mainloop()