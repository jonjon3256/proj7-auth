import os
from flask import Flask, redirect, url_for, request, render_template
import flask
from pymongo import MongoClient
import arrow
import acp_times
import config
import logging



app = Flask(__name__)
#CONFIG = config.configuration()
#app.secret_key = CONFIG.SECRET_KEY

client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)
db = client.tododb


@app.route('/')
@app.route('/index')
def index():
   # _items = db.tododb.find()
    #items = [item for item in _items]

    return flask.render_template('calc.html')

@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("calc")
    return flask.render_template('404.html'), 404


@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))


    b_dist = request.args.get('b_dist',type=int)
    start_d = request.args.get('start_d',type=str)
    start_time = request.args.get('start_time',type=str)
    start = start_d +" "+ start_time
    
   
    # FIXME: These probably aren't the right open and close times
    # and brevets may be longer than 200km
    
    
    open_time = acp_times.open_time(km,b_dist,start)
    close_time = acp_times.close_time(km,b_dist,start)
    result = {"open": open_time, "close": close_time}
    #data_list = {"open":open_time, "close": close_time}
    #app.logger.debug(data_list)
    #datalist.append(data_list)
    return flask.jsonify(result=result)

@app.route('/todo',methods=['POST'])
def todo():
    _items = db.tododb.find()
    items = [item for item in _items]
    return render_template('todo.html',items=items)


@app.route('/new')
def new():
    mi = request.args.get('mi',type=str)
    open_t = request.args.get('open',type=str)
    close_t = request.args.get('close',type=str)

    name = mi + km
    description = [open_t,close_t]
    item_doc = {
           'name':name,
           'description':description
    }
    db.todo.insert_one(item_doc)
    return "o"



#############

#app.debug = CONFIG.DEBUG
#if app.debug:
    #app.logger.setLevel(logging.DEBUG)

#@app.route('/')
@app.route("/favicon.ico")
def favicon():
    return flask.render_template('calc.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
