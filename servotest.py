from adafruit_servokit import ServoKit
import time
kit = ServoKit(channels=16)
# works great with "tower sg92r"
#the "tower sg-5010" servo has problems,
# min 0.75ms max2.25ms
#kit.servo[0].set_pulse_width_range(750, 2250)
#kit.servo[0].actuation_range = 90
print("GO!")
kit.servo[0].angle = 90

kit.servo[0].angle = 0
print("GO!")
time.sleep(0.2)
kit.servo[0].angle = 90
