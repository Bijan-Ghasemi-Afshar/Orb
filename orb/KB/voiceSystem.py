from gtts import gTTS
import speech_recognition as sr
# pip install speechrecognition
import os
import re
import webbrowser
import smtplib
import requests
from weather import Weather, Unit 
import pyttsx3
# pip install weather-api

class VoiceProcessor:

    state = True
    threshold = 500
    sampleRate = 48000
    def __init__(self):
        self.state=True
        self.threshold = 500
        self.sampleRate = 48000

    '''
    Talk function, this generates audion output from speakers
    '''    
    def talkToMe(self,text):

        print(text)
        print("called")
        engine = pyttsx3.init()
        engine.setProperty('rate', 140)
        engine.setProperty('volume', 2)
        engine.say(text)
        engine.runAndWait()


    '''
    microphone configuration functions
    '''
    def config(self):

        # list all microphones on the system
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

    '''
    Function to detect silence
    '''
    def isSilent(self,snd_data):
        "Returns 'True' if below the 'silent' threshold"
        return max(snd_data) < self.threshold

    '''
    Specific audio functions 
    '''
    def audioInput(self):
        "listens for commands"
        
        r = sr.Recognizer()

        with sr.Microphone() as source:
            print('System ready...')
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)

        try:
            command = r.recognize_google(audio).lower()
            print('You said: ' + command + '\n')

        #loop back to continue to listen for commands if unrecognizable speech is received
        except sr.UnknownValueError:
            print('Your last command couldn\'t be heard')
            command = self.audioInput()
        return command

    '''
    Detect specific audio input functions, such as exit, help , configuration. 
    '''
    def assistant(self,command):
        "if statements for executing commands"
        state = True
        if "orb stop" in command:
            state = False
            print(state)
            exit()
        elif 'how are you feeling' in command:
            self.talkToMe('i feel great!')

        elif 'open website' in command:
            reg_ex = re.search('open website (.+)', command)
            if reg_ex:
                domain = reg_ex.group(1)
                url = 'https://www.' + domain
                webbrowser.open(url)
                print('Done!')
            else:
                pass
        elif 'towner' in command:
            self.talkToMe('Towner is a monkey he likes to eat nutts')
        elif 'test' in command:
            self.talkToMe('testing 1 2 3')
        elif 'joke' in command:
            res = requests.get(
                    'https://icanhazdadjoke.com/',
                    headers={"Accept":"application/json"}
                    )
            if res.status_code == requests.codes.ok:
                self.talkToMe(str(res.json()['joke']))
            else:
                self.talkToMe('oops!I ran out of jokes')

        elif 'current weather in' in command:
            reg_ex = re.search('current weather in (.*)', command)
            if reg_ex:
                city = reg_ex.group(1)
                weather = Weather(unit=Unit.CELSIUS)
                location = weather.lookup_by_location('norwich')
                
                condition = location.condition
                self.talkToMe('The Current weather in %s is %s The tempeture is %.1f degree' % (city, condition.text, (int(condition.temp)-32)/1.8))

        elif 'what are you' in command:
            self.talkToMe('ORB advanced adaptive ai, built by Bijan and Richard to dominate the train world and make us very rich')
        elif 'weather forecast in' in command:
            reg_ex = re.search('weather forecast in (.*)', command)
            if reg_ex:
                city = reg_ex.group(1)
                weather = Weather()
                print(weather)
                location = weather.lookup_by_location(city)
                forecasts = location.forecast
                for i in range(0,3):
                    self.talkToMe('On %s will it %s. The maximum temperture will be %.1f degree.'
                            'The lowest temperature will be %.1f degrees.' % (forecasts[i].date(), forecasts[i].text(), (int(forecasts[i].high())-32)/1.8, (int(forecasts[i].low())-32)/1.8))
        return state


def main():

    talk.talkToMe('Hello, i am the ORB A-I. How can i help you?')
    state = True
    #loop to continue executing multiple commands
    while state:
        print(state)
        talk.assistant(talk.audioInput())

if __name__ == "__main__":
    talk = VoiceProcessor()
    main()