## main script to run on the raspi

# GPIO PINS
BUTTON_PIN = 26
SERVO_PIN = 13

LED1_PIN = 17   # Yellow1
LED2_PIN = 27   # Yellow2
LED3_PIN = 22   # Yellow3
LED4_PIN = 5    # Yellow4
LED5_PIN = 2    # RED

LEDs = [LED1_PIN, LED2_PIN, LED3_PIN, LED4_PIN, LED5_PIN]

OPEN_ANGLE = 30
CLOSE_ANGLE = 0

PATH_AUDIO = "/home/pi/XFactor/data/Audio/"
PATH_INIT_COMPLETE = "Initilization.wav"
PATH_PRESENT_RFID = "RFID.wav"
PATH_PRESENT_FINGER = "Finger.wav"
PATH_CAMERA = "please look into the came.wav"
PATH_MICROPHONE = "StartVoicerecognition.wav"
PATH_MARIOKART = "mariostart.mp3"
PATH_VOICE_DETECTED = "Voice-Passwort verified 1.wav"
PATH_UNAUTHORIZED = "ALARM - Unauthorized.wav"
PATH_FACEDETECTED = "Your face got successfull.wav"
PATH_DOOR_SOUND = "194325262-open-bank-vault.mp3"
PATH_OPEN = "X-Factor is opening now.wav"
PATH_CLOSE_DOOR = "Please close the Door_Samuel.wav"
PATH_NEW_AUT = "NewAuthentification.wav"


## IMPORT Files

import camera
import fingerprint
# import rfid
import helpers
import speaker
import led
import motor
import microphone


## IMPORT Libraries

import time
import os
import RPi.GPIO as GPIO
from gpiozero import Button


# VARIABLES
current_mode = "READY"
OPEN_TIME = 5 # specified in seconds
ifpressed = 0


# ISR to reboot once button held down
def on_button_held():
    print("Button pressed for 5 seconds, initiating reboot...")
    os.system("sudo reboot")


# ISR if button released
def on_button_released():
    print("Button released.")


# ISR for button pressed
def button_pressed():
    global ifpressed
    ifpressed = 1


# identify loop going through all security steps
def identify():
    
    global current_mode
    first_user = "UNKNOWN"
    next_step_user = ""

    helpers.clear_screen()

    # verification step 1, return value string of user name
    print("Please present your Finger to the fingerprint-sensor...")
    speaker.play_sound( PATH_AUDIO + PATH_PRESENT_FINGER )
    led.led_control(LEDs[0], GPIO.HIGH)
    first_user = fingerprint.verify()
    if first_user == "UNKNOWN":
        led.led_control(LEDs[0], GPIO.LOW)
        led.led_control(LEDs[4], GPIO.HIGH)
        speaker.play_sound( PATH_AUDIO + PATH_UNAUTHORIZED )
        time.sleep(4)
        current_mode = "READY"
        return
    
    print(f"Hello, {first_user}! Please continue with the verification steps.")
    speaker.play_sound( PATH_AUDIO + "hello_" + first_user + ".wav" )
    time.sleep(3)


    ## verification step 2
    led.led_control(LEDs[1], GPIO.HIGH)
    speaker.play_sound( PATH_AUDIO + PATH_MICROPHONE)
    time.sleep
    print("please press the button and start to speak!")
    global ifpressed
    while ifpressed != 1:
        time.sleep(0.1)
    ifpressed = 0
    speaker.play_sound( PATH_AUDIO + PATH_MARIOKART )
    next_step_user = microphone.verify()
    if first_user != next_step_user :
        speaker.play_sound( PATH_AUDIO + PATH_UNAUTHORIZED )
        time.sleep(4)
        current_mode = "READY"
        return
    speaker.play_sound( PATH_AUDIO + PATH_VOICE_DETECTED)
    time.sleep(3)
    
    
    # verification step 3
    led.led_control(LEDs[2], GPIO.HIGH)
    speaker.play_sound( PATH_AUDIO + PATH_CAMERA)
    time.sleep(1)
    next_step_user = camera.verify()

    if first_user != next_step_user :
        speaker.play_sound( PATH_AUDIO + PATH_UNAUTHORIZED )
        current_mode = "READY"
        print("Wrong Face Detected")
        time.sleep(4)
        return
    
    # verification step 4
    """
    next_step_user = rfid.verify()
    if first_user != next_step_user :
        current_mode = "READY"
        print("Wrong RFID Tag")
        return
    """

    led.led_control(LEDs[3], GPIO.HIGH)
    speaker.play_sound( PATH_AUDIO + first_user + ".wav" )
    time.sleep(1)
    speaker.play_sound( PATH_AUDIO + PATH_FACEDETECTED )
    time.sleep(4)

    print("User verified, opening lock...")
    
    speaker.play_sound( PATH_AUDIO + PATH_OPEN )
    time.sleep(3)
    current_mode = "OPENING"


# unlock the safe
def unlock():

    print("Lock open for 5 secods...")
    speaker.play_sound( PATH_AUDIO + PATH_DOOR_SOUND )
    motor.open()

    start_time = time.time()

    while time.time() - start_time < OPEN_TIME:
        led.led_blink()
        time.sleep(0.06)

    motor.close()
    speaker.play_sound( PATH_AUDIO + PATH_CLOSE_DOOR )
    time.sleep(3)
    
    speaker.play_sound( PATH_AUDIO + PATH_NEW_AUT )
    time.sleep(3)
    
    for i in LEDs:
        led.led_control(i, GPIO.HIGH)

    
    global ifpressed
    while ifpressed != 1:
        time.sleep(0.1)
    ifpressed = 0
    global current_mode
    current_mode = "READY"


# main loop
def main():

    helpers.clear_screen()
 
    # Initializing GPIOs
    GPIO.setmode(GPIO.BCM)
    
    led.init_gpio(LED1_PIN)
    led.init_gpio(LED2_PIN)
    led.init_gpio(LED3_PIN)
    led.init_gpio(LED4_PIN)
    led.init_gpio(LED5_PIN)

    button = Button(BUTTON_PIN, pull_up=True, bounce_time=0.2, hold_time=5)
    button.when_held = on_button_held
    button.when_released = on_button_released
    button.when_pressed = button_pressed

    ## Initialization of components
    print("Initializing ...")

    camera.init()
    fingerprint.init()
    # rfid.init()

    speaker.play_sound( PATH_AUDIO + PATH_INIT_COMPLETE )

    ## Start of loop
    global current_mode

    while True:

        if current_mode == "READY":
            # reseting LEDs
            for l in LEDs:
                led.led_control(l, GPIO.LOW)
            
            # RED LED to signal wrong user or boot-up
            led.led_control(LEDs[4], GPIO.HIGH)
            time.sleep(3)
            led.led_control(LEDs[4], GPIO.LOW)
            
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
        camera.camera.stop()
