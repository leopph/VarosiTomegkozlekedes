import tkinter
import tkinter.ttk
import tkinter.messagebox
import ContentPage
import mysql.connector


class DataDeletePage(ContentPage.ContentPage):
    def __init__(self, data, *args, **kwargs) -> None:
        ContentPage.ContentPage.__init__(self, data, *args, **kwargs)

        self.title_frame = None
        self.content_frame = None

        self.refresh()



    def refresh(self):
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

            self.title_frame = tkinter.Frame(self, bg = self["bg"])
            self.title_frame.grid(column = 0, row = 0, sticky = "NESW")

            self.title_frame.columnconfigure(0, weight = 1)

            tkinter.Label(self.title_frame, text="Adatok törlése", bg=self["bg"], font=("", 26)).grid(column=0, row=0, sticky="NESW")
            tkinter.Label(self.title_frame, text="Válassza ki a törölni kívánt adatot", bg=self["bg"], font=("", 22)).grid(column=0, row=1, sticky="NESW")

            self.content_frame = tkinter.Frame(self, bg = self["bg"])
            self.content_frame.grid(row = 1, column = 0, sticky = "NESW")

            self.content_frame.columnconfigure(0, weight = 1)
            self.content_frame.columnconfigure(5, weight = 1)

            tkinter.ttk.Button(self.content_frame, text = "Vonal törlése", command = self.delete_line).grid(row = 0, column = 0, sticky="E")
            tkinter.ttk.Button(self.content_frame, text = "Megálló törlése", command = self.delete_stop).grid(row = 0, column = 1)
            tkinter.ttk.Button(self.content_frame, text = "Vezető törlése", command = self.delete_driver).grid(row = 0, column = 2)
            tkinter.ttk.Button(self.content_frame, text = "Járműtípus törlése", command = self.delete_vehicle_type).grid(row = 0, column = 3)
            tkinter.ttk.Button(self.content_frame, text = "Jármű törlése", command = self.delete_vehicle).grid(row = 0, column = 4)
            tkinter.ttk.Button(self.content_frame, text = "Járat törlése", command = self.delete_route).grid(row = 0, column = 5, sticky="W")

            self.form_frame = tkinter.Frame(self.content_frame, bg = self["bg"])
            self.form_frame.grid(row = 1, column = 0, columnspan=6, sticky = "NESW")


    def delete_driver(self):
        def process_transaction():
            connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
            cursor = connection.cursor()
            sql = "DELETE FROM vezeto WHERE vezetoi_szam = %s"

            try:
                cursor.execute(sql, (drivers[driver.get()],))
                connection.commit()

                tkinter.messagebox.showinfo("Siker", "Sikeres törlés!")

                for child in self.form_frame.winfo_children():
                    child.destroy()

            except mysql.connector.Error as error:
                connection.rollback()
                tkinter.messagebox.showerror("Hiba", "Hiba történt az adattörlés során.\n" + str(error))

            finally:
                connection.close()
        

        connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
        cursor = connection.cursor()
        sql = "SELECT vezetoi_szam, vezeteknev, keresztnev FROM vezeto"
        cursor.execute(sql)
        drivers: dict[str, str] = {str(driver[0]) + " (" + str(driver[1]) + " " + str(driver[2]) + ")": driver[0] for driver in cursor.fetchall()}
        connection.close()

        for child in self.form_frame.winfo_children():
            child.destroy()

        self.form_frame.columnconfigure(index=0, weight=1)
        self.form_frame.columnconfigure(index=1, weight=1)

        driver = tkinter.StringVar(self.form_frame)
        driver.set(sorted(drivers.keys())[0])

        tkinter.Label(master=self.form_frame, text="Vezetői szám:", bg=self["bg"]).grid(row=0, column=0, sticky="E")
        tkinter.ttk.OptionMenu(self.form_frame, driver, driver.get(), *drivers).grid(row=0, column=1, sticky="W")
        tkinter.ttk.Button(master=self.form_frame, text="Törlés", command=process_transaction).grid(row=1, column=0, columnspan=2)


    def delete_vehicle(self):
        def process_transaction():
            connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
            cursor = connection.cursor()

            try:
                sql = "DELETE FROM jarmu WHERE rendszam = %s"
                cursor.execute(sql, params = (license.get(),))
                connection.commit()

                license_drop_down["menu"].delete(licenses.index(license.get()))
                licenses.remove(license.get())
                license.set(licenses[0])

                tkinter.messagebox.showinfo("Siker", "Sikeres törlés!")

                for child in self.form_frame.winfo_children():
                    child.destroy()

            except mysql.connector.Error as error:
                connection.rollback()
                tkinter.messagebox.showerror("Hiba", "Hiba történt az adattörlés során.\n" + str(error))

            finally:
                connection.close()


        def get_foreign_key_entries():
            connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
            cursor = connection.cursor()

            sql = "SELECT rendszam FROM jarmu"
            cursor.execute(sql)

            ret = [license[0] for license in cursor.fetchall()]

            connection.close()

            return ret


        for child in self.form_frame.winfo_children():
            child.destroy()

        self.form_frame.columnconfigure(index=0, weight=1)
        self.form_frame.columnconfigure(index=1, weight=1)
        
        licenses = get_foreign_key_entries()
        license = tkinter.StringVar(self.form_frame)
        license.set(licenses[0])
        license_drop_down = tkinter.ttk.OptionMenu(self.form_frame, license, license.get(), *licenses)
        license_drop_down.grid(row = 0, column = 1, sticky="W")

        tkinter.Label(self.form_frame, text = "Rendszám:", bg=self["bg"]).grid(row = 0, column = 0, sticky="E")
        tkinter.ttk.Button(self.form_frame, text = "Törlés", command = process_transaction).grid(row = 1, column = 0, columnspan = 2)

    
    def delete_vehicle_type(self):
        def process_transaction():
            connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
            cursor = connection.cursor()

            try:
                sql = "DELETE FROM jarmutipus WHERE nev = %s"
                cursor.execute(sql, params = (type_.get(),))
                connection.commit()

                type_drop_down["menu"].delete(types.index(type_.get()))
                types.remove(type_.get())
                type_.set(types[0])

                tkinter.messagebox.showinfo("Siker", "Sikeres törlés!")

                for child in self.form_frame.winfo_children():
                    child.destroy()

            except mysql.connector.Error as error:
                connection.rollback()
                tkinter.messagebox.showerror("Hiba", "Hiba történt az adattörlés során.\n" + str(error))

            finally:
                connection.close() 

        def get_foreign_key_entries():
            connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
            cursor = connection.cursor()

            sql = "SELECT nev FROM jarmutipus"
            cursor.execute(sql)

            ret = [type_name[0] for type_name in cursor.fetchall()]

            connection.close()

            return ret

        for child in self.form_frame.winfo_children():
            child.destroy()

        self.form_frame.columnconfigure(index=0, weight=1)
        self.form_frame.columnconfigure(index=1, weight=1)

        types = get_foreign_key_entries()
        type_ = tkinter.StringVar(self.form_frame)
        type_.set(types[0])
        type_drop_down = tkinter.ttk.OptionMenu(self.form_frame, type_, type_.get(), *types)
        type_drop_down.grid(row = 0, column = 1, sticky="W")

        tkinter.Label(self.form_frame, text = "Típusnév:", bg=self["bg"]).grid(row = 0, column = 0, sticky="E")
        tkinter.ttk.Button(self.form_frame, text = "Törlés", command = process_transaction).grid(row = 1, column = 0, columnspan = 2)


    def delete_line(self):
        def process_transaction():
            connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
            cursor = connection.cursor()

            try:
                sql = "DELETE FROM vonal WHERE nev = %s"
                cursor.execute(sql, (line.get(),))
                connection.commit()

                line_drop_down["menu"].delete(lines.index(line.get()))
                lines.remove(line.get())
                line.set(lines[0])

                tkinter.messagebox.showinfo("Siker", "Sikeres törlés!")

                for child in self.form_frame.winfo_children():
                    child.destroy()

            except mysql.connector.Error as error:
                connection.rollback()
                tkinter.messagebox.showerror("Hiba", "Hiba történt az adattörlés során.\n" + str(error))

            finally:
                connection.close() 

        def get_foreign_key_entries():
            connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
            cursor = connection.cursor()

            sql = "SELECT nev FROM vonal"
            cursor.execute(sql)

            ret = [line_name[0] for line_name in cursor.fetchall()]
            
            connection.close()

            return ret

        for child in self.form_frame.winfo_children():
            child.destroy()

        self.form_frame.columnconfigure(index=0, weight=1)
        self.form_frame.columnconfigure(index=1, weight=1)

        lines = get_foreign_key_entries()
        line = tkinter.StringVar(self.form_frame)
        line.set(lines[0])
        line_drop_down = tkinter.ttk.OptionMenu(self.form_frame, line, line.get(), *lines)
        line_drop_down.grid(row = 0, column = 1, sticky="W")

        tkinter.Label(self.form_frame, text = "Vonalnév:", bg=self["bg"]).grid(row = 0, column = 0, sticky="E")
        tkinter.ttk.Button(self.form_frame, text = "Törlés", command = process_transaction).grid(row = 1, column = 0, columnspan = 2)


    def delete_stop(self):
        def process_transaction():
            connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
            cursor = connection.cursor()

            try:
                sql = "DELETE FROM megallo WHERE id = %s"
                cursor.execute(sql, (stops[stop.get()],))
                connection.commit()

                stop_drop_down["menu"].delete(stop.get())
                del stops[stop.get()]
                stop.set(sorted(stops.keys())[0])

                tkinter.messagebox.showinfo("Siker", "Sikeres törlés!")

                for child in self.form_frame.winfo_children():
                    child.destroy()

            except mysql.connector.Error as error:
                connection.rollback()
                tkinter.messagebox.showerror("Hiba", "Hiba történt az adattörlés során.\n" + str(error))

            finally:
                connection.close()

        def get_foreign_key_entries():
            connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
            cursor = connection.cursor()

            sql = "SELECT id, nev FROM megallo"
            cursor.execute(sql)

            ret = {str(stop_id[0]) + " (" + stop_id[1] + ")": stop_id[0] for stop_id in cursor.fetchall()}
            
            connection.close()

            return ret


        for child in self.form_frame.winfo_children():
            child.destroy()

        self.form_frame.columnconfigure(index=0, weight=1)
        self.form_frame.columnconfigure(index=1, weight=1)

        stops = get_foreign_key_entries()
        stop = tkinter.StringVar(self.form_frame)
        stop.set(sorted(stops.keys())[0])
        stop_drop_down = tkinter.ttk.OptionMenu(self.form_frame, stop, stop.get(), *stops.keys())
        stop_drop_down.grid(row = 0, column = 1, sticky="W")

        tkinter.Label(self.form_frame, text = "Megálló ID:", bg=self["bg"]).grid(row = 0, column = 0, sticky="E")
        tkinter.ttk.Button(self.form_frame, text = "Törlés", command = process_transaction).grid(row = 1, column = 0, columnspan = 2)


    def delete_route(self):
        def process_transaction():
            connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
            cursor = connection.cursor()

            try:
                sql = "DELETE FROM jarat WHERE vonal_nev = %s and visszamenet = %s"
                cursor.execute(sql, (routes[route.get()][0], routes[route.get()][1],))
                connection.commit()

                if cursor.rowcount != 0:
                    tkinter.messagebox.showinfo("Siker", "Sikeres törlés!")

                    for child in self.form_frame.winfo_children():
                        child.destroy()

                else:
                    tkinter.messagebox.showerror("Hiba", "Ilyen járat már nincs az adatbázisban!")

            except mysql.connector.Error as error:
                connection.rollback()
                tkinter.messagebox.showerror("Hiba", "Hiba történt az adattörlés során.\n" + str(error))

            finally:
                connection.close()

        def get_foreign_key_entries():
            connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
            cursor = connection.cursor()

            sql = "SELECT vonal_nev, visszamenet FROM jarat"
            cursor.execute(sql)

            ret: dict[str, tuple[str, bool]] = {route[0] + " (" + str("visszamenet" if route[1] else "odamenet") + ")": (route[0], route[1]) for route in cursor.fetchall()}
            
            connection.close()

            return ret

        for child in self.form_frame.winfo_children():
            child.destroy()

        self.form_frame.columnconfigure(index=0, weight=1)
        self.form_frame.columnconfigure(index=1, weight=1)

        routes = get_foreign_key_entries()
        route = tkinter.StringVar(self.form_frame)
        route.set(sorted(routes.keys())[0])
        route_drop_down = tkinter.ttk.OptionMenu(self.form_frame, route, route.get(), *routes)
        route_drop_down.grid(row = 0, column = 1, sticky="W")

        tkinter.Label(self.form_frame, text = "Járat:", bg=self["bg"]).grid(row = 0, column = 0, sticky="E")
        tkinter.ttk.Button(self.form_frame, text = "Törlés", command = process_transaction).grid(row = 2, column = 0, columnspan = 2)
