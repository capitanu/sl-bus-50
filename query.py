import requests
import json

def get_data(key, minutes):
    URL = "https://api.sl.se/api2/realtimedeparturesV4.json?key={}&siteid=1180&timewindow={}".format(key, minutes)
    r = requests.get(URL)
    return r.text

def query_parser(data):
    json_string = json.loads(data)
    response_data = json_string["ResponseData"]
    return response_data
    
