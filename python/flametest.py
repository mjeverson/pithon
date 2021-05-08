from gpiozero import DigitalOutputDevice
from time import sleep

flame1 = DigitalOutputDevice(4)

while True:
    print("looping")
    flame1.on()
    sleep(1)
    flame1.off()
    sleep(1)