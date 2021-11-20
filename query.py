import requests
import json

def get_data(key, minutes):
    try:
        URL = "https://api.sl.se/api2/realtimedeparturesV4.json?key={}&siteid=1180&timewindow={}".format(key, minutes)
        r = requests.get(URL, timeout = 1)
        print(r.text)
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
    
