import machine, neopixel, esp, network, time, math, utime
from generic_dotstar import Apa102DotStar as APA102
#from apa102 import APA102
from ringbuffer import RINGBUFFER
### MICROPHONE
OUT = 35  # Connect it to OUT on microphone
NUM_LEDS = 60
mic = machine.ADC(machine.Pin(OUT))
mic.atten(machine.ADC.ATTN_11DB)
clock = machine.Pin(18)
data = machine.Pin(23)
apa = APA102(clock, data, NUM_LEDS)
timer = machine.Timer(0)
rbuffer = RINGBUFFER(100)

def handleInterrupt(timer):
    global rbuffer, mic
    rbuffer.put(mic.read())


timer.init(period=1, mode=machine.Timer.PERIODIC, callback=handleInterrupt)


def run(threshold):
    mid = 2048
    envelope = 0
    threshold = 1500
    beatline = 100
    first_zero = 1
    highest = 50
    brightness = 3
    beatcounter = 0
    counter = 0
    beat = False
    beatchange = False
    offbeat = True
    offbeatcounter = 0
    offbeatcountme = 0

    while True:
        global rbuffer
        val = rbuffer.get()
        if val != None: 
            if (val > mid): mid +=1 
            if (val < mid): mid -=1 
            envelope = abs(mid-val)
            if envelope > beatline: 
                beatline = envelope
            else: 
                beatline -= 5
        else: 
            continue
    	env = beatline
    	if counter < 5000:
    	    if counter % 100 == 0:
    		    print (beatline)
    	    counter +=1 
    	    continue
    	if env > threshold and beat == False:
    	    offbeat = False
    	    beat = True
    	    beatchange = True
    	    beatcounter +=1
            brightness = 20
    	    print('beat no'+str(beatcounter)+" Envelope Value: "+str(env)+" Threshold: "+str(threshold))
    	    print ("Number of reads below threshold during offbeat "+str(offbeatcountme))
    	    offbeatcountme = 0
    	elif envelope > threshold and beat == True: 
    	    beatchange == False
    	    print ("Same Beat  Envelope Value: "+str(env)+"   Threshold "+str(threshold))
    	elif env < threshold and offbeat == False:
    	    beat = False
            brightness = 3
    	    offbeatcounter += 1
    	    offbeat = True
    	    beatchange = True
    	    print ("Offbeat " + str(offbeatcounter)+ " Envelope Value "+str(env))
    	elif env < threshold and offbeat == True: 
    	    beatchange = False
    	    offbeatcountme +=1
        if beatchange == True: 
            for i in range(NUM_LEDS):
                apa[i] = (255, 0, 0, brightness)
            apa.write()
run(1000)