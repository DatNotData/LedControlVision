
***

YOU MUST RUN BOTH PYTHON SCRIPT AT THE SAME TIME.
THE RUN_ME.py SCRIPT SHOULD TAKE CARE OF THAT FOR YOU.

***



General informations : 
	Project goal : Use vision to control a led's brightness.
	Languages used : Python & Arduino
	Electric components : Arduino, LED, 220 ohm resistor
	Library for vision : OpenCV
	Communication protocol between Python & Arduino : Serial

The goal of the project is to use hand motions to control the brightness of an LED.
The vision code is written in Python using the OpenCV library.
The code is not completely done.
Hand motion isn't perfect yet and I'm still using a colored object for the target.

The vision code will analyze the frame taken by my computer's webcam and find the center of the target.
It will then do some maths to calculate what brightness we want to LED to be.
It will then write that value to a buffer file.
Another code will read that buffer file and will send the value to the Arduino via serial communication.
The Arduino code will read the serial message.
It will translate the message to a usable value and will make a PWM output that matches our needs.

The LED's anode is connected to the Arduino via a 220 ohm resistor at pin 3.

If you have any sugegstiosns, please email : datfalcon@gmail.com

Have fun!
