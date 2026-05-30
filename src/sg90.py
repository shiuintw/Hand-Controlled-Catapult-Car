import RPi.GPIO as GPIO
import time

SERVO_PIN = 12 # GPIO 18

GPIO.setmode(GPIO.BOARD)
GPIO.setup(SERVO_PIN, GPIO.OUT)

pwm = GPIO.PWM(SERVO_PIN, 50)  # 50Hz
pwm.start(0)

def set_angle(angle):
    # 0° = 2.5%, 90° = 7.5%, 180° = 12.5%
    duty = 2.5 + (angle / 180) * 10
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)  # stop jitter

try:
    while True:
        print("0 degrees")
        set_angle(0)
        time.sleep(1)

        print("90 degrees")
        set_angle(90)
        time.sleep(1)

        print("180 degrees")
        set_angle(180)
        time.sleep(1)

except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.cleanup()