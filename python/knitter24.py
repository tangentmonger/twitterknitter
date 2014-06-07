"""Communicates with TwitterKnitter hardware (i.e. Arduino)
over serial to send a pattern"""

import serial
from pattern24 import Pattern24
from time import sleep

class Knitter24:
    """Knitting machine (v1, 24 stitch patterns)"""
    
    def __init__(self, usb='/dev/ttyUSB0', baud=9600):
        self.serial = serial.Serial(usb, baud)

    def send_pattern(self, pattern):
        """Given a Pattern24 send it out over serial"""
        for row in pattern.get_pattern():
            # we want to output LSB first
            byte3, byte2, byte1 = self.pack_row(row) 
            self.serial.write([byte1, byte2, byte3])
            self.serial.flush()
            self.serial.read(1) #block until KM acks
            print("ACK")

    @classmethod
    def pack_row(cls, row):
        """Given a 24-value tuple, convert it to a tuple of three bytes"""
        #assumption: tuple was 24 items long and contained only '0' and '1'
        binary_pattern = [str(x) for x in row]
        row_string = ''.join(binary_pattern)
        print(row_string, end=" ")
        return (int(row_string[0:8], 2), 
                int(row_string[8:16], 2), 
                int(row_string[16:24], 2))
