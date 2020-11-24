import ContentPage
import tkinter
import Entity
import mysql.connector
import StopDetails




class RouteResults(ContentPage.ContentPage):
    def __init__(self, data, *args, **kwargs):
        ContentPage.ContentPage.__init__(self, data, *args, **kwargs)

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


    def stop_details(self, stop: Entity.Stop):
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

    
    def refresh(self):
        pass
