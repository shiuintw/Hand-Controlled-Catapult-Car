import RPi.GPIO as GPIO
import time

# ==============================================
# Pin Config (BCM)
# ==============================================
IN1 = 17   # Left motor direction
IN2 = 27   # Left motor direction
IN3 = 22   # Right motor direction
IN4 = 23   # Right motor direction

# ==============================================
# Setup
# ==============================================
GPIO.setmode(GPIO.BCM)
for pin in [IN1, IN2, IN3, IN4]:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def backward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def turn_left():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def turn_right():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def stop():
    for pin in [IN1, IN2, IN3, IN4]:
        GPIO.output(pin, GPIO.LOW)

# ==============================================
# Test
# ==============================================
try:
    print("Forward")
    forward()
    time.sleep(2)

    print("Stop")
    stop()
    time.sleep(1)

    print("Backward")
    backward()
    time.sleep(2)

    print("Stop")
    stop()
    time.sleep(1)

    print("Turn left")
    turn_left()
    time.sleep(2)

    print("Stop")
    stop()
    time.sleep(1)

    print("Turn right")
    turn_right()
    time.sleep(2)

    print("Stop")
    stop()
    print("Done!")

except KeyboardInterrupt:
    pass
finally:
    stop()
    GPIO.cleanup()