import RPi.GPIO as GPIO
import time

# ======================================================================================
# Pin Config (BCM)
# ======================================================================================
IN1 = 17   # Left motor direction
IN2 = 27   # Left motor direction
IN3 = 23   # Right motor direction
IN4 = 22   # Right motor direction
ENA = 12   # Left motor speed
ENB = 13   # Right motor speed

# ======================================================================================
# Setup
# ======================================================================================
GPIO.setmode(GPIO.BCM)
for pin in [IN1, IN2, IN3, IN4, ENA, ENB]:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

pwm_a = GPIO.PWM(ENA, 1000)
pwm_b = GPIO.PWM(ENB, 1000)
pwm_a.start(0)
pwm_b.start(0)

def set_speed(speed):
    pwm_a.ChangeDutyCycle(max(0, speed - 5))
    pwm_b.ChangeDutyCycle(speed)

def forward(speed=100):
    set_speed(speed)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def backward(speed=100):
    set_speed(speed)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def turn_left(speed=100):
    set_speed(speed)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def turn_right(speed=100):
    set_speed(speed)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def stop():
    set_speed(0)
    for pin in [IN1, IN2, IN3, IN4]:
        GPIO.output(pin, GPIO.LOW)

def clean_up():
    pwm_a.stop()
    pwm_b.stop()
    stop()
    GPIO.cleanup()

# ======================================================================================
# Test
# ======================================================================================
if __name__ == '__main__':
    try:
        print("Forward 100%")
        forward(100)
        time.sleep(1)

        print("Stop")
        stop()
        time.sleep(1)

        print("Backward 100%")
        backward(100)
        time.sleep(1)

        print("Stop")
        stop()
        time.sleep(1)

        print("Turn left")
        turn_left(100)
        time.sleep(1)

        print("Stop")
        stop()
        time.sleep(1)

        print("Turn right")
        turn_right(100)
        time.sleep(1)

        print("Stop")
        stop()
        print("Done!")

    except KeyboardInterrupt:
        pass
    finally:
        clean_up()