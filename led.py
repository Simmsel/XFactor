import RPi.GPIO as GPIO

"""
from main import LED1_PIN
from main import LED2_PIN
from main import LED3_PIN
from main import LED4_PIN
from main import LED5_PIN
from main import LEDs
"""
from example import LED1_PIN
from example import LED2_PIN
from example import LED3_PIN
from example import LED4_PIN
from example import LED5_PIN
from example import LEDs

LED_matrix = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
]

cyclic_counter = 0


def init_gpio(pin: int):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)


def led_control(pin: int, mode=GPIO.LOW):
    GPIO.output(pin, mode)


def led_blink():
    global cyclic_counter
    current_states = LED_matrix[cyclic_counter]

    for i in [0, 1, 2, 3]:
        if current_states[i]==1:
            led_control(LEDs[i], GPIO.HIGH)
        elif current_states[i]==0:
            led_control(LEDs[i], GPIO.LOW)

    # increment by 1 for next cycle of blink
    cyclic_counter+=1
    if cyclic_counter == len(LED_matrix): # because for length = 7, last index is 6
        cyclic_counter = 0
