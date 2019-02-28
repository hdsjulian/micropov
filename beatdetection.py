import machine, neopixel, esp, network, time, math, utime
from generic_dotstar import Apa102DotStar as APA102
### MICROPHONE
OUT = 35  # Connect it to OUT on microphone
NUM_LEDS = 60
mic = machine.ADC(machine.Pin(OUT))
mic.atten(machine.ADC.ATTN_11DB)
clock = machine.Pin(18)
data = machine.Pin(23)
apa = APA102(clock, data, NUM_LEDS)
timer = machine.Timer(0)

mid = 2048
envelope = 0

def handleInterrupt(timer):
	global envelope, mid
	val = mic.read()
	if (val > mid): mid +=1 
	if (val < mid): mid -=1 
	envelope = abs(mid-val)
timer.init(period=1, mode=machine.Timer.PERIODIC, callback=handleInterrupt)

def run(threshold):
    global ringbuffer
    first_zero = 1
    highest = 50
    brightness = 3
    beatcounter = 0
    offbeatcounter = 0
    counter = 0
    beat = False
    beatchange = False
    offbeat = True
    while True:
    	global envelope
    	print(envelope)
    	if counter < 5000:
    	    if counter % 100 == 0:
    		    print (counter)
    	    counter +=1 
    	    continue
    	if envelope > threshold and beat == False:
    	    offbeat = False
    	    beat = True
    	    beatchange = True
    	    beatcounter +=1
    	    print('beat no'+str(beatcounter)+" envelope "+str(envelope))
    	elif envelope > threshold and beat == True: 
    	    beatchange == False
    	    print ("Same Beat"+str(envelope)+"   "+str(counter))
    	elif envelope < threshold and offbeat == False:
    	    beat = False
    	    offbeatcounter += 1
    	    offbeat = True
    	    beatchange = True
    	    print ("Offbeat " + str(offbeat)+ " envelope "+str(envelope))
    	elif envelope < threshold and offbeat == True: 
    	    beatchange = False
        time.sleep(0.001)
run(45)