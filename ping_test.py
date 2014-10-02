import time
import smbus


bus = smbus.SMBus(1) # bus address,. 0 or 1. use i2cdetect to find out
address = 0x04 # address of the micro

while True:
	bus.write_byte_data(address, 1, 10) # write to register 1 the value 10 to start a ping. data is unused and can be anything
	while True:
		time.sleep(0.01) # don't bother it too quickly
		tmp = bus.read_byte(address)
		if tmp != 0:
			print tmp
			break
