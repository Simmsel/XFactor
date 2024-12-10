import speech_recognition as sr
import time
LANGUAGE = "en-GB" 
# LANGUAGE = "de-DE"
DURATION = 10


text_database = {
    "what's the craic": "Simon",
    "give me your money": "Jonathan",
    "Belfast 24": "Nico",
    "hello mate": "MoritzR",
    "please open the box": "MoritzG"
}

    
def verify():
    
    text = recognize_speech()

    print(text)
    if not text:
        text = "Unknown"
    
    stripped_text = text.strip()
    
    if text in text_database: 
        print(f"person {text_database[stripped_text]} was detected")
        return text_database[stripped_text]
    else:
        return "UNKNOWN"


def recognize_speech():
    time.sleep(3.3)
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("Say something (listening for 5 seconds)...")
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)  # calibrate background noise
            print("I'm listening...")
            audio = recognizer.listen(source, timeout=DURATION, phrase_time_limit=DURATION)  # Listen for 5 seconds
            print("Processing...")
            text = recognizer.recognize_google(audio, language=LANGUAGE)  # recognize speech
            print(f"You said: {text}")
            return text
    except sr.UnknownValueError:
        print("Sorry, I could'nt understand you.")
    except sr.RequestError as e:
        print(f"Error resolving: {e}")
    except Exception as e:
        print(f"An error has occured: {e}")
