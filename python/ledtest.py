from gpiozero import PWMLED
from time import sleep

led = PWMLED(18)

while True:
    print("looping")
    led.on()
    sleep(1)
    led.off()
    sleep(1)