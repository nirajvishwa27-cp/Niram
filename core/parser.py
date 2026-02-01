from rapidfuzz import process, utils

class CommandParser:
    def __init__(self):
        # Define the 'Intent Map'
        # Key: The internal command name
        # Value: List of phrases that mean that command
        self.intent_map = {
            "SEARCH": ["search for", "find", "google search", "look up"],
            "NAVIGATE": ["open", "go to", "launch", "visit", "take me to"],
            "SCROLL_DOWN": ["scroll down", "move down", "lower"],
            "SCROLL_UP": ["scroll up", "move up", "higher"],
            "SCREENSHOT": ["screenshot", "capture screen", "take a snap", "save image"],
            "EXIT": ["exit", "stop", "close niram", "goodbye", "shutdown"]
        }

    def parse(self, text):
        if not text:
            return None, None

        text = text.lower().strip()
        
        # We check each intent group to see if any phrase matches the user input
        best_intent = "UNKNOWN"
        highest_score = 0
        
        for intent, phrases in self.intent_map.items():
            # extractOne finds the closest match in the list of phrases
            result = process.extractOne(text, phrases, processor=utils.default_process)
            if result:
                match_text, score, index = result
                if score > 70 and score > highest_score:
                    highest_score = score
                    best_intent = intent

        # Extracting the "Argument" (e.g., in "open google", "google" is the argument)
        argument = None
        if best_intent == "NAVIGATE":
            # Remove the trigger words to find the website name
            for word in self.intent_map["NAVIGATE"]:
                if text.startswith(word):
                    argument = text.replace(word, "").strip()
                    break
        
        return best_intent, argument