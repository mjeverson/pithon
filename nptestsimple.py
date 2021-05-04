import board
import neopixel
import time
pixels = neopixel.NeoPixel(board.D18, 30)
pixels.fill((255,0,0))
print("Did the thing")
time.sleep(2)