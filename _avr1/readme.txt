Interfaces the hr-sr04 ultrasonic sensor with an ATmega328P and the Raspberry Pi through the i2c bus

To use flash the sketch to a suitable AVR (I used avrdude and linuxspi with my raspberry pi as an ISP) and test using ping_test.py

notes:
-power the avr with 3.3v so 5v doesn't go back to the pi through the i2c pins
-power the sensor with 5V from the pi for stable readings and !!USE A LEVEL SHIFTER ON THE ECHO PIN!! to the avr
-the included hex file is for an ATmega328P with the 8MHz internal oscillator and NO BOOTLOADER


libraries used:
NewPing and RunningMedian (median function in newping had some quirks)