import RPi.GPIO as GPIO


def init_gpio(pin: int):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)


def led_control(pin: int, mode=GPIO.LOW):
    GPIO.output(pin, mode)


def cleanup_gpio():
    GPIO.cleanup()