import os
from bottle import (get, post, redirect, request, route, run, static_file, template, error)
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
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData = {})


@route("/browse")
def browse():
    shows = []
    for show in utils.AVAILABE_SHOWS:
        shows.append(json.loads(utils.getJsonFromFile(show)))
    browse_template = "./templates/browse.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=browse_template, sectionData=shows)


@route("/ajax/show/<number>")
def show_ajax(number):
    selected_show = json.loads(utils.getJsonFromFile(number))
    return template("./templates/show.tpl", result=selected_show)


@route("/show/<number>")
def show(number):
    selected_show = json.loads(utils.getJsonFromFile(number))
    show_template = "./templates/show.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=show_template, sectionData=selected_show)


@route("/ajax/show/<shownumber>/episode/<episodenumber>")
def episode(shownumber, episodenumber):
    selected_show = json.loads(utils.getJsonFromFile(shownumber))
    episodes = selected_show["_embedded"]["episodes"]
    for episode in episodes:
        if episode["id"] == int(episodenumber):
            return template("./templates/episode.tpl", result=episode)


@route("/show/<shownumber>/episode/<episodenumber>")
def episode(shownumber, episodenumber):
    selected_show = json.loads(utils.getJsonFromFile(shownumber))
    episodes = selected_show["_embedded"]["episodes"]
    episode_template = "./templates/episode.tpl"
    for episode in episodes:
        if episode["id"] == int(episodenumber):
            return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=episode_template, sectionData=episode)


@route("/search")
def search():
    search_template = "./templates/search.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=search_template, sectionData = {})

@route("/search", method="POST")
def search():
    user_input=request.POST.get("q")
    results=[]
    for show in utils.AVAILABE_SHOWS:
        each_show=json.loads(utils.getJsonFromFile(show))
        episodes = each_show["_embedded"]["episodes"]
        for each_episode in episodes:
            if user_input.lower() in each_episode["name"].lower() or user_input.lower() in str(each_episode["summary"]).lower():
                result={
                    'showid': each_show["id"],
                    'episodeid': each_episode["id"],
                    'text': "%s : %s" % (each_show["name"], each_episode["name"])}

                results.append(result)
    search_template = "./templates/search_result.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=search_template, sectionData = {}, query=user_input, results=results)



@error(404)
def error(error):
    error_template = "./templates/404.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=error_template, sectionData={})


run(host='localhost', port=os.environ.get('PORT', 5000))