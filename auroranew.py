import utime, time, machine
from apa102 import APA102
from rgbhsv import rgb2hsv, hsv2rgb
NUM_LEDS = 60
clock = machine.Pin(14)
data = machine.Pin(13)
apa = APA102(clock, data, NUM_LEDS*2)
brightness = 1
apa.fill((0, 120, 0, 1))
apa.write()
brightness = [1]*NUM_LEDS
fader = []
print(brightness)
def fade(fader, brightness): 
	print ("Fade Called")
	print(fader)
	width = fader['width']
	middlepin = fader['middlepin']
	currentBrightness = fader['currentBrightness']
	currentBrightness += 1
	targetBrightness  = fader['targetBrightness']
	for i in range(targetBrightness):
		if abs(brightness[middlepin])-i > 0:
			brightness[middlepin+i] = abs(currentBrightness) -i
			brightness[middlepin-i] = abs(currentBrightness) - i
			print ("new brightn i "+str(i))
			print(brightness)
	if currentBrightness == targetBrightness: 
		currentBrightness = targetBrightness*(-1)
		targetBrightness = 1
	
	if currentBrightness == 0 and targetBrightness == 1: 
		currentBrightness = False
	else: 
		currentBrightness +=1
	fader['currentBrightness'] = currentBrightness
	return fader, brightness
i = 0
while True:
	print ("-----")
	print(fader)
	print ("------")
	if utime.ticks_us() % 4 == 1:
		append = utime.ticks_us() % 60
		print ("BLEEP "+str(append))
		fader.append({"middlepin": append, "currentBrightness" : 1, "targetBrightness" : 4, "width": 3})
		print(fader)
	fadernew = []
	for i in range(len(fader)):
		fader[i], brightness = fade(fader[i], brightness)
		if fader[i]['currentBrightness'] != False: 
			fadernew.append(fader[i])
	fader = fadernew
	print (brightness)
	for i in range(NUM_LEDS):
		apa.buf[i*4+3] = brightness[i]
		print((NUM_LEDS*2*4-(i*4))+3)
		apa.buf[(NUM_LEDS*2*4)-(i*4+3)] = brightness[i]
	apa.write()
	time.sleep_ms(100)
