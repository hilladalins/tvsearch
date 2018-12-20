import os
from bottle import (get, post, redirect, request, route, run, static_file,
                    template, Bottle)
import utils
import json
import functools


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
    sectionTemplate = "./templates/home.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData={})


@route('/<path:re:browse(/name|/ratings)?>')
def browse(path):
    sectionTemplate = "./templates/browse.tpl"
    if path == 'browse/name':
        sectionData = utils.get_all_shows_sorted('name')
    elif path == 'browse/ratings':
        sectionData = utils.get_all_shows_sorted('ratings')
    else:
        sectionData = utils.getAllShows()
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData=sectionData)


@route('/ajax/show/<id>')
def show(id):
    result = utils.getShow(id)
    return template("./templates/show.tpl", version=utils.getVersion(), result=result)


@route('/show/<id>')
def show(id):
    sectionTemplate = "./templates/show.tpl"
    sectionData = utils.getShow(id)
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData=sectionData)


@route('/ajax/show/<id>/episode/<episode_id>')
def show(id, episode_id):
    result = utils.getEpisode(id, episode_id)
    print(result)
    return template("./templates/episode.tpl", version=utils.getVersion(), result=result)


@route('/show/<id>/episode/<episode_id>')
def show(id, episode_id):
    sectionTemplate = "./templates/episode.tpl"
    sectionData = utils.getEpisode(id, episode_id)
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
