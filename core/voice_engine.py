import speech_recognition as sr
import pyttsx3
import os

class VoiceEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # Initial setup
        self.setup_voice()

    def setup_voice(self):
        # Using 'nsss' driver explicitly for Mac stability
        try:
            self.engine = pyttsx3.init(driverName='nsss')
            self.engine.setProperty('rate', 180)
            self.engine.setProperty('volume', 1.0)
        except Exception as e:
            print(f"Voice init error: {e}")

    def speak(self, text):
        print(f"Niram: {text}")
        # On Mac, sometimes the engine needs a fresh start to "wake up" the audio driver
        try:
            # We use a simpler call for the main loop to prevent thread-locking
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            # Fallback to system 'say' command if pyttsx3 fails (Mac Only)
            os.system(f'say "{text}"')

    def listen_continuous(self):
        with sr.Microphone() as source:
            # OPTIMIZATION: Faster silence detection
            self.recognizer.pause_threshold = 0.7  # Default is 0.8
            self.recognizer.non_speaking_duration = 0.4
            
            # Reduce ambient noise adjustment time
            self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
            
            print("\n(Listening...)")
            try:
                # phrase_time_limit stops the 'infinite listen' lag
                audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=4)
                
                # Use recognizer.recognize_google(audio)
                command = self.recognizer.recognize_google(audio)
                return command.lower()
            except Exception:
                return None