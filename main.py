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

root = tk.Tk()
root.configure(background = "white")
root.geometry("1920x1080")
bg = PhotoImage(file = "christmas.png")

canvas = Canvas(root, width=1920, height=1080)
canvas.pack(expand=YES, fill=BOTH)
canvas.create_image(0, 0, image=bg, anchor=NW, tag="image")

api_key_file = open("api_key", 'r')
api_key = api_key_file.readlines()[0].strip("\n")

def get_data(key, minutes):
    try:
        URL = "https://api.sl.se/api2/realtimedeparturesV4.json?key={}&siteid=1180&timewindow={}".format(key, minutes)
        r = requests.get(URL, timeout = 1)
        return r.text
    except:
        return "Failed to retrieve data"

def query_parser(data):
    try:
        json_string = json.loads(data)
        if "ResponseData" not in json_string:
            return []
        response_data = json_string["ResponseData"]
        buses = response_data["Buses"]
        rtn = []
        for bus in buses[:3]:
            dt = bus["DisplayTime"]
            if not "min" in dt and dt != "Nu":
                now = datetime.datetime.now()
                hour = str(now.hour)
                if dt[:2] == hour[:2]:
                    dt = abs(int(dt[3:5]) - int(now.minute))
                else:
                    dt = 60 - int(now.minute) + int(dt[3:5])
                dt = "{} min".format(dt)
                
            rtn.append([bus["LineNumber"], bus["Destination"], dt])
        return rtn
    except:
        return []


def failed_case():
    print("FAILED CASE")
    busses = []
    for i in range(3):
        bus = []
        bus.append(canvas.itemcget(canvas.find_withtag("line{}0".format(i)), 'text'))
        bus.append(canvas.itemcget(canvas.find_withtag("line{}1".format(i)), 'text'))
        bus.append(canvas.itemcget(canvas.find_withtag("line{}2".format(i)), 'text'))
        busses.append(bus)

    print(busses)
    for i in range(3):
        canvas.delete("line{}0".format(i))
        canvas.delete("line{}1".format(i))
        canvas.delete("line{}2".format(i))

    if busses[0][2] == "Nu":
        busses = busses[1:]
        busses[0][2] = "{} min".format(int(busses[0][2][:len(busses[0][2]) - 4]) - 1)
        busses[1][2] = "{} min".format(int(busses[1][2][:len(busses[1][2]) - 4]) - 1)

    elif "1" in busses[0][2]:
        busses[0][2] = "Nu"
        busses[1][2] = "{} min".format(int(busses[1][2][:len(busses[1][2]) - 4]) - 1)
        busses[2][2] = "{} min".format(int(busses[2][2][:len(busses[2][2]) - 4]) - 1)
    else:
        busses[0][2] = "{} min".format(int(busses[0][2][:len(busses[0][2]) - 4]) - 1)
        busses[1][2] = "{} min".format(int(busses[1][2][:len(busses[1][2]) - 4]) - 1)
        busses[2][2] = "{} min".format(int(busses[2][2][:len(busses[2][2]) - 4]) - 1)

    print(busses)
    

    for i, bus in enumerate(busses):
        canvas.create_text(1920/6, 1080/6 + i*1080/3, fill="green", font=("Arial", 60), text=bus[0], tag="line{}0".format(i))
        canvas.create_text(1920/6 + 1920/3, 1080/6 + i*1080/3, fill="green", font=("Arial", 60), text=bus[1], tag="line{}1".format(i))
        canvas.create_text(1920/6 + 2*1920/3, 1080/6 + i*1080/3, fill="green", font=("Arial", 60), text=bus[2], tag="line{}2".format(i))


def query_do():
    try:
        global test, displayed_data
        returned_data = get_data(api_key, 60)
        if returned_data == "Failed to retrieve data":
            failed_case()
            return "failed case"
        parsed_data = query_parser(returned_data)
        now = datetime.datetime.now()
        displayed_data = parsed_data[:3]
        return parsed_data[:3]
    except:
        return []




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

    print("UPDATE UI")
    data = query_do()

    if data == "failed case":
        root.after(60000, update_ui)
        return
        

    now = datetime.datetime.now()
    time = now.hour < 23 and now.hour > 8

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
    if not time:
        root.after(300000, update_ui)
    else:
        root.after(60000, update_ui)
    return





root.after(0, init_ui)
root.mainloop()

