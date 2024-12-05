#Live Umwandulung von Sprache in Text

import speech_recognition as sr
from pynput import keyboard

# Variable, um das Programm zu steuern
stop_listening = False

# Funktion, um die "q"-Taste zu überwachen
def on_press(key):
    global stop_listening
    try:
        if key.char == 'q':  # Wenn die Taste "q" gedrückt wird
            stop_listening = True
            return False  # Stoppt den Listener
    except AttributeError:
        pass

# Funktion für die Spracherkennung
def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("Sprechen Sie etwas (Drücken Sie 'q', um zu beenden)...")
    while not stop_listening:
        try:
            with mic as source:
                recognizer.adjust_for_ambient_noise(source)  # Hintergrundgeräusche kalibrieren
                print("Ich höre zu...")
                audio = recognizer.listen(source, timeout=10)  # Höre Sprache mit Timeout
                print("Verarbeite...")
                text = recognizer.recognize_google(audio, language="de-DE")  # Sprache erkennen
                #text = recognizer.recognize_google(audio, language="en-GB")  # Sprache erkennen
                print(f"Sie sagten: {text}")
        except sr.UnknownValueError:
            print("Entschuldigung, ich konnte Sie nicht verstehen.")
        except sr.RequestError as e:
            print(f"Fehler bei der Anfrage: {e}")
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")

# Hauptprogramm
if __name__ == "__main__":
    # Starte den Tastatur-Listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    # Start der Spracherkennung
    recognize_speech()

    print("Programm beendet.")
