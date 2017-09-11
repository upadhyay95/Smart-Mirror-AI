# speech.py
# speechrecognition, pyaudio, brew install portaudio
import speech_recognition as sr
import os
import requests
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play


class Speech(object):
    def __init__(self, launch_phrase="mirror mirror", debugger_enabled=False):
        self.launch_phrase = launch_phrase
        #self.launch_phrase = " ".join(launch_phrase)
        self.debugger_enabled = debugger_enabled
        self.__debugger_microphone(enable=False)

    def google_speech_recognition(self, recognizer, audio):
        speech = None
        try:
            speech = recognizer.recognize_google(audio)
            print("Google Speech Recognition thinks you said : " + speech)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service at this time; {0}".format(e))

        return speech

    def listen_for_audio(self):
        # obtain audio from the microphone
        r = sr.Recognizer()
        m = sr.Microphone()
        with m as source:
            r.adjust_for_ambient_noise(source)
            self.__debugger_microphone(enable=True)
            print "I'm listening To You"
            audio = r.listen(source)

        self.__debugger_microphone(enable=False)
        print "Audio Found"
        return r, audio

    def is_call_to_action(self, recognizer, audio):
        speech = self.google_speech_recognition(recognizer, audio)
        speech1=["ok mirror","okey mirror","okay mirror","ohk mirror","okie mirror","ok miror"]
        if speech is not None and speech in speech1:
            return True

        return False

    def synthesize_text(self, text):
        tts = gTTS(text=text, lang='en')
        tts.save("tmp.mp3")
        song = AudioSegment.from_mp3("tmp.mp3")
        play(song)
        os.remove("tmp.mp3")

    def __debugger_microphone(self, enable=True):
        if self.debugger_enabled:
            try:
                r = requests.get("http://localhost:8080/microphone?enabled=%s" % str(enable))
                if r.status_code != 200:
                    print("Used wrong endpoint for microphone debugging")
            except Exception as e:
                print(e)
