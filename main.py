import query
from playsound import playsound
import time
import datetime
import tkinter as tk
import numpy as np
import os

TIME = 3

displayed_data = [['Init'],[],[]]


api_key_file = open("api_key", 'r')
api_key = api_key_file.readlines()[0].strip("\n")

def query_do():
    try:
        global test, displayed_data
        returned_data = query.get_data(api_key, 60)
        parsed_data = query.query_parser(returned_data)
        now = datetime.datetime.now()
        time = now.hour < 23 and now.hour > 8
        for bus in parsed_data:
            if bus[2] == '{} min'.format(TIME) or "{}:{}".format(now.hour, now.minute+TIME) == bus[2]:
                if not np.array_equal(parsed_data[0], displayed_data[0]) and time:
                    os.system("mpg123 3min.mp3 > /dev/null 2>&1")
            if bus[2] == 'Nu' or "{}:{}".format(now.hour, now.minute) == bus[2]:
                if not np.array_equal(parsed_data[0], displayed_data[0]) and time:
                    os.system("mpg123 nu.mp3 > /dev/null 2>&1")
        displayed_data = parsed_data[:3]
        return parsed_data[:3]
    except:
        return []


def repeat():
    while True:
        query_do()
        time.sleep(3)

root = tk.Tk()

def init_ui():
    data = [
            ['', '', ''],
            ['', '', ''],
            ['', '', '']
           ]
    root.title("Lektorstiggen")
    root.attributes("-fullscreen", True)
    
    for i, bus in enumerate(data):
        labelnr = tk.Label(root, font=("Arial", 60), text = bus[0]).grid(column=0, row=i)
        labeldest = tk.Label(root, font=("Arial", 60), text = bus[1]).grid(column=1, row=i)
        labeltime = tk.Label(root, font=("Arial", 60), text = bus[2]).grid(column=2, row=i)
    for i in range(len(data)):
        root.rowconfigure(i, weight=1)
    root.after(30, update_ui)


def update_ui():
    data = query_do()
    now = datetime.datetime.now()
    time = now.hour < 23 and now.hour > 8
    if len(data) == 0 and time:
        root.after(300000, update_ui)    
        return
    elif len(data) == 0 and not time:
        root.after(60000, update_ui)
        return
    while len(data) < 3:
        data.append(['','',''])
    widgets = np.array(root.winfo_children()).reshape(3,3)
    for bus, labels in zip(data, widgets):
        labels[0].config(text = bus[0])
        labels[1].config(text = bus[1])
        labels[2].config(text = bus[2])
    if time:
        root.after(300000, update_ui)
    else:
        root.after(60000, update_ui)    

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.after(0, init_ui)
root.mainloop()

