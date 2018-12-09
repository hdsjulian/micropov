import utime
import lis3dh
import machine
i2c=machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
print(i2c.scan())
accelerometer=lis3dh.LIS3DH_I2C(i2c, address=24)


class ShakePoint:
	def __init__(self):
		self.g = 0
		self.micros = 0

class Shaker: 
	def __init__(self):
		i2c=machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
		print(i2c.scan())
		self.accelerometer=lis3dh.LIS3DH_I2C(i2c, address=24)
		self.hysteresis = 0
		self.sensitivity = 5.0
		#last time it took to go from accel minimum to maximum
		self.min2maxDelta = 0
		self.max2minDelta = 0
		self.min2maxFrames = 0
		self.max2minFrames = 0
		#timestamp of current minimum or maximum
		self.lastMin = ShakePoint()
		self.lastMax = ShakePoint()
		self.activeMin = ShakePoint()
		self.activeMax = ShakePoint()
		self.activeFramesMin2Max = 0
		self.activeFramesMax2Min = 0
		#searching for Minimum? then True, or Maximum? then False
		self.searchMin = True
		#only fire events once
		self.firedPredictedZero = False
		self.firedPredictedExtremum = False
		#find out what to do here
		self.sameCount = 0
		self.diffCount = 0
		#number of frames in pic, replace with image loader
		self.frames = 16
		#starting time of current frame
		self.frameStartTime = 0
		self.frameIndex = 0
		self.isActive = False
		self.isFrameIndexActive = False
		self.currentMicros = 0



	def getFrameIndex(self):
		if (self.isActive and self.isFrameIndexActive):
			return self.frameIndex
		else: 
			return -1


	def update(self, g):
		self.lastMicros = self.currentMicros
		self.currentMicros = utime.ticks_us()
		#if we are shaking
		if (self.isActive and self.isFrameIndexActive):
			self.frameIndex += -1 if self.searchMin else 1
			#if we are past zero or past max number of frames
			if self.frameIndex < 0 or self.frameIndex >= selfframes:
				self.isFrameIndexActive = False
		#if we aren't currently shaking
		else:
			#if at least 500ms have passed or last minimum plus sensitivity is larger than last maximum (out of range)
			if self.lastMin.micros > self.currentMicros + 500 * 1000 or (self.lastMin.g + self.sensitivity) > self.lastMax.g:
				self.isActive = False
			else: 
				self.isActive = True
		#set last frame index and timestamp when frame index was static
		self.lastFrameIndex = 0
		self.lastFrameIndexStaticTime = 0
		#if frameindex has stayed the same
		if self.frameIndex == self.lastFrameIndex:
			#add the time passed since last static time
			self.lastFrameIndexStaticTime += self.currentMicros - self.lastMicros
		else:
			lastFrameIndexStaticTime = 0
		self.lastFrameIndex = self.frameIndex
		#if 500ms have passed since frameindex has been static, become inactive
		if self.lastFrameIndexStaticTime > 500 * 1000:
			self.isActive = False
		#iterate frames
		self.activeFramesMin2Max += 1
		self.activeFramesMax2Min += 1
		#if we are searching for a minimum (shaking left)
		if (self.searchMin): 
			#if we are still moving
			if g < self.activeMin.g:
				#set new minum g
				self.activeMin.g = g
				#set new minimum microseconds
				self.activeMin.micros = self.currentMicros
				#set newminium to maximum (swipe right) frame counter to zero
				self.activeFramesMin2Max = 0
				#set the frame to active
				self.max2minFrames = self.activeFramesMax2Min
			#if g + hysteresis is larger than last one
			if g > (self.activeMin.g + self.hysteresis):
				#set last V 
				self.lastV = self.max2minDelta
				#set lastmin to the currently active minimum
				self.lastMin = self.activeMin
				#time it took from last maximum to last (current) minimum
				self.max2minDelta = self.lastMin.micros - self.lastMax.micros
				#not looking for minimum anymore
				self.searchMin = False
				#not fired yet
				self.firedPredictedZero = False
				#not fired extremum
				self.firedPredictedExtremum = False
				#set the frame start time
				self.frameStartTime = self.lastMin.micros + self.min2maxDelta / 2 - ((float(self.min2maxDelta) / self.min2maxFrames)*self.frames)/2
				#set frame index to inactive
				isFrameIndexActive = False
				#check if max2mindelta has stayed the same
				self.dSame = self.max2minDelta - self.lastV
				if self.dSame < 0:
					#if so, turn it around
					self.dSame = -self.dSame
				self.dDiff = self.max2minDelta - self.min2maxDelta
				if self.dDiff < 0:
					self.dDiff = -self.dDiff
				if self.dSame <= self.dDiff:
					self.sameCount +=1
				else:
					self.diffCount +=1
				self.activeMax.g = g
				self.activeMax.micros = self.currentMicros
			elif (not self.firedPredictedZero and (self.currentMicros > self.frameStartTime)):
				self.frameIndex = self.frames -1
				isFrameIndexActive = True
				firedPredictedZero = True
			elif (not self.firedPredictedExtremum and self.currentMicros >= (self.lastMax.micros + self.max2minDelta)):
				self.firedPredictedExtremum = True
		else:
			if g > self.activeMax.g:
				self.activeMax.g = g
				self.activeMax.micros = self.currentMicros
				self.activeFramesMax2Min = 0
				self.min2maxFrames = self.activeFramesMin2Max
			if g < (self.activeMax.g - self.hysteresis):
				self.lastMax = self.activeMax
				self.min2maxDelta = self.lastMax.micros = self.lastMin.micros
				self.searchMin = True
				self.firedPredictedZero = False
				self.firedPredictedExtremum = False
				self.frameStartTime = self.lastMax.micros + self.max2minDelta / 2 - ((float(self.max2minDelta) / self.max2minFrames) * self.frames) / 2
				self.isFrameIndexActive = False
				self.activeMin.g = g
				self.activeMin.micros = self.currentMicros
			elif (not self.firedPredictedZero and self.currentMicros > self.frameStartTime):
				self.frameIndex = 0
				self.isFrameIndexActive = True
				self.firedPredictedZero = True
		return self.isActive


shaker = Shaker()

def step(shaker):
	x, y, z = [value / lis3dh.STANDARD_GRAVITY for value in shaker.accelerometer.acceleration]
	if shaker.update(x):
		index = shaker.getFrameIndex()
		if index > 0:
			#set LEDs to Index
			print(index)
while True:
	step(shaker)



