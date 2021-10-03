import query
from playsound import playsound
import time
import os
import datetime
import tkinter as tk

TIME = 3
test = 0
def get_api_key():
    api_key_file = open("api_key", 'r')
    api_key = api_key_file.readlines()[0]
    return api_key

def query_do():
    global test
    api_key = get_api_key()
    returned_data = query.get_data(api_key, 60)
    parsed_data = query.query_parser(returned_data)
    now = datetime.datetime.now()
    for bus in parsed_data:
        print(bus)
        if bus[2] == '{} min'.format(TIME) or "{}:{}".format(now.hour, now.minute+TIME) == bus[2]:
            os.system("mpg123 -n 200 3min.mp3 > /dev/null 2>&1")
        if bus[2] == 'Nu' or "{}:{}".format(now.hour, now.minute) == bus[2]:
            os.system("mpg123 -n 200 nu.wav > /dev/null 2>&1")


    temp = [
        ['50', 'Odenplan', '2 min'],
        ['50', 'Odenplan', '10 min'],
        ['50', 'Odenplan', '13:25']
    ]
    if test == 1:
        temp[2][1] = 'HAHHA'
        temp.append(['50', 'Test','Nu'])
    test = 1
    return temp
    return parsed_data


def repeat():
    while True:
        query_do()
        time.sleep(30)


def init_ui(root):
    data = query_do()
    print("help")
    for widget in root.winfo_children():
        widget.destroy()
    root.title("Lektorstiggen")
    root.attributes("-fullscreen", True)
    for i, bus in enumerate(data):
        labelnr = tk.Label(root, text = bus[0]).grid(column=0, row=i)
        labeldest = tk.Label(root, text = bus[1]).grid(column=1, row=i)
        labeltime = tk.Label(root, text = bus[2]).grid(column=2, row=i)
    for i in range(len(bus)):
        root.rowconfigure(i, weight=1)



root = tk.Tk()
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.after(30, init_ui(root))
root.mainloop()

