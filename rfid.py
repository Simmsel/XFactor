# https://devdrik.de/pi-mit-rfid-rc522/


# IMPORTS

import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


Users = ["MoritzG", "MoritzR", "Jonathan", "Nico", "Simon", "Gabriel", "Sonstige"]


# example values, insert actual RFID Tag values here
TAG_LISTS = [
    248491346734,
    127346721368,
    120934609721,
    245934175389
]


def init():
    print("Initializing RFID-sensor connection")
    try:
        reader = SimpleMFRC522()
        print("Initialization of RFID-reader was successfull")
        return reader
    except Exception as e:
        print(f"Error initializing RFID-reader: {e}")
        return None

    
def check_rfid_tag(reader, expected_tag_id):
    print("Please present RFID-TAG...")
    while True:
        try:
            # wait for tag and read ID
            tag_id, text = reader.read()
            print(f"Tag ID: {tag_id}, Text: {text.strip()}")

            if tag_id == expected_tag_id:
                print("Right RFID-Tag detected!")
                break
            else:
                print("Wrong RFID-Tag. Please try again.")
        except Exception as e:
            print(f"Error Reading RFID-Tag: {e}")
            time.sleep(1)  # Wait before trying again


def verify():
    detected_user = ""

    reader = SimpleMFRC522()

    print("Please present RFID-TAG...")
    while True:
        try:
            # wait for tag and read ID
            tag_id, text = reader.read()
            print(f"Tag ID: {tag_id}, Text: {text.strip()}")

            if tag_id in TAG_LISTS:
                print("Right RFID-Tag detected!")
                return text
            else:
                print("Wrong RFID-Tag. Please try again.")
        except Exception as e:
            print(f"Error Reading RFID-Tag: {e}")
            time.sleep(0.2)  # Wait before trying again

    return detected_user
