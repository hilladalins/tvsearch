import os
from bottle import (get, post, redirect, request, route, run, static_file,
                    template, Bottle, error)
import utils
import json


# Static Routes

@get("/js/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="./js")


@get("/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="./css")


@get("/images/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="./images")


@route('/')
def index():
    sectionData = None
    sectionTemplate = "./templates/home.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData=sectionData)


@route('/<path:re:browse(/name|/ratings)?>')
def browse(path):
    sectionTemplate = "./templates/browse.tpl"
    if path == 'browse/name':
        sectionData = utils.get_all_shows_sorted('name')
    elif path == 'browse/ratings':
        sectionData = utils.get_all_shows_sorted('ratings')
    else:
        sectionData = utils.get_shows_from_api()
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData=sectionData)


@route('/ajax/show/<id>')
def show_ajax(id):
    result = utils.get_specific_show_api(id)
    return template("./templates/show.tpl", version=utils.getVersion(), result=result)


@route('/show/<id>')
def show(id):
    sectionData = utils.get_specific_show_api(id)
    if not sectionData:
        sectionTemplate = "./templates/404.tpl"
        return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                        sectionData={})
    else:
        sectionTemplate = "./templates/show.tpl"
        return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                        sectionData=sectionData)


@route('/ajax/show/<id>/episode/<episode_id>')
def episode_ajax(id, episode_id):
    result = utils.get_specific_episode_api(id, episode_id)
    return template("./templates/episode.tpl", version=utils.getVersion(), result=result)


@route('/show/<id>/episode/<episode_id>')
def episode(id, episode_id):
    sectionData = utils.get_specific_episode_api(id, episode_id)
    #hila
    if not sectionData:
        sectionTemplate = "./templates/404.tpl"
        return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                        sectionData={})
    else:
        sectionTemplate = "./templates/episode.tpl"
        return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                        sectionData=sectionData)


@route('/search', method=['GET', 'POST'])
def search():
    query = request.forms.get('q')
    sectionData = None
    if query:
        sectionTemplate = "./templates/search_result.tpl"
        sectionData = utils.get_search_results(query)
    else:
        sectionTemplate = "./templates/search.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData={}, query=query, results=sectionData)


run(host='localhost', port=os.environ.get('PORT', 5000))
