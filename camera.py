from picamera2 import Picamera2
from datetime import datetime
import os

## FaceNet ( Google) -> might be good for face recognition


Users = ["MoritzG", "MoritzR", "Jonathan", "Nico", "Simon", "Gabriel", "Sonstige"]

def init():

    camera = Picamera2()
    config = camera.create_still_configuration()
    camera.configure(config)
    camera.start()
    print("Camera initialization successfull")
    return camera


def take_picture(save_path="~/Desktop/Pictures"):
    # Kamera initialisieren oder Fehler ausgeben, falls Kamera nicht verfügbar
    camera = init()
    if camera is None:
        raise RuntimeError("Camera not available")

    # ensure path is available
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(save_path, f"Pic_{timestamp}.jpg")

    # take picture and save
    camera.capture_file(file_path)
    print(f"Picture saved under: {file_path}")
    
    # stop camera
    camera.stop()
    return file_path


def delete_picture(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


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
