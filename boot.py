import machine, neopixel, esp, network, time, math, utime, gc, urandom
import micropython
from machine import SPI, Pin
from apa102 import APA102
NUM_LEDS = 120
NUM_MODES = 6
BRIGHTNESS = 20
try: 
	f = open('mode.txt', 'r')
	mode = int(f.read())
	f.close()
except Exception as e: 
	mode = 1
	print ("fehler")
	print (e.__class__.__name__)
print(mode)
try: 
	f = open('mode.txt', 'w')
	if mode % NUM_MODES == 0:
		f.seek(0)
		f.write(str(1))
		print ("one")
	elif mode <= NUM_MODES: 
		f.seek(0)
		f.write(str(mode+1))
except Exception as e: 
	print(e.__class__.__name__)

f.close()
time.sleep(3)
clock = machine.Pin(14)
data = machine.Pin(13)
apa = APA102(clock, data, NUM_LEDS)
def no_debug():
    # this can be run from the REPL as well
    esp.osdebug(None)

gamma = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,3,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,8,8,8,9,9,9,10,10,10,11,11,11,12,12,13,13,14,14,14,15,15,16,16,17,17,18,18,19,19,20,21,21,22,22,23,23,24,25,25,26,27,27,28,29,29,30,31,31,32,33,33,34,35,36,36,37,38,39,40,40,41,42,43,44,45,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,74,75,76,77,78,79,81,82,83,84,86,87,88,89,91,92,93,95,96,97,99,100,101,103,104,105,107,108,110,111,113,114,115,117,118,120,121,123,125,126,128,129,131,132,134,136,137,139,140,142,144,145,147,149,151,152,154,156,158,159,161,163,165,166,168,170,172,174,176,178,179,181,183,185,187,189,191,193,195,197,199,201,203,205,207,209,211,213,215,217,220,222,224,226,228,230,232,235,237,239,241,244,246,248,250,253,255]
#np = neopixel.NeoPixel(machine.Pin(4), 144, timing=True)

"""
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect("WLIAN", "WaldMoeveBowieCanyon")
"""

def colorfill (r, g, b, brightness=3):
	apa.fill((r, g, b, brightness))
	apa.write()


if mode == 1:
	def initialize_rgb(start, end):
		maxdistance = 0
		longest = 0
		rgb = {
			0 : { 
				"start" : start[0],
				"end" : end[0],
				"current" : start[0],
			},
			1 : {
				"start" : start[1],
				"end" : end[1],
				"current" : start[1],
			},
			2 : {
				"start" : start[2],
				"end" : end[2],
				"current" : start[2],
			}
		}

		for i in range(len(start)):
			current_distance = abs(start[i]-end[i])
			if maxdistance < current_distance:
				longest = i
				maxdistance = current_distance
		for i in range(len(start)):
			if rgb[i]["start"]-rgb[i]["end"] != 0:
				rgb[i]["step"] = abs(float(maxdistance)/float((rgb[i]["start"]-rgb[i]["end"])))
			else: 
				rgb[i]["step"] = 0	
		return rgb, maxdistance




	def switch_start_and_end(rgb):
		for i in range(len(rgb)): 
			rgb[i]["end"] = rgb[i]["start"]
			rgb[i]["start"] = rgb[i]["current"]
		return rgb

	def nextstep(rgb, iterator):
		for i in range(len(rgb)):
			if rgb[i]["step"]>0 and abs(rgb[i]["current"]-rgb[i]["start"]) < int(abs(iterator/rgb[i]["step"])) and rgb[i]["current"] != rgb[i]["end"]:
				if rgb[i]["end"] - rgb[i]["start"] > 0:
					rgb[i]["current"] += 1
				else:
					rgb[i]["current"] -= 1
		colorfill(gamma[rgb[0]["current"]], gamma[rgb[1]["current"]], gamma[rgb[2]["current"]], BRIGHTNESS)
			#apa[i] = (rgb[0]["current"], rgb[1]["current"], rgb[2]["current"], )
		#print("Red "+str(rgb[0]["current"])+" Green" +str(rgb[1]["current"])+" Blue "+str(rgb[2]["current"]))

	def step_through(rgb, maxdistance): 
		for i in range(maxdistance+1):
			nextstep(rgb, i)
			time.sleep_ms(5)
		time.sleep_ms(2000)
		return switch_start_and_end(rgb)
	def run(rgb, maxdistance, endtime = 0):
		starttime = utime.time()
		while True: 
			if endtime != 0 and utime.time() > starttime + endtime: 
				break
			rgb = step_through(rgb, maxdistance)
	start_green = 0
	end_green = 0
	start_blue = 0
	end_blue = 128
	start_red = 128
	end_red = 0

	start = [start_red, start_green, start_blue]
	end = [end_red, end_green, end_blue]
	rgb, maxdistance = initialize_rgb(start, end)
	run(rgb, maxdistance)
