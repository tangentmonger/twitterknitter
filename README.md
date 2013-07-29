twitterknitter
==============

TOG's 70's knitting machine knits tweets.

Knitting machine: Empisal Knitmaster 321

Extra hardware: contraption made of 24 servos, laser cut dibblers, three LEDs and a microswitch.

knitting.ino runs on an Arduino Mega and controls the knitting machine hardware.

server.py runs on a laptop connected to the Arduino via USB. Converts tweets to images and sends them to the Mega via USB.
