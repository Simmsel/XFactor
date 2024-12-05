#Live Umwandulung von Sprache in Text

import speech_recognition as sr

# Funktion für die Spracherkennung
def recognize_speech_once():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("Sprechen Sie etwas (Höre für 5 Sekunden)...")
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)  # Hintergrundgeräusche kalibrieren
            print("Ich höre zu...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)  # Höre für 5 Sekunden
            print("Verarbeite...")
            text = recognizer.recognize_google(audio, language="de-DE")  # Sprache erkennen
            print(f"Sie sagten: {text}")
    except sr.UnknownValueError:
        print("Entschuldigung, ich konnte Sie nicht verstehen.")
    except sr.RequestError as e:
        print(f"Fehler bei der Anfrage: {e}")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

# Hauptprogramm
if __name__ == "__main__":
    # Starte die Spracherkennung einmalig
    recognize_speech_once()

    print("Programm beendet.")
