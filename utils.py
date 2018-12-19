from bottle import template
import json
# import ast
# ast.literal_eval("{'muffin' : 'lolz', 'foo' : 'kitty'}")

JSON_FOLDER = './data'
AVAILABLE_SHOWS = ["7", "66", "73", "82", "112", "143", "175", "216", "1371", "1871", "2993", "305"]


def getVersion():
    return "0.0.1"


def getJsonFromFile(showName):
    try:
        return template("{folder}/{filename}.json".format(folder=JSON_FOLDER, filename=showName))
    except:
        return "{}"


def getShow(showName):
    return json.loads(getJsonFromFile(showName))


def getAllShows():
    result = []
    for show in AVAILABLE_SHOWS:
        result.append(json.loads(getJsonFromFile(show)))
    return result







