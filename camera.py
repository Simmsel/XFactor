from picamera2 import Picamera2
from datetime import datetime
import os

## FaceNet ( Google) -> might be good for face recognition


Users = ["MoritzG", "MoritzR", "Jonathan", "Nico", "Simon", "Gabriel", "Sonstige"]
camera = Picamera2()


def init():
    
    global camera

    
    if camera is None:
        raise RuntimeError("Camera not available")
    try:
        config = camera.create_still_configuration()
        camera.configure(config)
        camera.start()
        print("camera initialization successfull")
    except:
        print("Error during Initilization of camera")
        

def take_picture(save_path="/home/pi/XFactor/data/Pictures/"):
    
    global camera

    camera.start()


    if save_path.endswith(".jpg"):
        file_path = save_path
    else:
        # create filename with timestamp and ending
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(save_path, f"Pic_{timestamp}.jpg")

    # take picture and save
    camera.capture_file(file_path)
    # print(f"Picture saved under: {file_path}")
    
    # stop camera
    return file_path


def delete_picture(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def make_dataset(path, set_size = 20):
    
    # required LED imports
    from main import LEDs
    import RPi.GPIO as GPIO
    import led
    import time
    
    # led setup
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    for l in LEDs:
            led.init_gpio(l)
    
    if path == None:
        print("please specify a path!")
        return
               
    if not os.path.exists(path):
        os.makedirs(path)
    
    print("collection of dataset begins shortly")
    time.sleep(3)
    
    for i in range(1, set_size):
        
        # make all lights off
        for l in LEDs:
            led.led_control(l)
        
        # count down for lights on
        for l in LEDs:
            time.sleep(0.5)
            led.led_control(l, GPIO.HIGH)
            
        time.sleep(0.6)
        
        file_path = os.path.join(path, f"Pic_{i}.jpg")
        take_picture(file_path)
        
        # make all lights off
        for l in LEDs:
            led.led_control(l)
        time.sleep(0.3)
        
        # make all lights on
        for l in LEDs:
            led.led_control(l, GPIO.HIGH)
        time.sleep(0.3)
        
        # make all lights off
        for l in LEDs:
            led.led_control(l)
        time.sleep(0.3)
            
        # make all lights on
        for l in LEDs:
            led.led_control(l, GPIO.HIGH)
        time.sleep(0.3)
        
        print(f"Progress: {i} / {set_size}")


def verify():
    detected_user = ""
    
    picture = take_picture()
    
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
    #



    # optionally keep picture if inncorrect to find intruder?
    delete_picture(picture) 
    
    return detected_user
    
    
if __name__ == "__main__":
    init()


