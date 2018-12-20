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
    # if the episode doesn't exceed return False
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
    all_shows_unsorted = get_shows_from_api()
    if order == 'name':
        return sorted(all_shows_unsorted, key=lambda k: k['name'])
    elif order == 'ratings':
        return sorted(all_shows_unsorted, key=lambda k: str(k['rating']['average']), reverse=True)


# query is a string
def get_search_results(query):
    results = []
    api_url = 'http://api.tvmaze.com/search/shows'
    r_json = requests.get(url=api_url, params=dict(q=query))
    r = r_json.json()
    for show in r:
        print(show)
        episodes_url = 'http://api.tvmaze.com/shows/{}/episodes'.format(show['show']['id'])
        episode_req = requests.get(url=episodes_url)
        show_episodes = episode_req.json()
        for episode in show_episodes:
            results.append({'showid': show['show']['id'], 'episodeid': episode['id'],
                            'text': '{}: {}'.format(show['show']['name'], episode['name'])})
    return results


def get_shows_from_api():
    api_url = 'http://api.tvmaze.com/shows'
    shows_page_number = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    while True:
        r = requests.get(url=api_url, params=dict(page=random.choice(shows_page_number)))
        # in case the page is not found in the API
        if r.status_code != 404:
            break
    response_list = r.json()
    return response_list


def get_specific_show_api(show_id):
    episodes_url = 'http://api.tvmaze.com/shows/{}/episodes'.format(show_id)
    show_url = 'http://api.tvmaze.com/shows/{}'.format(show_id)
    # get the show name
    r = requests.get(url=show_url)
    if r.status_code != 404:
        show = r.json()
    else:
        return False
    # get show episodes
    r = requests.get(url=episodes_url)
    show_episodes = r.json()
    return {'id': show['id'], 'name': show['name'], '_embedded': {'episodes': show_episodes}}


def get_specific_episode_api(show_id, episode_id):
    episodes_url = 'http://api.tvmaze.com/shows/{}/episodes'.format(show_id)
    r = requests.get(url=episodes_url)
    if r.status_code == 404:
        return False
    show_episodes = r.json()
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
