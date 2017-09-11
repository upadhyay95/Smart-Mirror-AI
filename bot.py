# bot.py
# speechrecognition, pyaudio, brew install portaudio
import sys				
import pygame as pyg			
import threading			
sys.path.append("./")			

import requests				
import datetime				
import dateutil.parser			
import json				
import traceback			
from nlg import NLG			
from speech import Speech		
from knowledge import Knowledge		
from vision import Vision		
from moviepy.editor import *
from moviepy.video.fx.resize import resize
#from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

my_name = "Abhishek"
launch_phrase = "ok mirror"#["okey mirror","ok mirror","okay mirror"]
use_launch_phrase = False
weather_api_token = "5859edf9ce7b6028dab4b3f369e39cfa"
wit_ai_token = "Bearer OT2WJZMM7DEUWONITTHEJCJSJIBVL6EX"
debugger_enabled = True
camera = 0
music_file = "./Channa.mp3"

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


class Bot(object):
    def __init__(self):
        self.nlg = NLG(user_name=my_name) #using the nlg 
        self.speech = Speech(launch_phrase=launch_phrase, debugger_enabled=debugger_enabled) #calling the speech.py file here
        self.knowledge = Knowledge(weather_api_token) #calling the knowledge.py file here
        self.vision = Vision(camera=camera) #checking the camera working through the sision.py

    def start(self):
        """
        Main loop. Waits for the launch phrase, then decides an action.
        :return:
        """
        while True:
            requests.get("http://localhost:8080/clear")  #clearing the screen on the web browser
            speech="Welcome to Smart Mirror !!"
            requests.get("http://localhost:8080/statement?text=%s" % speech) # calling the text to appear on the browser
            self.speech.synthesize_text("hello"+speech)  #synthesizing the text into speech
            speech1="Say The launch Phrase ."   #asking the user to say the lauch phrase
            self.speech.synthesize_text(speech1)   #speaking of the above line,
            if self.vision.recognize_face():       #checking if
                print "Face Found"			#the person is infront of camera
                if use_launch_phrase:			#checking whether to use the launch phrase or not
                    recognizer, audio = self.speech.listen_for_audio()		#initializing
                    if self.speech.is_call_to_action(recognizer, audio):	#checking if the audio is recognized
                        self.__acknowledge_action()			#if it is recognized take action
                        self.decide_action()			#deciding which action to be taken
                else:
                    self.decide_action()			#printing the else part

    def decide_action(self):					#defining the function to decide the action 
        """
        Recursively decides an action based on the intent.
        :return:
        """
        recognizer, audio = self.speech.listen_for_audio()		#listening for the audio

        # received audio data, now we'll recognize it using Google Speech Recognition
        speech = self.speech.google_speech_recognition(recognizer, audio)	#storing the speech into variable as a text

        if speech is not None:		#if speech is not recognized
            try:
                req = requests.get('https://api.wit.ai/message?v=20160918&q=%s' % speech,
                                 headers={"Authorization": wit_ai_token})		#getting the wit.ait token and checking it
                print req.text			#printing the text
                json_responce = json.loads(req.text)		#printing the responce
                entities = None			#inititaling the entities
                intent = None			#initialising the intent
                if 'entities' in json_responce and 'Intent' in json_responce['entities']:	#checking the the intents and entitites
                    entities = json_responce['entities']		#entities 
                    intent = json_responce['entities']['Intent'][0]["value"]	#intents 

                print intent	#printing the intents
                if intent == 'greeting':	#checking the intent type
                    self.__text_action(self.nlg.greet())    #getting the function of the intent
                elif intent == 'snow white':		#checking the intent type
                    self.__text_action(self.nlg.snow_white())		#getting the function of the intent
                elif intent == 'weather':		#checking the intent type
                    self.__weather_action(entities)	#getting the function of the intent
                elif intent == 'news':			#checking the intent type
                    self.__news_action()	#getting the function of the intent
                elif intent == 'maps':			#getting the function of the intent
                    self.__maps_action(entities)		#getting the function of the intent#checking the intent type
                elif intent == 'holidays':		#getting the function of the intent#checking the intent type
                    self.__holidays_action()			#getting the function of the intent#checking the intent type
                elif intent == 'appearance':		#getting the function of the intent#checking the intent type
                    self.__appearance_action()		#getting the function of the intent#checking the intent type
                elif intent == 'user status':		#getting the function of the intent#checking the intent type
                    self.__user_status_action(entities)		#getting the function of the intent#checking the intent type
                elif intent == 'user name':			#getting the function of the intent#checking the intent type
                    self.__user_name_action()			#getting the function of the intent#checking the intent type
                elif intent == 'personal status':		#getting the function of the intent#checking the intent type
                    self.__personal_status_action()		#getting the function of the intent#checking the intent type
                elif intent == 'joke':			#getting the function of the intent#checking the intent type
                    self.__joke_action()		#getting the function of the intent#checking the intent type
                elif intent == 'insult':		#getting the function of the intent#checking the intent type
                    self.__insult_action()	#getting the function of the intent#checking the intent type
                    return				#retuning
                elif intent == 'appreciation':			#getting the function of the intent#checking the intent type
                    self.__appreciation_action()			#getting the function of the intent#checking the intent type
                    return
                elif intent == 'music':			#getting the function of the intent#checking the intent type
                    self.__music_action(music_file)		#getting the function of the intent#checking the intent type
                elif intent == 'navigation':			#getting the function of the intent#checking the intent type
                    self.__navigate_action()
                elif intent == 'tasks':
                    self.__calender_events()
		elif intent == 'guide':
                    self.__guide()
                elif intent == 'web':
                    self.__web()
                elif intent == 'video':
                    self.__video()
                else: # No recognized intent
                    self.__text_action("I'm sorry, I don't know about this yet.")
                    return

            except Exception as e:
                print "Failed wit !"			#error message
                print(e)			#printing the error
                traceback.print_exc()
                self.__text_action("I'm sorry, I couldn't understand what you mean !!")  #printing message
                return				

            self.decide_action()

    def __joke_action(self):			#joke
        joke = self.nlg.joke()				#function

        if joke is not None:			#finding if the intent is joke
            self.__text_action(joke)		#calling the joke function
        else:		#printin else
            self.__text_action("I couldn't find any of the jokes")	

    def __user_status_action(self, nlu_entities=None):	#user status
        attribute = None		

        if (nlu_entities is not None) and ("Status_Type" in nlu_entities):
            attribute = nlu_entities['Status_Type'][0]['value']

        self.__text_action(self.nlg.user_status(attribute=attribute))

    def __user_name_action(self):		#name actions
        if self.nlg.user_name is None:
            self.__text_action("I don't know your name yet. You can configure it in bot.py")

        self.__text_action(self.nlg.user_name)		#calling of the name

    def __appearance_action(self):
        text_speech="This Application is developed by Abhishek, Veekas , Darshan And Ashwini"
        self.speech.synthesize_text(text_speech)
        requests.get("http://localhost:8080/face")		#showing of the face

    def __appreciation_action(self):
        self.__text_action(self.nlg.appreciation())		#appriciation

    def __acknowledge_action(self):
        self.__text_action(self.nlg.acknowledge())		#acknolege

    def __insult_action(self):
        self.__text_action(self.nlg.insult())		#insulting

    def __personal_status_action(self):
        self.__text_action(self.nlg.personal_status())		#personnel status

    def __text_action(self, text=None):
        if text is not None:	
            requests.get("http://localhost:8080/statement?text=%s" % text)		#printing it on screen
            self.speech.synthesize_text(text)

    def __news_action(self):
        headline = self.knowledge.get_news()		#getting the news

        if headline:
            requests.post("http://localhost:8080/news", data=json.dumps({"articles":headline}))	#headlines
            self.speech.synthesize_text(self.nlg.news("past"))	
            interest = self.nlg.article_interest(headline)	#headlines
            if interest is not None:
                self.speech.synthesize_text(interest)
        else:
            self.__text_action("I am facing some issues in finding news for you at this moment!!")

    def __weather_action(self, nlu_entities=None):

        current_dtime = datetime.datetime.now()			#displayin the current time and date
        skip_weather = False # used if we decide that current weather is not important

        weather_obj = self.knowledge.find_weather()	#finding the weather
        temperature = weather_obj['temperature']	#temp
        icon = weather_obj['icon']			#icon
        wind_speed = weather_obj['windSpeed']		#windspeed

        weather_speech = self.nlg.weather(temperature, current_dtime, "present")	#present status
        forecast_speech = None	#init

        if nlu_entities is not None:
            if 'datetime' in nlu_entities:
                if 'grain' in nlu_entities['datetime'][0] and nlu_entities['datetime'][0]['grain'] == 'day':	#displaying of date and 
                    dtime_str = nlu_entities['datetime'][0]['value'] # 2016-09-26T00:00:00.000-07:00 --
                    dtime = dateutil.parser.parse(dtime_str)
                    if current_dtime.date() == dtime.date(): # hourly weather---
                        forecast_obj = {'forecast_type': 'hourly', 'forecast': weather_obj['daily_forecast']}
                        forecast_speech = self.nlg.forecast(forecast_obj) #forcasting the weather objects
                    elif current_dtime.date() < dtime.date(): # sometime in the future ... get the weekly forecast or handle specific days
                        forecast_obj = {'forecast_type': 'daily', 'forecast': weather_obj['weekly_forecast']}
                        forecast_speech = self.nlg.forecast(forecast_obj)	#speech of the weather
                        skip_weather = True
            if 'Weather_Type' in nlu_entities:
                weather_type = nlu_entities['Weather_Type'][0]['value']
                print weather_type
                if weather_type == "current":
                    forecast_obj = {'forecast_type': 'current', 'forecast': weather_obj['current_forecast']}
                    forecast_speech = self.nlg.forecast(forecast_obj)
                elif weather_type == 'today':
                    forecast_obj = {'forecast_type': 'hourly', 'forecast': weather_obj['daily_forecast']}
                    forecast_speech = self.nlg.forecast(forecast_obj)
                elif weather_type == 'tomorrow' or weather_type == '3 day' or weather_type == '7 day':
                    forecast_obj = {'forecast_type': 'daily', 'forecast': weather_obj['weekly_forecast']}
                    forecast_speech = self.nlg.forecast(forecast_obj)
                    skip_weather = True


        weather_data = {"temperature": temperature, "icon": icon, 'windSpeed': wind_speed, "hour": datetime.datetime.now().hour}
        requests.post("http://localhost:8080/weather", data=json.dumps(weather_data))

        if not skip_weather:
            self.speech.synthesize_text(weather_speech)

        if forecast_speech is not None:
            self.speech.synthesize_text(forecast_speech)

    def __maps_action(self, nlu_entities=None):

        location = None
        map_type = None
        if nlu_entities is not None:
            if 'location' in nlu_entities:
                location = nlu_entities['location'][0]["value"]
            if "Map_Type" in nlu_entities:
                map_type = nlu_entities['Map_Type'][0]["value"]

        if location is not None:
            maps_url = self.knowledge.get_map_url(location, map_type)
            maps_action = "Sure. Here is a map of %s." % location
            body = {'url': maps_url}
            requests.post("http://localhost:8080/image", data=json.dumps(body))
            self.speech.synthesize_text(maps_action)
        else:
            self.__text_action("I'm sorry, I couldn't understand what location you wanted.")

    def __holidays_action(self):
        holidays = self.knowledge.get_holidays()
        next_holiday = self.__find_next_holiday(holidays)
        requests.post("http://localhost:8080/holidays", json.dumps({"holiday": next_holiday}))
        self.speech.synthesize_text(self.nlg.holiday(next_holiday['localName']))

    def __find_next_holiday(self, holidays):
        today = datetime.datetime.now()
        for holiday in holidays:
            date = holiday['date']
            if (date['day'] > today.day) and (date['month'] > today.month):
                return holiday

        # next year
        return holidays[0]
    def __music_action(self,music_file):
        freq = 44100     # audio CD quality setting
        bitsize = -16    # unsigned 16 bit bit size
        channels = 2     # 1 is mono, 2 is stereo ,we are selecting for stereo
        buffer = 2048    # number of samples (experiment to get best sound)
        pyg.mixer.init(freq, bitsize, channels, buffer)		#mixing it
        #pg.mixer.music.set_volume(volume)
        clock = pyg.time.Clock()			#for checking of the time elasped in the song
        try:
            pyg.mixer.music.load(music_file)		#loading of the file
            print("Music file {} loaded successfully!".format(music_file))
            m="ok , i am playing a music for you !!"
            requests.get("http://localhost:8080/statement?text=%s" % m)
            self.speech.synthesize_text(m)
        except pyg.error:
            print("File {} not found ,i am sorry ! ({})".format(music_file, pg.get_error()))
            return
        pyg.mixer.music.play()				#playing of the music
        while pyg.mixer.music.get_busy():		#checking if the music is over
            # check if playback has finished
            clock.tick(30)
    def __navigate_action(self):
        speech="I have opened the navigation application for you !!"
        requests.get("http://localhost:8080/statement?text=%s" % speech) # calling the text to appear on the browser
        self.speech.synthesize_text(speech)
        source1="Please let me know the source of your navigation"
        self.speech.synthesize_text(source1)
        recognizer, audio = self.speech.listen_for_audio()
        source = self.speech.google_speech_recognition(recognizer, audio)
        destination1="Please let me know the destination of your navigation"
        self.speech.synthesize_text(destination1)
        recognizer, audio = self.speech.listen_for_audio()
        destination = self.speech.google_speech_recognition(recognizer, audio) #listening for the destination
        self.speech.synthesize_text("Source is "+source) #speaks the source
        url="http://localhost:8080/statement?text=source : "+source+", destination : "+destination  
        requests.get(url) # calling the text to appear on the browser
        self.speech.synthesize_text("Destination is "+destination) #speaks the destination
        #http://maps.googleapis.com/maps/api/staticmap?center=%s&zoom=13&scale=false&size=1200x600&maptype=roadmap&format=png
        maps_url = "http://maps.googleapis.com/maps/api/staticmap?center=%s&zoom=13&scale=false&size=1200x600&maptype=roadmap&format=png" % source
        maps_action = "Sure. Here is a map of %s." % source
        body = {'url': maps_url}
        requests.post("http://localhost:8080/image", data=json.dumps(body))
        self.speech.synthesize_text(maps_action)
