# IMPORTS
from pyfingerprint.pyfingerprint import PyFingerprint
import time

Users = ["MoritzG", "MoritzR", "Jonathan", "Nico", "Simon", "Gabriel", "Sonstige"]

# Initialize fingerprint sensor
def init():
    try:
        print("Initializing fingerprint sensor connection")
        # Initialize with device path and settings (adjust for your setup)
        f = PyFingerprint('/dev/ttyS0', 57600, 0xFF, 0x01)
        if f.verifyPassword() == False:
            print("Invalid password for fingerprint sensor")
            return None
        print("Initialization successful.")
        return f
    except Exception as e:
        print(f"Error during initialization of fingerprint sensor: {e}")
        return None

# Enroll a new fingerprint at a specified location
def enroll_fingerprint(sensor, location):
    """Enrolls a new fingerprint at the specified location"""
    print("Place your finger on the sensor...")

    # Step 1: Capture fingerprint image
    while not sensor.readImage():
        pass

    # Step 2: Convert the image to a template
    sensor.convertImage(0x01)

    print("Remove your finger...")
    time.sleep(1)  # Pause for finger removal

    # Step 3: Request second image for a matching template
    print("Place the same finger again...")
    while not sensor.readImage():
        pass

    sensor.convertImage(0x02)

    # Step 4: Create a model from the two images
    if sensor.createTemplate() < 0:
        print("Error creating fingerprint model.")
        return False

    # Step 5: Store the model in the specified location
    if not sensor.storeTemplate(location):
        print("Error storing fingerprint.")
        return False

    print(f"Fingerprint enrolled successfully at ID {location}")
    return True

# Function to search for a fingerprint and display user ID
def get_fingerprint(sensor):
    """Searches for a fingerprint and displays the user ID"""
    print("Place your finger on the sensor...")

    # Wait until the fingerprint is detected
    while not sensor.readImage():
        pass

    # Convert the fingerprint image to a template
    sensor.convertImage(0x01)

    # Search for the fingerprint in memory
    result = sensor.searchTemplate()
    position_number = result[0]
    if position_number >= 0:
        print(f"Fingerprint recognized! User ID: {position_number}")
        return True
    else:
        print("Fingerprint not recognized.")
        return False



def verify():
    detected_user = ""
# Main loop to test the sensor
    sensor = init()
    if sensor:
        while True:
            print("Searching for fingerprint...")
            if get_fingerprint(sensor):
                print(f"Fingerprint recognized, ID: {sensor.downloadCharacteristics(0)}")
            else:
                print("Fingerprint not recognized.")
            time.sleep(1)
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
