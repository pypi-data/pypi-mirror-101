from pyjuni.deflib import *

class Packet:
    def __init__(self, model = JDCODE):
        self.model = model
        self.packet = bytearray(20) 
        if self.model == JDCODE:
            self.packet[0:5] = [0x26, 0xA8, 0x14, 0xB1, 0x14]
        elif self.model == UGLYBOT:
            self.packet[0:5] = [0x26, 0xA8, 0x14, 0xE1, 0x14]
        elif self.model == JCBOARD:
            self.packet[0:5] = [0x26, 0xA8, 0x14, 0xC1, 0x14]
        else:
            self.packet[0:5] = [0x26, 0xA8, 0x14, 0x00, 0x14]


    def getPacket(self):
        return self.packet


    def makePacket(self, start, data):
        for n in range(start, start+len(data)):
            self.packet[n] = data[n-start]
        self.packet[5] = DefLib.checksum(self.packet)
#        DefLib._print(self.packet)
        return self.packet
       

    def clearPacket(self):
        for n in range(5, 20):
            self.packet[n] = 0
        if self.model == JDCODE:
            self.packet[5] = self.packet[14] = 0x01
            self.packet[16] = self.packet[18] = 0x64
        return self.packet
