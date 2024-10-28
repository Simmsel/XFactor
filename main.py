## main script to run on the raspi

## IMPORT Files

import microphone
import camera
import fingerprint
import rfid
import helpers
import motor
import speaker
import led




## IMPORT Libraries

import tensorflow as tf
import numpy as np
import RPi.GPIO as GPIO
import time
import os






# GPIO PINS
BUTTON_PIN = 6
LED1_PIN = 17
LED2_PIN = 27
LED3_PIN = 22
LED4_PIN = 5


# VARIABLES
Users = ["MoritzG", "MoritzR", "Jonathan", "Nico", "Simon", "Gabriel", "Sonstige"]
current_mode = "READY"







# Callback-Funktion für den Knopf-Interrupt

def button_press_callback(channel):
    global current_mode
    if current_mode == "READY":
        print("Button pressed, starting user identification...")
        current_mode = "VERIFICATION"

    elif current_mode == "VERIFICATION":
        hold_start = time.time()
        
        # Check for 5 seconds button press
        while GPIO.input(BUTTON_PIN) == GPIO.LOW:
            if time.time() - hold_start >= 5:
                print("Reboot initiated...")
                
                os.system("sudo reboot")
                return
            time.sleep(0.1)  # Polling-Intervall







def identify():
    global current_mode
    first_user = "Nobody"
    next_step_user = ""

    print("starting verification process...")

    # verification step 1, return value string of user name
    first_user = rfid.verify()
    
    # verification step 2
    next_step_user = camera.verify()
    if first_user != next_step_user :
        current_mode = "READY"
        return
    
    # verification step 3
    next_step_user = microphone.verify()
    if first_user != next_step_user :
        current_mode = "READY"
        return
    
    # verification step 4
    next_step_user = fingerprint.verify()
    if first_user != next_step_user :
        current_mode = "READY"
        return


    print("User verified, opening lock...")
    current_mode = "OPENING"




def unlock():

    print("Lock open for 5 secods...")
    motor.open()
    time.sleep(5)
    motor.close()

    global current_mode
    current_mode = "READY"





def main():

    ## Eingabezeile leeren
    helpers.clear_screen()

    # Initializing GPIOs
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    led.init_gpio(LED1_PIN)
    led.init_gpio(LED2_PIN)
    led.init_gpio(LED3_PIN)
    led.init_gpio(LED4_PIN)



    ## Initialization of components
    print("Initializing ...")
    microphone.init()
    camera.init()
    fingerprint.init()
    rfid.init()



    ## Start of loop
    global current_mode
    while True:

        # optionally go from ready state directly to 
        # current_mode = "VERIFICATION" 
        # and wait for start by RFID etc. instead of the button press

        if current_mode == "READY":
            print("Startup-mode: waiting for press of button...")
            time.sleep(1)

        elif current_mode == "VERIFICATION":
            identify()

        elif current_mode == "OPENING":
            unlock()







if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program terminated manually")
    finally:
        GPIO.cleanup()

