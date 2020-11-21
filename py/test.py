import tkinter
import tkinter.messagebox
import mysql.connector




def Insert():
    if keyInput.get() == "" or valueInput.get() == "":
        tkinter.messagebox.showerror("ERROR", "All fields must be filled!")

    elif not keyInput.get().isnumeric():
        tkinter.messagebox.showerror("ERROR", "The key must be an integer!")

    else:
        connection = mysql.connector.connect(host = dbhost, database = dbname, user = dbuser, password = dbpwd)
       
        try:
            connection.cursor().execute(operation = "INSERT INTO test(kulcs, ertek) VALUES(%s, %s)", params = (keyInput.get(), valueInput.get()))
            connection.commit()

            tkinter.messagebox.showinfo("INFO", "Successful insertion!")
        
        except:
            tkinter.messagebox.showerror("ERROR", "The key is already in use!")
        
        finally:
            keyInput.delete(0, "end")
            valueInput.delete(0, "end")
            connection.close()



def Update():
    if keyInput.get() == "" or valueInput.get() == "":
        tkinter.messagebox.showerror("ERROR", "All fields must be filled!")

    elif not keyInput.get().isnumeric():
        tkinter.messagebox.showerror("ERROR", "The key must be an integer!")

    else:
        connection = mysql.connector.connect(host = dbhost, database = dbname, user = dbuser, password = dbpwd)
       
        try:
            cursor = connection.cursor()
            cursor.execute(operation = "UPDATE test SET ertek = %s WHERE kulcs = %s", params = (valueInput.get(), keyInput.get()))
            connection.commit()

            if (cursor.rowcount == 0):
                tkinter.messagebox.showerror("ERROR", "Entry does not exist!")
            else:
                tkinter.messagebox.showinfo("INFO", "Successful updating!")
        
        except:
            tkinter.messagebox.showerror("ERROR", "Big oof!")
        
        finally:
            keyInput.delete(0, "end")
            valueInput.delete(0, "end")
            connection.close()



def Delete():
    if keyInput.get() == "":
        tkinter.messagebox.showwarning("ERROR", "Please enter a key!")

    elif not keyInput.get().isnumeric():
        tkinter.messagebox.showerror("ERROR", "The key must be an integer!")

    else:
        connection = mysql.connector.connect(host = dbhost, database = dbname, user = dbuser, password = dbpwd)
        cursor = connection.cursor()

        try:
            cursor.execute(operation = "DELETE FROM test WHERE kulcs = %s", params = (keyInput.get(),))
            connection.commit()

            if (cursor.rowcount == 0):
                tkinter.messagebox.showerror("ERROR", "Entry does not exist!")
            else:
                tkinter.messagebox.showinfo("INFO", "Successful deletion!")

        except:
            tkinter.messagebox.showerror("ERROR", "Big oof!")

        finally:
            keyInput.delete(0, "end")
            valueInput.delete(0, "end")
            connection.close()



def Get():
    if keyInput.get() == "":
        tkinter.messagebox.showerror("ERROR", "Enter a key number!")

    elif not keyInput.get().isnumeric():
        tkinter.messagebox.showerror("ERROR", "The key must be an integer!")

    else:
        connection = mysql.connector.connect(host = dbhost, database = dbname, user = dbuser, password = dbpwd)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM test WHERE kulcs = {}".format(keyInput.get()))
        rows = cursor.fetchmany(1)

        if not rows:
            tkinter.messagebox.showinfo("INFO", "No entry exists with this key!")

        else:
            for row in rows:
                valueInput.insert(0, row[1])

        connection.close()




dbhost = "localhost"
dbname = "test"
dbuser = "root"
dbpwd = ""

root = tkinter.Tk()
root.geometry("600x300")
root.title("test")

key = tkinter.Label(root, text = "Key", font = ("bold", 10))
key.place(x = 20, y = 30)

keyInput = tkinter.Entry()
keyInput.place(x = 150, y = 30)

value = tkinter.Label(root, text = "Value", font = ("bold", 10))
value.place(x = 20, y = 60)

valueInput = tkinter.Entry()
valueInput.place(x = 150, y = 60)

insertButton = tkinter.Button(root, text = "Insert", font = ("italic", 10), command = Insert)
updateButton = tkinter.Button(root, text = "Update", font = ("italic", 10), command = Update)
deleteButton = tkinter.Button(root, text = "Delete", font = ("italic", 10), command = Delete)
getButton = tkinter.Button(root, text = "Get", font  = ("italic", 10), command = Get)

insertButton.place(x = 20, y = 100)
updateButton.place(x = 80, y = 100)
deleteButton.place(x = 140, y = 100)
getButton.place(x = 200, y = 100)

listBox = tkinter.Listbox(root)
listBox.place(x = 290, y = 30)

root.mainloop()