##################################
    def __calender_events(self):
        """this is the use of google calender api to display the upcoming 
           latest calender events of the user .. !!
           we can call upto a number of events here we are restricting it to 5.
        """
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        pt="Getting the upcoming latest events"
        requests.get("http://localhost:8080/statement?text=%s" % pt)
        self.speech.synthesize_text(pt)
        eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=1, singleEvents=True,
        orderBy='startTime').execute()
        events = eventsResult.get('items', [])

        if not events:
            pq="No upcoming events found."
            requests.get("http://localhost:8080/statement?text=%s" % pt)
            self.speech.synthesize_text(pq)
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            #start1=''.join(start)
            summary=event['summary']
            print start,summary
            requests.get("http://localhost:8080/statement?text="+start+"  "+summary)
    def __guide(self):
        guide="This project is done under the guidence of Dr. Nandini Prasad."
        self.speech.synthesize_text(guide)
        maps_url = "https://scontent.fblr4-1.fna.fbcdn.net/v/t1.0-9/575151_3352748596658_894671435_n.jpg?oh=16368cb6caa6c2ae21c6033e6b00e8b8&oe=59526F09"
        #maps_url = "www.dr-ait.org"
        body = {'url': maps_url}
        requests.post("http://localhost:8080/guide", data=json.dumps(body))
    def __web(self):
        r = requests.get('http://www.google.com/')
        print r.content
        '''web_site="Opening Doctor Ambedkar Institute Of Technology Website !!"
        self.speech.synthesize_text(web_site)
        maps_url = "www.dr-ait.org"
        body = {'url': maps_url}
        requests.post("http://localhost:8080/", data=json.dumps(body))'''
    def __video(self):
        pyg.display.set_caption("Abhishek's Test Video !!")

        clip = VideoFileClip('video.mp4')
        clip.resize(width=1200).preview()
        pyg.quit()
        
if __name__ == "__main__":
    bot = Bot()
    bot.start()
