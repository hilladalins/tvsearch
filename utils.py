from bottle import template
import json
import requests

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


def parseJsonShow(showName):
    return json.loads(getJsonFromFile(showName))


def getShowIdAndName(show_to_return, show):
    show_to_return['id'] = show['id']
    show_to_return['name'] = show['name']
    return show_to_return


def getEpisodeSeasonNameAndImage(episode_to_return, episode):
    episode_to_return['season'] = episode['season']
    episode_to_return['name'] = episode['name']
    episode_to_return['image'] = {}
    if episode['image']:
        episode_to_return['image']['original'] = episode['image']['original']
    return episode_to_return


def getShow(showName):
    show = parseJsonShow(showName)
    show_to_return = {}
    show_to_return = getShowIdAndName(show_to_return, show)
    show_to_return['_embedded'] = {}
    show_to_return['_embedded']['episodes'] = []
    episodes = show['_embedded']['episodes']
    for i in range(len(episodes)):
        episode = {}
        episode = getEpisodeSeasonNameAndImage(episode, episodes[i])
        episode['id'] = episodes[i]['id']
        show_to_return['_embedded']['episodes'].append(episode)
    return show_to_return


def getEpisode(showName, episodeName):
    show = parseJsonShow(showName)
    episode_to_return = {}
    for episode in show['_embedded']['episodes']:
        if episode['id'] == int(episodeName):
            episode_to_return = getEpisodeSeasonNameAndImage(episode_to_return, episode)
            episode_to_return['number'] = episode['number']
            episode_to_return['summary'] = episode['summary']
            return episode_to_return
    #if the episode doesn't exceed return False
    return False


def getAllShows():
    result = []
    for show in AVAILABLE_SHOWS:
        show = parseJsonShow(show)
        show_to_return = {}
        show_to_return = getShowIdAndName(show_to_return, show)
        show_to_return['rating'] = {}
        show_to_return['rating']['average'] = show['rating']['average']
        show_to_return['image'] = {}
        show_to_return['image']['original'] = show['image']['original']
        result.append(show_to_return)
    return result


def get_all_shows_sorted(order):
    all_shows_unsorted = getAllShows()
    if order == 'name':
        return sorted(all_shows_unsorted, key=lambda k: k['name'])
    elif order == 'ratings':
        return sorted(all_shows_unsorted, key=lambda k: str(k['rating']['average']), reverse=True)


# query is a string
def get_search_results(query):
    results = []
    r_json = requests.get(url=api_url, params=dict(q=query))
    r = r_json.json()
    for show in r:
        for episode in show["_embedded"]["episodes"]:
            results.append({'showid': show['id'], 'episodeid': episode['id'],
            'text': '{}: {}'.format(show['name'], episode['name'])})
    return results

#to be implemented in the API version:
# def get_shows_from_api():
#     api_url = 'http://api.tvmaze.com/shows'
#     # r = requests.get(url=api_url, params=dict(q=, q2=))
#     r = requests.get(url=api_url)
#     response_json = r.json()
#     return response_json