else: 
	#@micropython.native	
	def hsv2rgb(h: int, s: int, v:int):
		print("hsv")
		print (h, s, v)
		h60 = h // 60
		dings = int(h60//1000)
		h60f = (dings*1000)
		hi = int(h60f//1000) % 6
		f = (h60 - h60f)
		p = v * (1000 - s)
		q = v * (1000 - (f * s)//1000)
		t = v * (1000 - (1000 - f) * s//1000)
		p = p//1000
		q = q//1000
		t = t//1000
		r1 = 0
		g1 = 0
		b1 = 0
		if hi == 0: 
			r1 = v
			g1 = t
			b1 = p
		elif hi == 1: 
			r1 = q
			g1 = v
			b1 = p
		elif hi == 2: 
			r1 = p
			g1 = v
			b1 = t
		elif hi == 3:
			r1 = p
			g1 = q
			b1 = v
		elif hi == 4: 
			r1 = t
			g1 = p
			b1 = v
		elif hi == 5: 
			r1 = v
			g1 = p
			b1 = q
		r = r1*255
		r = r1//1000
		g = g1*255
		g = g1//1000
		b = b1*255
		b = b1//1000
		#print("First, secodnd, third, alltogether = ", str(second-first), str(third-second), str(fourth-third), str(fourth-first))
		print (h60, dings, h60f, hi, r, g, b)
		return r, g, b
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
	#@micropython.native	
	def apa_update(apa, position, r, g, b, brightness):
	    position = position * 4
	    apa.buf[position] = r
	    position +=1 
	    apa.buf[position] = g
	    position +=1 
	    apa.buf[position] = b
	    position +=1 
	    apa.buf[position] = brightness
	    return apa

if mode == 2:
	def double_rainbow(apa, start, length):
	    for i in range(length):
	        h = int((i+start)*(360/length))
	        s = 1.0
	        v = 0.1
	    	r, g, b = hsv2rgb(h, s, v)
	        apa = apa_update(apa, i, r, g, b, 31)
	        apa = apa_update(apa, (2*length)-1-i, r, g, b, 31)
	    apa.write()

	def rainbow_anim(apa, length, speed, endtime = 0):
	    starttime = utime.time()
	    i = 0
	    while True:	
	    	if endtime != 0 and utime.time() > starttime + endtime:
	    		print ("breaking")
	    		break
	    	measure_start = utime.ticks_us()
	        double_rainbow(apa, i, length)
	        #print(utime.ticks_us()-measure_start)
	        time.sleep_ms(speed)
	        i+=1
	        if i ==length:
	            i=0
	print ("rainbow?")
	rainbow_anim(apa, 60, 1)

if mode == 3 or mode == 4 or mode == 5:
	def fade(fader, brightness): 

		width = fader['width']
		middlepin = fader['middlepin']
		currentBrightness = fader['currentBrightness']
		currentBrightness += 1
		targetBrightness  = fader['targetBrightness']
		for i in range(targetBrightness):
			if abs(brightness[middlepin])-i > 0:
				if middlepin+i < NUM_LEDS: 
					brightness[middlepin+i] = abs(currentBrightness) - i
				if middlepin-i > 0:
					brightness[middlepin-i] = abs(currentBrightness) - i
		if currentBrightness == targetBrightness: 
			currentBrightness = targetBrightness*(-1)
			targetBrightness = 1
		
		if currentBrightness == 0 and targetBrightness == 1: 
			currentBrightness = False
		else: 
			currentBrightness +=1
		fader['currentBrightness'] = currentBrightness
		return fader, brightness
	def aurora(r=0, g=120, b=0, rando = False, endtime = 0):
		starttime = utime.time()
		apa.fill((r, g, b, 1))
		apa.write()
		brightness = [1]*NUM_LEDS
		fader = []
		while True:
			if endtime != 0 and utime.time() > starttime + endtime: 
				break
			if rando == True:
				if utime.ticks_us() % 128 == 1:
					colorfill(urandom.getrandbits(8), urandom.getrandbits(8), urandom.getrandbits(8), 1)
					fader = []
					continue
			if utime.ticks_us() % 8 == 1:
				append = utime.ticks_us() % 60
				fader.append({"middlepin": append, "currentBrightness" : 1, "targetBrightness" : 8, "width": 3})
			fadernew = []
			for i in range(len(fader)):
				fader[i], brightness = fade(fader[i], brightness)
				if fader[i]['currentBrightness'] != False: 
					fadernew.append(fader[i])
			fader = fadernew
			for i in range(NUM_LEDS/2):
				apa.buf[i*4+3] = max(brightness[i], 1)
				apa.buf[((NUM_LEDS*4)-(i*4))-1] = max(brightness[i], 1)
			apa.write()
			gc.collect()
			time.sleep_ms(80)	
if mode == 3:
	print("aurora")
	aurora(0, 120, 0, False)
if mode == 4:
	print("aurora ice")
	aurora(162,210,223, False)
if mode == 5:
	print("aurora colors")
	aurora(186,242,239, True)
if mode == 6:
	def gummiband(apa, r, g, b, length, sleep):
		mid = (length // 2) +1
		for i in range(mid):
			time.sleep_ms(sleep)
			apa.fill((r, g, b, 1))
			for j in range(i+1):
				apa_update(apa, mid-j, gamma[r-j*2], g, gamma[b+j*2], max(i-j, 1))
				apa_update(apa, (2*length)-1-mid-j, gamma[r-j*2], g, gamma[b+j*2], max(i-j, 1))
				apa_update(apa, mid+j, gamma[r-j*2], g, gamma[b+j*2], max(i-j, 1))
				apa_update(apa, (2*length)-1-mid+j, gamma[r-j*2], g, gamma[b+j*2], max(i-j, 1))
			apa.write()
		time.sleep_ms(2000)
		for i in range(mid, 0, -1):
			time.sleep_ms(sleep)
			apa.fill((r, g, b, 1))
			for j in range(i):
				apa_update(apa, mid-j, gamma[r-j*2], g, gamma[b+j*2], max(i-j, 1))
				apa_update(apa, (2*length)-1-mid-j, gamma[r-j*2], g, gamma[b+j*2], max(i-j, 1))
				apa_update(apa, mid+j, gamma[r-j*2], g, gamma[b+j*2], i-j)
				apa_update(apa, (2*length)-1-mid+j, gamma[r-j*2], g, gamma[b+j*2], max(i-j, 1))
			apa.write()	
	print ("gummiband")
	while True: 
		gummiband(apa, 125, 0, 25, 60, 100)
		gc.collect()
		time.sleep(2)



#apa.fill((0, 0, 0))


#while True:
#	step_through(rgb)