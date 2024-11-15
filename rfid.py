# IMPORTS
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

tag_database = {
    1069488694246: "Simon",
    588620194713: "Jonathan",
<<<<<<< HEAD
    932268172086: "Nico",
    108591145915: "MoritzR",
    660828676947: "MoritzG"
=======
>>>>>>> aef3af3cb209eda02aa4fa5ce2ccbd9799fe6d52
}



def init():
    try:
        reader = SimpleMFRC522()
        print("Initialization of RFID-reader was successfull")
        # reader.Close_MFRC522()
        return reader
        
    except Exception as e:
        print(f"Error initializing RFID-reader: {e}")
        return None


def verify():

    reader = SimpleMFRC522()

    tag_id, _ = reader.read()
    #reader.Close_MFRC522()
    if tag_id in tag_database:
        return tag_database[tag_id]
    else:
        GPIO.cleanup()
        return "UNKNOWN"
        
