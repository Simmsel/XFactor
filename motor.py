import RPi.GPIO as GPIO
import time

from main import OPEN_ANGLE
from main import CLOSE_ANGLE
from main import SERVO_PIN

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

pwm = GPIO.PWM(SERVO_PIN, 50)  # 50 Hz for SG90 Servos
pwm.start(0)



def angle_to_duty_cycle(angle):
    # Dca. 2% - 12% Duty Cycle for 0 - 180 Degree
    return 2 + (angle / 180) * 10



def move(angle):
    global pwm
    duty_cycle = angle_to_duty_cycle(angle)
    pwm.ChangeDutyCycle(duty_cycle)
    print(f"Moving Servo to angle: {angle}° (Duty Cycle: {duty_cycle}%)")
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)


def open():
    print("Opening...")
    move(OPEN_ANGLE)

def close():
    print("Locking...")
    move(CLOSE_ANGLE)
