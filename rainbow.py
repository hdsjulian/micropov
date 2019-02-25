
import machine, neopixel, esp, network, time, math
from generic_dotstar import DotStar
from generic_dotstar import Apa102DotStar as APA102
from generic_dotstar import SpiDotStar as SPIDotStar
from machine import SPI, Pin
NUM_LEDS = 120


apa = APA102(Pin(18), Pin(23), NUM_LEDS) # Just one DotStar
NUM_MODES = 2
BRIGHTNESS = 20

def hsv2rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b
    
def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return h, s, v

def double_rainbow(np, start, length):
    for i in range(length):
        h = (i+start)*(360/length)
    	if i == 1:
    		print ("setting h to "+str(h))
        apa[i] = (hsv2rgb(h, 1.0, 0.10))
        apa[(2*length)-i]=(hsv2rgb(h, 1.0, 0.10))
    apa.write()

def rainbow_anim(np, length, speed):
    i = 0
    while True:	
        double_rainbow(np, i, length)
        time.sleep_ms(speed)
        i+=1
        if i ==length:
            print (i)
            i=0

rainbow_anim(apa, 60, 1)
