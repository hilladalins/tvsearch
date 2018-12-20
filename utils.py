from bottle import template
import json
import requests
import random

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


def getEpisode(showName, episodeName):
    show = json.loads(getJsonFromFile(showName))
    for episode in show['_embedded']['episodes']:
        if episode['id'] == int(episodeName):
            return episode


def getAllShows():
    result = []
    for show in AVAILABLE_SHOWS:
        result.append(json.loads(getJsonFromFile(show)))
    return result


def get_all_shows_sorted(order):
    all_shows_unsorted = get_shows_from_api()
    if order == 'name':
        return sorted(all_shows_unsorted, key=lambda k: k['name'])
    elif order == 'ratings':
        return sorted(all_shows_unsorted, key=lambda k: str(k['rating']['average']), reverse=True)
    else:
        print('provided wrong parameter to get_all_shows_sorted. only "name" or "ratings"')
        return all_shows_unsorted


# query is a string
def get_search_results(query):
    results = []
    all_shows = getAllShows()
    # searching if the user entered a text as part of the summary
    # "2. For the search functionality search for the string in episode name and summary" - from the HIVE
    for show in all_shows:
        for episode in show["_embedded"]['episodes']:
            if episode['name'] and episode['summary']:  # to investigate
                if query in episode['name'] or query in episode['summary']:
                    results.append(
                        {'showid': show['id'], 'episodeid': episode['id'],
                         'text': '{}: {}'.format(show['name'], episode['name'])})
    return results


def get_shows_from_api():
    api_url = 'http://api.tvmaze.com/shows'
    shows_page_number = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    while True:
        r = requests.get(url=api_url, params=dict(page=random.choice(shows_page_number)))
        # in case the page is not found in the API
        if r.status_code != 404:
            break
    response_dict = r.json()
    return response_dict


def get_specific_show_api(show_id):
    episodes_url = 'http://api.tvmaze.com/shows/{}/episodes'.format(show_id)
    show_url = 'http://api.tvmaze.com/shows/{}'.format(show_id)
    # get the show episodes
    r = requests.get(url=episodes_url)
    if r.status_code != 404:
        show_episodes = r.json()
    else:
        return False
    # get the show name
    r = requests.get(url=show_url)
    if r.status_code != 404:
        show = r.json()
    else:
        return False
    return {'id': show_id, 'name': show['name'], '_embedded': {'episodes': show_episodes}}


def get_specific_episode_api(show_id, episode_id):
    episodes_url = 'http://api.tvmaze.com/shows/{}/episodes'.format(show_id)
    r = requests.get(url=episodes_url)
    if r.status_code != 404:
        show_episodes = r.json()
    else:
        return False
    for episode in show_episodes:
        if int(episode_id) == episode['id']:
            if episode['image']:
                original = episode['image']['original']
            else:
                original = episode['image']
            return {
                'name': episode['name'],
                'season': episode['season'],
                'number': episode['number'],
                'image': {'original': original},
                'summary': episode['summary']
            }
    # iterated through all the show and didn't find the episode in the api, returning False
    return False
