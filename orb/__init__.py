import os
from flask import (Flask, render_template, request)
from flask_pymongo import PyMongo
from time import sleep
from orb import convo as orbb


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        MONGO_URI="mongodb://localhost:27017/orbDatabase"
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    mongo=PyMongo(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Home page
    @app.route('/')
    def hello():
        # test_data = mongo.db.testDoc.find_one_or_404()
        # return render_template('home.html', test_data=test_data)
        chat_instruction, orb_init = orbb.initiate()
        return render_template('home.html', chat_instruction=chat_instruction, orb_init=orb_init)

    # Process user input and respond
    @app.route('/process', methods=['GET'])
    def process():
        sleep(2)
        user_input = request.args.get('user_input').lower()
        orb_response = orbb.chat_respond(user_input)
        print(user_input)
        station = mongo.db.trainStations.find_one_or_404({"name": user_input})
        print(station["abbreviation"])
        return orb_response

    return app