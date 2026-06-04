import RPi.GPIO as GPIO
import time

# ======================================================================================
# Pin Config (BCM)
# ======================================================================================
SERVO_PIN = 18 # GPIO 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

pwm = GPIO.PWM(SERVO_PIN, 50)  # 50Hz
pwm.start(0)

def set_angle(angle):
    # 0° = 2.5%, 90° = 7.5%, 180° = 12.5%
    duty = 2.5 + (angle / 180) * 10
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)  # stop jitter

def clean_up():
    pwm.stop()
    GPIO.cleanup()

# ======================================================================================
# Test
# ======================================================================================
if __name__ == '__main__':
    try:
        while True:
            print("0 degrees")
            set_angle(0)
            time.sleep(1)

            print("170 degrees")
            set_angle(170)
            time.sleep(1)

    except KeyboardInterrupt:
        pass
    finally:
        clean_up()