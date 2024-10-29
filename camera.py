import time
import picamera
import numpy as np
import tensorflow as tf

## FaceNet ( Google) -> might be good for face recognition


Users = ["MoritzG", "MoritzR", "Jonathan", "Nico", "Simon", "Gabriel", "Sonstige"]



def init():
    print("Initializing camera connection")
    try:
        # create camera-instance
        camera = picamera.PiCamera()
        camera.start_preview()  # show preview
        print("Initialization of camera was successfull.")
        time.sleep(2)  # hold preview for 2 seconds
        return camera
    except Exception as e:
        print(f"Camera could not be initialized: {e}")
        return None
    
def take_picture(camera, filename='image.jpg'):
    if camera is not None:
        camera.capture(filename)  # take picture
        print(f"Picture saved as: {filename}")
    else:
        print("Camera not initialized. Picture unsuccessfull.")




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
