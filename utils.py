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


# query is a string
def get_search_results(query):
    results = []
    all_shows = getAllShows()
    # searching if the user entered the show's name. not implemented in ITC's search, but should be.
    for show in all_shows:
        if query == show['name']:
            if show["_embedded"]['episodes']:
                for episode in show["_embedded"]['episodes']:
                    results.append({'showid': show['id'], 'episodeid': episode['id'],
                                    'text': '{}: {}'.format(show['name'], episode['name'])})
                return results
    # searching if the user entered a text as part of the summary
    # "2. For the search functionality search for the string in episode name and summary" - from the HIVE
    for show in all_shows:
        for episode in show["_embedded"]['episodes']:
            if episode['name'] and episode['summary']:
                if query in episode['name'] or query in episode['summary']:
                    results.append(
                        {'showid': show['id'], 'episodeid': episode['id'],
                         'text': '{}: {}'.format(show['name'], episode['name'])})
    return results
