import re
import pyttsx3


def speak_story(story: str):
    # Strip section labels like [SETUP], [TITLE] etc. before reading
    clean = re.sub(r'\[.*?\]', '', story).strip()

    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # default is ~200, 150 is slow and it will be calm for kids
    engine.say(clean)
    engine.runAndWait()