## main script to run on the raspi

# GPIO PINS
BUTTON_PIN = 26
SERVO_PIN = 13

LED1_PIN = 17   # Yellow1
LED2_PIN = 27   # Yellow2
LED3_PIN = 22   # Yellow3
LED4_PIN = 5    # Yellow4
LED5_PIN = 2 # RED

LEDs = [LED1_PIN, LED2_PIN, LED3_PIN, LED4_PIN, LED5_PIN]

import led
import helpers
import time

import RPi.GPIO as GPIO
from gpiozero import Button

def on_button_held():
    print("Button pressed for 5 seconds, initiating reboot...")
    os.system("sudo reboot")


def on_button_released():
    print("Button released.")


def main():

    GPIO.cleanup()
    ## Eingabezeile leeren
    helpers.clear_screen()

    
    # Initializing GPIOs
    GPIO.setmode(GPIO.BCM)
    
    led.init_gpio(LEDs[4])

    button = Button(26, pull_up=True, bounce_time=0.2, hold_time=5)
    button.when_held = on_button_held
    button.when_released = on_button_released
    
    
    while True:
        print("New cycle")
        led.led_control(LEDs[4], GPIO.HIGH)
        time.sleep(1)
        led.led_control(LEDs[4], GPIO.LOW)
        time.sleep(1)




if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program terminated manually")
    finally:
        GPIO.cleanup()

