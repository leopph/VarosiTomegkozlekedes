import ContentPage
import tkinter
import Entity
import mysql.connector
import StopDetails




class RouteResults(ContentPage.ContentPage):
    def __init__(self, data, *args, **kwargs) -> None:
        ContentPage.ContentPage.__init__(self, data, *args, **kwargs)

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 9)

        self.refresh()


    def stop_details(self, stop: Entity.Stop) -> None:
        connection = mysql.connector.connect(host = self.master.dbhost, database = self.master.dbname, user = self.master.dbuser, password = self.master.dbpwd)
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
            data["routes"].append({"route": Entity.Route(row[0], row[1], row[2], row[3]), "misc": (row[4], row[5])})

        connection.close()

        self.master.load_new_page(StopDetails.StopDetails, data)

    
    def refresh(self) -> None:
        for child in self.winfo_children():
            child.destroy()

        title_frame = tkinter.Frame(self, bg = self["bg"])
        title_frame.grid(row = 0, column = 0, sticky = "NESW")

        title_frame.columnconfigure(index=0, weight = 1)
        title_frame.columnconfigure(index=1, weight = 1)
        title_frame.columnconfigure(index=2, weight = 1)

        tkinter.Label(title_frame, text = self.data["route"].name + " jelzésű " + self.data["route"].type, font = ("", 24), bg = self["bg"], fg="snow").grid(row = 0, columnspan=3, sticky = "NESW")
        tkinter.Label(title_frame, text = str(self.data["stops"][0][1]) + " " + self.data["stops"][-1][0].name + " felé", font = ("", 20), bg = self["bg"], fg="snow").grid(row = 1, columnspan=3, sticky = "NESW")

        if self.master.user is not None:
            tkinter.Label(title_frame, text="Alacsony padlós" if self.data["bonus"][0] else "Nem alacsony padlós", font=("", 18), bg=self["bg"], fg="snow").grid(row=2, column=0)
            tkinter.Label(title_frame, text="Útvonal hossza: " + str(self.data["bonus"][3]) + "km", font=("", 18), bg=self["bg"], fg="snow").grid(row=2, column=1)
            tkinter.Label(title_frame, text="Vezető: " + self.data["bonus"][1] + " " + self.data["bonus"][2], font=("", 18), bg=self["bg"], fg="snow").grid(row=2, column=2)

        result_frame = tkinter.Frame(self, bg = self["bg"])
        result_frame.grid(row = 1, sticky = "NESW")

        result_frame.columnconfigure(0, weight = 8)
        result_frame.columnconfigure(1, weight = 4)
        result_frame.columnconfigure(2, weight = 4)
        result_frame.columnconfigure(3, weight = 4)
        result_frame.columnconfigure(4, weight = 1)
        result_frame.columnconfigure(5, weight = 8)

        tkinter.Label(master=result_frame, text="Időpont", font=("", 16), bg=self["bg"], fg="snow").grid(row=0, column=1)
        tkinter.Label(master=result_frame, text="Megálló neve", font=("", 16), bg=self["bg"], fg="snow").grid(row=0, column=2)
        tkinter.Label(master=result_frame, text="Megálló helye", font=("", 16), bg=self["bg"], fg="snow").grid(row=0, column=3)

        grid_row_count = 1
        for stop, time in self.data["stops"]:
            tkinter.Label(result_frame, text = time, font = ("", 12), bg=self["bg"], fg="snow").grid(row = grid_row_count, column = 1, sticky = "NESW")
            tkinter.Label(result_frame, text = stop.name, font = ("", 12), bg=self["bg"], fg="snow").grid(row = grid_row_count, column = 2, sticky = "NESW")
            tkinter.Label(result_frame, text = stop.location, font = ("", 12), bg=self["bg"], fg="snow").grid(row = grid_row_count, column = 3, sticky = "NESW")
            tkinter.Button(result_frame, text = "Részletek", command = lambda stop = stop: self.stop_details(stop), bg = "dark slate blue", fg = "snow").grid(row = grid_row_count, column = 4, sticky = "NESW")

            grid_row_count += 1
