# IMPORTS
from pyfingerprint.pyfingerprint import PyFingerprint
import time


Users = ["MoritzG", "MoritzR", "Jonathan", "Nico", "Simon", "Gabriel", "Sonstige"]


def init():
    try:
        print("Initializing fingerprint sensor connection")
        f = PyFingerprint('/dev/ttyS0', 57600, 0xFF, 0x01)  # Die Parameter können je nach Konfiguration variieren
        if f.verifyPassword() == False:
            print("Invalid password for fingerprint sensor")
            return None
        print("Initialization successfull.")
        return f
    except Exception as e:
        print(f"Error during initialization of fingerprint sensor: {e}")
        return None


def read_finger(sensor):
    print("Please put Finger on Sensor...")
    while True:
        try:
            # Wait for finger to be detected
            if sensor.readImage() == False:
                continue
            
            sensor.convertImage(0x01)
            result = sensor.searchTemplate()

            if result[0] >= 0:
                print(f"Fingerprint detected! ID: {result[0]}")
                break
            else:
                print("Fingerabdruck not detected. Please try again.")
                time.sleep(1)  # Wait before trying again
        except Exception as e:
            print(f"Error reading fingerprint: {e}")
            time.sleep(1)



def verify():
    detected_user = ""

    ## do verification here
    #
    #
    #
    #
    #
    #
    #
    #
    #


    return detected_user
