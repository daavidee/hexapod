#!/usr/bin/env python

import time
import smbus
import thread
from common import *


class hcsr04:
	currentDistance = -1;
	def __init__(self, busAddress, i2cAddress):
		self.bus = smbus.SMBus(busAddress) # bus address.. 0 or 1. use i2cdetect to find out
		self.address = i2cAddress # address of the micro
		log("initialized connection to ATmega328P at address " + str(self.address) + " on i2c bus number " + str(busAddress))
	def ping(self):
		try:
			self.bus.write_byte_data(self.address, 1, 10) # write to register 1 the value 10 to start a ping. data is unused and can be anything
			for i in range(1, 10):
				time.sleep(0.05) # don't bother it too quickly
				tmp = self.bus.read_byte(self.address)
				if tmp > 0: return tmp
				if tmp == -1: return tmp
			return -1
		except:
			return self.currentDistance
	def updateObjectDistance(self):
		while True:
			self.currentDistance = self.ping()
			time.sleep(0.05)
	def beginIntervalPinging(self):
		thread.start_new_thread(self.updateObjectDistance, ())
	def getPingDistance(self):
		return self.currentDistance
