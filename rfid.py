"""
# IMPORTS
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import spidev

tag_database = {
    1069488694246: "Simon",
    588620194713: "Jonathan",
    932268172086: "Nico",
    108591145915: "MoritzR",
    660828676947: "MoritzG"
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
    if tag_id in tag_database: 
        return tag_database[tag_id]
    else:
        return "UNKNOWN"
"""

import RPi.GPIO as GPIO
from mfrc522 import MFRC522
import signal

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted


def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()
    
def verify():

    # Hook the SIGINT
    signal.signal(signal.SIGINT, end_read)

    # Create an object of the class MFRC522
    MIFAREReader = MFRC522.MFRC522()

    # Welcome message
    print("Welcome to the MFRC522 data read example")
    print("Press Ctrl-C to stop.")

    # This loop keeps checking for chips. If one is near it will get the UID and authenticate
    # while continue_reading:

    # Scan for cards
    (status, TagType) = MIFAREReader.Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print("Card detected")

    # Get the UID of the card
    (status, uid) = MIFAREReader.Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        print("Card read UID: " + str(uid[0]) + "," + str(uid[1]) + "," + str(uid[2]) + "," + str(uid[3]))

        # This is the default key for authentication
        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

        # Select the scanned tag
        MIFAREReader.SelectTag(uid)
        data = MIFAREReader.DumpClassic1K_Data(key, uid)

        MIFAREReader.StopCrypto1()

        for block in data:
            b = ""
            for byte in block:
                b += chr(byte)
            print(b)
