import os, re
from flask import (Flask, render_template, request)
from flask_pymongo import PyMongo
from time import sleep
from orb.KB import general_kb as orb_bot
from orb.KB import chat_state_classifier
from orb.KB import parse_input as parse_user_input
from orb.KB import voiceSystem

'''
Goal: Creates the Flask app and handles application routes.

Action: Sends user input to the right module and recieves its 
response to present to the user.
'''
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        MONGO_URI="mongodb://localhost:27017/orbDatabase"
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    # Create an instance of mongo(database) and voice agent 
    mongo=PyMongo(app)
    voiceAgent = voiceSystem.VoiceProcessor()

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

    ''' 
    Home page & initiate the chat with instructions 
    '''
    @app.route('/')
    def hello():
        orb_init = orb_bot.initiate()
        return render_template('home.html', orb_init=orb_init)

    ''' 
    User chats with orb through text; process it; respond to it; 
    '''
    @app.route('/process', methods=['GET'])
    def process():

        sleep(1)
        
        user_input = request.args.get('user_input')

        parse_text_object = parse_user_input.ParseText()

        user_input = parse_text_object.userInput(user_input)

        user_input = " ".join(user_input).lower()

        chat_state = chat_state_classifier.classify_chat(user_input)

        orb_response = chat_state.response(user_input)

        return orb_response

    ''' 
    Speek the orb response
    '''
    @app.route('/speek', methods=['GET'])
    def speek():
        user_input = request.args.get('user_input')
        voiceAgent.talkToMe(user_input)
        return 'success'

    ''' 
    User chats with orb through voice; presents the user input in text 
    '''
    @app.route('/speechInput', methods=['GET'])
    def speechInput():
        user_input = voiceAgent.audioInput()

        return user_input

    ''' 
    Responds to voice user input 
    '''
    @app.route('/speechResponse', methods=['GET'])
    def speechResponse():
        
        user_input = request.args.get('user_input')

        parse_text_object = parse_user_input.ParseText()

        user_input = parse_text_object.userInput(user_input)

        user_input = " ".join(user_input).lower()

        chat_state = chat_state_classifier.classify_chat(user_input)

        orb_response = chat_state.response(user_input)

        return orb_response


    return app