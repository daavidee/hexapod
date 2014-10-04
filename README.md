<h1>Note: This project is a work in progress.</h1>
<h2>About</h2>
This project is based around Python and the <a href="http://en.wikipedia.org/wiki/Raspberry_Pi">Raspberry Pi</a>. It is a 6-legged (hexapod) robot with 3 degrees of freedom per leg. Currently it can walk linearly, interface with a PS3 controller, stream 1080p30 video, talk via flite and an on-board speaker, sense objects with an ultrasonic sensor offloaded to an ATmega328P and collect acceleration data. Facial recognition using the camera with <a href="http://opencv.org/">OpenCV</a>, full integration of all features and more are underway.

<h2>Hardware</h2>
<ul>
	<li>1 x <a href="http://en.wikipedia.org/wiki/Raspberry_Pi">Model B Raspberry Pi</a></li>
	<li>1 x 4GB or bigger SD Card</li>
	<li>1 x Low-power USB wifi module used for connection to a home network</li>
	<li>1 x Low-power USB bluetooth module used for connection to the PS3 controller</li>
	<li>2 x <a href="http://www.adafruit.com/products/815">16-Channel 12-bit PWM Drivers</a> used for control of the servo PWM signals. This is based on the <a href="http://www.nxp.com/documents/data_sheet/PCA9685.pdf">PCA9685</a> which has its own internal clock. Each driver controls one side of the robot for a total of 9 servos controlled per driver</li>
	<li>19 x High Torque <a href="http://www.hobbyking.com/hobbyking/store/__28972__H_King_High_Torque_Metal_Geared_Ball_Bearing_Waterproof_Servo_58g_12_8kg_cm_0_22s_60.html">analog servos</a></li>
	<li>1 x <a href="http://www.hobbyking.com/hobbyking/store/__9172__Turnigy_5000mAh_2S_20C_Lipo_Pack.html">2s1p Lipo Battery Pack</a></li>
	<li>1 x <a href="http://www.hobbyking.com/hobbyking/store/__10312__Turnigy_5A_8_26v_SBEC_for_Lipo.html">5A SBEC</a> for converting the 8.4V from the Lipo Battery to 5V for the Pi</li>
	<li>1 x <a href="http://www.hobbyking.com/hobbyking/store/__40274__Hobbyking_YEP_20A_HV_2_12S_SBEC_w_Selectable_Voltage_Output.html">20A SBEC</a> for converting the 8.4V from the Lipo Battery to 6V for the servos</li>
	<li>2 x (1/8" x 1.5" x 48") aluminum flats bought from Home Depot and cut with a scroll saw for the legs. The frame is made from salvaged aluminum</li>
	<li>1 x <a href="http://www.adafruit.com/products/1367">CSI Camera</a></li>
	<li>1 x Audio amplifier. A <a href="http://www.electronicaestudio.com/docs/VMA2012.pdf">VMA2012 amplifier</a> was used</li>
	<li>1 x Generic 0.4W 8Ohm Speaker</li>
	<li>1 x 12V fuse and holder. A 20A 32V fuse was used</li>
	<li>1 x 12V Toggle switch</li>
	<li>1 x <a href="http://www.hobbyking.com/hobbyking/store/__18987__On_Board_Lipoly_Low_Voltage_Alarm_2s_4s_.html">Lipo low voltage alarm</a></li>
	<li>1 x Solderless breadboard for prototyping purposes</li>
	<li>1 x <a href="http://www.adafruit.com/products/914">Pi breakout</a> for easy interfacing to a breadboard</li>
	<li>2 x <a href="http://www.atmel.com/Images/doc8161.pdf">Atmega328P</a></li>
	<li>1 x <a href="http://media.digikey.com/pdf/Data%20Sheets/Bosch/BMA180_Flyer.pdf">BMA180 Accelerometer module.</a></li>
	<li>1 x <a href="https://docs.google.com/document/d/1Y-yZnNhMYy7rwhAgyL_pfa39RsB-x2qR4vP8saG73rE/edit">HC-SR04 Ultrasonic Module.</a></li>
</ul>

<h2>Software Requirements</h2>
The following modules should be installed using apt-get after installing <a href="http://www.raspbian.org/">Raspbian</a> on the Raspberry Pi:
	<ul>
		<li>Python</li>
		<li><a href="http://www.festvox.org/flite/">flite</a> tts engine</li>
		<li><a href="http://opencv.org/">OpenCV</a> for facial recognition (not yet implemented)</li>
		<li><a href="http://www.pygame.org">Pygame </a></li>
		<li>Sixpair for pairing the PS3 controller to the bluetooth module and the <a href="http://qtsixa.sourceforge.net/">sixad</a> driver. <a href="http://booting-rpi.blogspot.ro/2012/08/dualshock-3-and-raspberry-pi.html">This</a> tutorial may be helpful. You may need to modify the sixad sourcecode as described <a href="http://www.raspberrypi.org/forums/viewtopic.php?f=78&t=16702&sid=1f1d82acca88f4ace5195643900b1123&start=29">here</a> in order for the controller to work.</li>
	</ul>
The <a href="https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/tree/master/Adafruit_PWM_Servo_Driver">Adafruit_PWM_Servo_Driver</a> library is included in the source and is used for low-level control of the <a href="http://www.nxp.com/documents/data_sheet/PCA9685.pdf">PCA9685</a> chip via the I2C bus. A sixAxis wrapper library I wrote is also included for ease of use.

<h2>Notes</h2>
<ul>
	<li>An Atmega328P is used to offload the ultrasonic sensing for reliable measurements</li>
	<li>Most of the parts can be ordered from <a href="http://www.adafruit.com">Adafruit</a> and <a href="http://www.hobbyking.com">Hobbyking</a></li>
</ul>
