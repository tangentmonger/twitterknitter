twitterknitter
==============

TOG's 70's knitting machine knits tweets.

Travis CI status: ![Travis status] (https://travis-ci.org/tangentmonger/twitterknitter.svg?branch=master "Travis status")

![The TwitterKnitter](https://raw.githubusercontent.com/tangentmonger/twitterknitter/master/img/contraption.jpg "The TwitterKnitter")

![Row change microswitch](https://raw.githubusercontent.com/tangentmonger/twitterknitter/master/img/microswitch.jpg "Row change microswitch")

![Hello world](https://raw.githubusercontent.com/tangentmonger/twitterknitter/master/img/helloworld.jpg "Hello world")

Knitting machine: Empisal Knitmaster 321

Extra hardware: contraption made of 24 servos, laser cut dibblers, three LEDs and a microswitch.

arduino/knitting.ino runs on an Arduino Mega and controls the knitting machine hardware.

python/server.py runs on a laptop connected to the Arduino via USB. Converts tweets to images and sends them to the Mega via USB. Python 3

