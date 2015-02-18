__author__ = 'jfindley'
import serial
import numpy as np


class DialIndicator(object):
    def __init__(self, com_port, baud_rate, min_reads=10):
        self.min_reads = min_reads
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.dial = None
        self.dial_connected = False

    def disconnect(self):
        raise NotImplementedError

    def connect(self):
        raise NotImplementedError

    def read(self):
        raise NotImplementedError

    def isConnected(self):
        raise NotImplementedError

    def parse_reading(self, data):
        return NotImplementedError


class FakeDialIndicator(DialIndicator):
    def disconnect(self):
        self.dial_connected = False

    def connect(self):
        self.dial_connected = True

    def isConnected(self):
        return self.dial_connected

    def read(self):
        return self.parse_reading(1)

    def parse_reading(self, data):
        return data


class HumanDialIndicator(DialIndicator):
    def disconnect(self):
        self.dial_connected = False

    def connect(self):
        self.dial_connected = True

    def isConnected(self):
        return self.dial_connected

    def read(self):
        while True:
            try:
                data = float(raw_input("Measurement: "))
                return self.parse_reading(data)
            except Exception, e:
                print "Invalid entry: ", e

    def parse_reading(self, data):
        return data
    

class HF93295(DialIndicator):
    def connect(self):
        self.dial = serial.Serial(self.com_port, self.baud_rate)
        self.dial_connected = True

    def disconnect(self):
        self.dial.close()
        self.dial_connected = False

    def isConnected(self):
        return self.dial_connected

    def read(self):
        self.connect()

        values = []
        while True:
            data = self.dial.readline().strip()
            if len(data) != 24:
                continue

            val = self.parse_reading(data)
            # if val < -10 or val > 10:
            #     continue

            if not values or all([val == x for x in values]):
                values.append(val)
            else:
                values = []

            if len(values) == self.min_reads:
                self.disconnect()
                return -val

    def parse_reading(self, data):
        val = int(data[1:-3][::-1], 2)/100.0
        if data[-3] == '1':
            val = -val
        return val

if __name__ == "__main__":
    dial = HF93295("/dev/ttyACM0", 115200)
    dial.connect()
    while True:
        print dial.read()