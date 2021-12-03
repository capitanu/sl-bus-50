import query
from playsound import playsound
import time
import datetime
import tkinter as tk
from tkinter import *
import numpy as np
from PIL import ImageTk, Image
import os
import requests
import json


TIME = 3

displayed_data = [['Init'],[],[]]


api_key_file = open("api_key", 'r')
api_key = api_key_file.readlines()[0].strip("\n")

def get_data(key, minutes):
    try:
        URL = "https://api.sl.se/api2/realtimedeparturesV4.json?key={}&siteid=1180&timewindow={}".format(key, minutes)
        r = requests.get(URL, timeout = 1)
        return r.text
    except:
        return ""

def query_parser(data):
    try:
        json_string = json.loads(data)
        if "ResponseData" not in json_string:
            return []
        response_data = json_string["ResponseData"]
        buses = response_data["Buses"]
        rtn = []
        for bus in buses:
            rtn.append([bus["LineNumber"], bus["Destination"], bus["DisplayTime"]])
        return rtn
    except:
        return []


def query_do():
    try:
        global test, displayed_data
        returned_data = get_data(api_key, 60)
        parsed_data = query_parser(returned_data)
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
root.configure(background = "white")
root.geometry("1920x1080")
bg = PhotoImage(file = "christmas.png")

canvas = Canvas(root, width=1920, height=1080)
canvas.pack(expand=YES, fill=BOTH)
canvas.create_image(0, 0, image=bg, anchor=NW, tag="image")

def init_ui():
    data = [
            ['', '', ''],
            ['', '', ''],
            ['', '', '']
           ]
    root.title("Lektorstiggen")
    root.attributes("-fullscreen", True)
    
    for i, bus in enumerate(data):
        canvas.create_text(1920/6, 1080/6 + i*1080/3, fill="green", font=("Arial", 60), text=bus[0], tag="line{}0".format(i))
        canvas.create_text(1920/6 + 1920/3, 1080/6 + i*1080/3, fill="green", font=("Arial", 60), text=bus[1], tag="line{}1".format(i))
        canvas.create_text(1920/6 + 2*1920/3, 1080/6 + i*1080/3, fill="green", font=("Arial", 60), text=bus[2], tag="line{}2".format(i))
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

    for i in range(3):
        canvas.delete("line{}0".format(i))
        canvas.delete("line{}1".format(i))
        canvas.delete("line{}2".format(i))
    while len(data) < 3:
        data.append(['','',''])
    for i, bus in enumerate(data):
        canvas.create_text(1920/6, 1080/6 + i*1080/3, fill="green", font=("Arial", 60), text=bus[0], tag="line{}0".format(i))
        canvas.create_text(1920/6 + 1920/3, 1080/6 + i*1080/3, fill="green", font=("Arial", 60), text=bus[1], tag="line{}1".format(i))
        canvas.create_text(1920/6 + 2*1920/3, 1080/6 + i*1080/3, fill="green", font=("Arial", 60), text=bus[2], tag="line{}2".format(i))
    if time:
        root.after(300000, update_ui)
    else:
        root.after(60000, update_ui)    





root.after(0, init_ui)
root.mainloop()

