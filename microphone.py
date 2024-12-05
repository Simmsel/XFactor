import speech_recognition as sr
import time
LANGUAGE = "en-GB" 
# LANGUAGE = "de-DE"
DURATION = 10



text_database = {
    "what's the craic": "Simon",
    "give me your money": "Jonathan",
    "": "Nico",
    "hello mate": "MoritzR",
    "please open the box": "MoritzG"
}

def init():
    return
    
    


    
def verify():
    
    # bla bla code to determine user
    
    text = recognize_speech()
    #lastsign_text = text[-1]
    #print(f"das letzte Zeichen ist:{lastsign_text}")
    print(text)
    if not text:
        text = "Unknown"
    
    stripped_text = text.strip()
    
    if text in text_database: 
        print(f"person {text_database[stripped_text]} wurde erkannt")
        return text_database[stripped_text]
    else:
        return "UNKNOWN"



# Funktion für die Spracherkennung
def recognize_speech():
    time.sleep(3.3)
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("Sprechen Sie etwas (Höre für 5 Sekunden)...")
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)  # Hintergrundgeräusche kalibrieren
            print("Ich höre zu...")
            audio = recognizer.listen(source, timeout=DURATION, phrase_time_limit=DURATION)  # Höre für 5 Sekunden
            print("Verarbeite...")
            text = recognizer.recognize_google(audio, language=LANGUAGE)  # Sprache erkennen
            print(f"Sie sagten: {text}")
            return text
    except sr.UnknownValueError:
        print("Entschuldigung, ich konnte Sie nicht verstehen.")
    except sr.RequestError as e:
        print(f"Fehler bei der Anfrage: {e}")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
