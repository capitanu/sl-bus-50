


def get_time(key, minutes):
    URL = "https://api.sl.se/api2/realtimedeparturesV4.xml?key={}&siteid=1180&timewindow={}".format(key, minutes)
