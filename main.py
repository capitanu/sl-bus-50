import query
from playsound import playsound
import time
import os
import datetime

def get_api_key():
    api_key_file = open("api_key", 'r')
    api_key = api_key_file.readlines()[0]
    return api_key

def query_do():
    api_key = get_api_key()
    returned_data = query.get_data(api_key, 60)
    parsed_data = query.query_parser(returned_data)
    now = datetime.datetime.now()
    for bus in parsed_data:
        print(bus)
        if bus[2] == '2 min' or "{}:{}".format(now.hour, now.minute+2) == bus[2]:
            os.system("mpg123 -n 200 florin.mp3 > /dev/null 2>&1")
    print("")
            
while True:
    query_do()
    time.sleep(30)
