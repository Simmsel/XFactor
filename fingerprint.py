from pyfingerprint.pyfingerprint import PyFingerprint
import time
import serial
import RPi.GPIO as GPIO

fingerprint_database = [
    "FingerprintTemplate",
    "Jonathan", # ID 1 right pointy finger 
    "Jonathan", # ID 2 right tumb
    "Jonathan", # ID 3 left pointy finger
    "Jonathan", # ID 4 right tumb
    "Simon", # ID5 right index
    "Simon", #ID6 right index
    "Simon", #ID7 right thumb
    "Simon", #ID8 left index
    "MoritzG", #ID9 right thumb
    "MoritzG", #ID10 right thumb
    "MoritzG", #ID11 right index
    "MoritzG", #ID12 right index
    "Nico", #ID13 right thumb
    "Nico", #ID14 right thumb
    "Nico", #ID15 right index
    "Nico", #ID16 right index
    "MoritzR", #ID17 right thumb
    "MoritzR", #ID18 right thumb
    "MoritzR", #ID19 right index
    "MoritzR", #ID20 right index
    "Gabriel", 
    "Sonstige"]


# Initialize fingerprint sensor
def init():
    try:
        print("Initializing fingerprint sensor connection")
        # Initialize with device path and settings
        sensor = PyFingerprint('/dev/serial0', 57600,  0xFFFFFFFF, 0x00000000)
        if not sensor.verifyPassword():
            print("Invalid password for fingerprint sensor")
            return None
        print("Initialization successful.")
        return sensor
    except Exception as e:
        print(f"Error during initialization of fingerprint sensor: {e}")
        return None


# Enroll a new fingerprint at a specified location
def enroll(sensor,location):        
    try: 
        print(f"{sensor}")
        print("Place your finger on the sensor...")
        # Step 1: Capture fingerprint image
        while not sensor.readImage():
            print("Ich seh keinen finger du spasst")
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
    except Exception as e:
            print(f"Error during initialization of fingerprint sensor: {e}")
            return None

 
# Function to search for a fingerprint and display user ID
def get(sensor, fingerprint_database):

    print("Place your finger on the sensor...")

    # Wait until the fingerprint is detected
    while not sensor.readImage():
        pass

    # Convert the fingerprint image to a template
    sensor.convertImage(0x01)

    # Search for the fingerprint in memory
    result = sensor.searchTemplate()
    position_number = result[0]
    confidence = result[1]

    if position_number > 0:
        user_name = fingerprint_database[position_number] if position_number < len(fingerprint_database) else "Unknown User"
        print(f"Fingerprint recognized! User: {user_name}, with confidence: {confidence}")
        return user_name
    else:
        print("Fingerprint not recognized.")
        return False


# Read a fingerprint and verify the user
def verify():
    GPIO.setmode(GPIO.BCM)
    ser = serial.Serial('/dev/serial0', 57600,  timeout=1)    
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    try: 
        data = ser.read(10)
        print(data)

    finally: 
        ser.close()
        ser.open() 
    
    global fingerprint_database

    sensor = PyFingerprint('/dev/serial0', 57600,  0xFFFFFFFF, 0x00000000)    
    
    if sensor:
        while True:
            print("Searching for fingerprint...")
            user_name = get(sensor, fingerprint_database)
            if user_name:
                print(f"Welcome, {user_name}!")
                return user_name
            else:
                print("Fingerprint not recognized.")
