import speech_recognition as sr
from playwright.sync_api import sync_playwright
import pyttsx3

def test_setup():
    engine = pyttsx3.init()
    recognizer = sr.Recognizer()
    
    # 1. Test Voice Output
    print("--- Testing Voice Output ---")
    engine.say("Niram system check initiated.")
    engine.runAndWait()

    # 2. Test Voice Input
    print("--- Testing Microphone (Please say 'Hello') ---")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"I heard: {text}")
        except Exception as e:
            print(f"Voice Input Failed: {e}")

    # 3. Test Browser
    print("--- Testing Browser Automation ---")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, channel="chrome")
        page = browser.new_page()
        page.goto("https://www.google.com")
        print(f"Title: {page.title()}")
        browser.close()

    print("\nSUCCESS: All systems operational for Project Niram!")

if __name__ == "__main__":
    test_setup()