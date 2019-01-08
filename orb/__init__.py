import os, re
from flask import (Flask, render_template, request)
from flask_pymongo import PyMongo
from time import sleep
from orb.KB import convo as orb_bot
from orb.KB import chat_state_classifier


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

    # Home page & initiate the chat with instructions
    @app.route('/')
    def hello():
        chat_instruction, orb_init = orb_bot.initiate()
        return render_template('home.html', chat_instruction=chat_instruction, orb_init=orb_init)

    # User chats with orb; process it; respond to it;
    @app.route('/process', methods=['GET'])
    def process():

        sleep(1)
        
        user_input = normalize_input(request.args.get('user_input'))

        chat_state = chat_state_classifier.classify_chat(user_input)

        orb_response = chat_state.response(user_input)

        return orb_response


    def normalize_input(user_input):
        user_input = user_input.lower()
        return re.sub('[^A-Za-z0-9/:]+', ' ', user_input)
        


    return app