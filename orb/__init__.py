import os, re
from flask import (Flask, render_template, request)
from flask_pymongo import PyMongo
from time import sleep
from orb.KB import general_kb as orb_bot
from orb.KB import chat_state_classifier
from orb.KB import parse_input as parse_user_input


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
        orb_init = orb_bot.initiate()
        return render_template('home.html', orb_init=orb_init)

    # User chats with orb; process it; respond to it;
    @app.route('/process', methods=['GET'])
    def process():

        sleep(1)
        
        user_input = request.args.get('user_input')

        parse_text_object = parse_user_input.ParseText()

        user_input = parse_text_object.userInput(user_input)

        user_input = " ".join(user_input).lower()

        # print("user input parse: ", user_input)

        chat_state = chat_state_classifier.classify_chat(user_input)

        orb_response = chat_state.response(user_input)

        return orb_response


    return app