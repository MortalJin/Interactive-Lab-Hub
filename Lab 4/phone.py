
import time
import qwiic_proximity
import pi_servo_hat

# Phone detection thresholds
PHONE_ON_THRESHOLD = 1000
PHONE_OFF_THRESHOLD = 500

# Servo settings
CLOSED_ANGLE = 0
OPEN_ANGLE = 120
SERVO_CHANNEL = 0

# Initialize the proximity sensor
sensor = qwiic_proximity.QwiicProximity()

if not sensor.connected:
    print("Proximity sensor not found. Check the Qwiic connection.")
    raise SystemExit

sensor.begin()

# Initialize the servo
servo = pi_servo_hat.PiServoHat()
servo.restart()

phone_present = False

# Start with the snack box closed
servo.move_servo_position(SERVO_CHANNEL, CLOSED_ANGLE)
print("System ready. Waiting for a phone...")

try:
    while True:
        proximity = sensor.get_proximity()
        print("Proximity:", proximity)

        # Open the box when a phone is detected
        if not phone_present and proximity > PHONE_ON_THRESHOLD:
            print("Phone detected. Opening the snack box!")
            servo.move_servo_position(SERVO_CHANNEL, OPEN_ANGLE)
            phone_present = True

        # Close the box when the phone is removed
        elif phone_present and proximity < PHONE_OFF_THRESHOLD:
            print("Phone removed. Closing the snack box.")
            servo.move_servo_position(SERVO_CHANNEL, CLOSED_ANGLE)
            phone_present = False

        time.sleep(0.2)

except KeyboardInterrupt:
    print("\nProgram stopped. Closing the snack box.")
    servo.move_servo_position(SERVO_CHANNEL, CLOSED_ANGLE)