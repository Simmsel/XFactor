## main script to run on the raspi

# GPIO PINS
RESET_BUTTON_PIN = 6
SERVO_PIN = 13
LED1_PIN = 17
LED2_PIN = 27
LED3_PIN = 22
LED4_PIN = 5
LEDs = [LED1_PIN, LED2_PIN, LED3_PIN, LED4_PIN]

OPEN_ANGLE = 90
CLOSE_ANGLE = 0




## IMPORT Files

import microphone
import camera
import fingerprint
import rfid
import helpers
import speaker
import led
import motor



## IMPORT Libraries

import tensorflow as tf
import numpy as np
import time
import os
import RPi.GPIO as GPIO




# VARIABLES
Users = ["MoritzG", "MoritzR", "Jonathan", "Nico", "Simon", "Gabriel", "Sonstige"]
current_mode = "READY"
OPEN_TIME = 5 # specified in seconds







# Callback-Funktion für den Knopf-Interrupt

def button_press_callback(channel):
    hold_start = time.time()

    # Check for 5 seconds button press
    while GPIO.input(RESET_BUTTON_PIN) == GPIO.HIGH:
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
    print("Bitte den RFID-Tag an das Lesegerät halten...")
    led.led_control(LEDs[0], GPIO.HIGH)
    first_user = rfid.verify()
    if first_user == "UNKNOWN":
        current_mode = "READY"
        return
    

    # # verification step 2
    # led.led_control(LEDs[1], GPIO.HIGH)
    # next_step_user = fingerprint.verify()
    # if first_user != next_step_user :
    #     current_mode = "READY"
    #     return
    
    # # verification step 3
    # led.led_control(LEDs[2], GPIO.HIGH)
    # next_step_user = camera.verify()
    # if first_user != next_step_user :
    #     current_mode = "READY"
    #     return
    
    # # verification step 4
    # led.led_control(LEDs[3], GPIO.HIGH)
    # next_step_user = microphone.verify()
    # if first_user != next_step_user :
    #     current_mode = "READY"
    #     return


    print("User verified, opening lock...")
    current_mode = "OPENING"




def unlock():

    print("Lock open for 5 secods...")
    motor.open()


    # what to do while box is open
    # speaker.playback(Opening sound) # optionally
    start_time = time.time()

    while time.time() - start_time < OPEN_TIME:
        led.led_blink()
        time.sleep(0.06)

    motor.close()

    global current_mode
    current_mode = "READY"





def main():

    ## Eingabezeile leeren
    helpers.clear_screen()

    # Initializing GPIOs
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RESET_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    led.init_gpio(LED1_PIN)
    led.init_gpio(LED2_PIN)
    led.init_gpio(LED3_PIN)
    led.init_gpio(LED4_PIN)



    ## Initialization of components
    print("Initializing ...")
    rfid.init()
    # fingerprint.init()
    # microphone.init()
    # camera.init()

    ## Start of loop
    global current_mode

    while True:

        if current_mode == "READY":
            # reseting LEDs
            for l in LEDs:
                led.led_control(l, GPIO.LOW)

            current_mode = "VERIFICATION"

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

