import board
import neopixel
import random

# Connected to pin 18 with 30 LEDs
pixels = neopixel.NeoPixel(board.D18, 30)

rnd_red, rnd_green, rnd_blue = random.sample(range(0, 256), 3)
# Fill all the pixel RANDOM colour - Assuming it's a RGB strip
pixels.fill((rnd_red, rnd_green, rnd_blue))
