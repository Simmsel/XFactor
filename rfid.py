# Student card IDs
# MoritzG
# MoritzR
# Gabriel

# IMPORTS

import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


tag_database = {
    1069488694246: "Simon",
    588620194713: "Jonathan",
    932268172086: "Nico"
}



def init():
    print("Initializing RFID-sensor connection")
    try:
        reader = SimpleMFRC522()
        print("Initialization of RFID-reader was successfull")
        return reader
    except Exception as e:
        print(f"Error initializing RFID-reader: {e}")
        return None


def verify():
    print("Bitte den RFID-Tag an das Lesegerät halten...")
    reader = SimpleMFRC522()
    # Lese die Tag-Nummer ein
    tag_id, _ = reader.read()
    print(f"Tag-ID: {tag_id}")
    
    # Überprüfe, ob die Tag-ID in der Datenbank ist
    if tag_id in tag_database:
        return tag_database[tag_id]
    else:
        return "Unbekannter Tag"
