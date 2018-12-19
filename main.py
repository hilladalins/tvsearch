import os
from bottle import (get, post, redirect, request, route, run, static_file,
                    template)
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
    sectionTemplate = "./templates/home.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData={})


@route('/browse')
def browse():
    sectionTemplate = "./templates/browse.tpl"
    sectionData = utils.getAllShows()
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
