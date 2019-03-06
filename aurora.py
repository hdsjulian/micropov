import machine, neopixel, esp, network, time, math, utime
#from generic_dotstar import Apa102DotStar as APA102
from apa102 import APA102
from rgbhsv import rgb2hsv, hsv2rgb
NUM_LEDS = 60
clock = machine.Pin(14)
data = machine.Pin(13)
apa = APA102(clock, data, NUM_LEDS*2)
brightness = 1

colors = [(0, 0, 0, 0), (20,232,30, 3), (0,234,141, 3),(1,126,213, 3), (181,61,255, 3), (141,0,196, 3), (20,232,30, 3)]
colors = [(0, 0, 0), (20,232,30), (0,234,141),(1,126,213), (181,61,255), (141,0,196), (20,232,30)]
colors = [(141,0,196), (181,61,255), (1,126,213), (0,234,141), (20,232,30)]
for i in range(len(colors)):
	colors[i] = rgb2hsv(*colors[i])

FILLER = (0, 25, 0, 1)


"""
grün
eisblau
stahlblau
lilaish
dunkellila
"""

def grad(start, end, steps, brightness):
	starthue = colors[start]
	endhue = colors[end]
	currenthue = starthue
	returncolors = []
	for i in range(steps):
		r, g, b = hsv2rgb(*currenthue)
		returncolors.append((r,g,b, brightness))
		currenthue = (currenthue[0]+(endhue[0]-starthue[0])/(steps), currenthue[1], currenthue[2])
	return returncolors

def scale(brightness = 10):

	sequence = [1, 1, 2, 4, 8]	
	sequencelength = sum(sequence)
	zeropoint = 0-sequencelength
	for startingpoint in range(NUM_LEDS):
		led = zeropoint
		print ("zeropoint = "+str(zeropoint))
		if zeropoint > 0: 
			for i in range(zeropoint):
				apa[i] = (FILLER) 
				apa[(2*NUM_LEDS)-1-i] = (FILLER)
		for i in range(len(sequence)-1):
			gradcolors = grad(i, i+1, sequence[i], brightness)
			for j in range(sequence[i]):
				doubleLED = zeropoint + ((sequencelength*2)-led-1)+zeropoint
				if led > 0 and led < NUM_LEDS:
					apa[led] = gradcolors[j]
					apa[(2*NUM_LEDS)-1-led] = gradcolors[j]
				if doubleLED > 0 and doubleLED < NUM_LEDS:
					apa[doubleLED] = gradcolors[j]
					apa[(2*NUM_LEDS)-1-doubleLED] = gradcolors[j]
				led +=1
		r, g, b = hsv2rgb(*colors[i+1])
		midcolor = (r, g, b, brightness)
		for j in range(sequence[i+1]):
			doubleLED = zeropoint + ((sequencelength*2)-led-1)+zeropoint
			if led > 0 and led < NUM_LEDS: 
				midcolor = (r, g, b, brightness)
				apa[led] = midcolor
				apa[(2*NUM_LEDS)-1-led] = midcolor
			if doubleLED > 0 and doubleLED < NUM_LEDS:
				apa[doubleLED] = midcolor
				apa[(2*NUM_LEDS)-1-doubleLED] = midcolor

			led += 1
		lastpos = led+sequencelength
		while (lastpos) < NUM_LEDS:
			apa[lastpos] = (FILLER)
			apa[(2*NUM_LEDS)-1-lastpos] = (FILLER)
			lastpos += 1
		zeropoint += 1
		apa.write()





def aurora(apa, start, length):
    for i in range(length):
    	cindex = (i+start%len(colors)) % len(colors)
    	print(cindex)
        c = colors[cindex]
        apa[i] = c
    apa.write()

def aurora_anim(np, length, speed):
    i = 0
    while True:	
        aurora(np, i, length)
        time.sleep_ms(speed)
        i+=1
        if i ==length:
            print (i)
            i=0
#aurora_anim(apa, 60, 100)