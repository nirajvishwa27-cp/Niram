import asyncio
import os
from core.parser import CommandParser
from core.voice_engine import VoiceEngine
from core.controller import BrowserManager

async def main():
    # Initialize components
    voice = VoiceEngine()
    browser = BrowserManager()
    parser = CommandParser()
    
    voice.speak("System Niram is online and ready.")
    
    # Launch browser and get the active page
    page = await browser.launch()

    voice.speak("Niram is ready for commands.")
    page = await browser.launch()

    while True:
        command_text = voice.listen_continuous()
        if not command_text:
            continue
            
        print(f"User heard: {command_text}")
        
        # Use the ML-lite Fuzzy Parser
        intent, arg = parser.parse(command_text)
        
        if intent == "NAVIGATE" and arg:
            url = f"https://{arg}.com" if "." not in arg else f"https://{arg}"
            voice.speak(f"Navigating to {arg}")
            await page.goto(url)

        elif intent == "SCROLL_DOWN":
            await page.mouse.wheel(0, 600)

        elif intent == "SCREENSHOT":
            # ... (your existing screenshot logic)
            voice.speak("Taking a snap.")
            await page.screenshot(path="assets/snap.png")
            
        elif intent == "SEARCH" and arg:
            voice.speak(f"Searching for {arg}")
            search_url = f"https://www.google.com/search?q={arg}"
            await page.goto(search_url)

        elif intent == "EXIT":
            voice.speak("Shutting down.")
            break
            
        elif intent == "UNKNOWN":
            print("Niram: I didn't quite catch that intent.")

    await browser.shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nManual Exit.")