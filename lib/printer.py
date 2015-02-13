__author__ = 'jfindley'
import serial


class Printer(object):
    def __init__(self, com_port, baud_rate):
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.printer = None
        self.printer_connected = False

    def disconnect(self):
        raise NotImplementedError

    def connect(self):
        raise NotImplementedError

    def write(self, command):
        raise NotImplementedError

    def read(self):
        raise NotImplementedError

    def isConnected(self):
        raise NotImplementedError


class FakeOrionDelta(Printer):
    def disconnect(self):
        self.printer_connected = False

    def connect(self):
        self.printer_connected = True

    def isConnected(self):
        return self.printer_connected

    def read(self):
        if self.isConnected():
            return "ok"
        return "NOT CONNECTED"

    def write(self, command):
        if self.isConnected():
            print "Sending: ", command
        else:
            print "NOT CONNECTED: ", command


class OrionDelta(Printer):
    def disconnect(self):
        if self.isConnected():
            try:
                self.printer.close()
            except Exception, e:
                print "Unable to close connection: ", e

        self.printer_connected = False
        return

    def connect(self):
        self.printer = serial.Serial(self.com_port, self.baud_rate)
        wait_count = 0
        while True:
            data = self.printer.readline()
            #print "From {0}: {1}".format(self.com_port, data)

            if "wait" in data:
                wait_count += 1

            if wait_count == 3:
                break

        print "Connected to printer on port {0}".format(self.com_port)
        self.printer_connected = True

    def isConnected(self):
        return self.printer_connected

    def write(self, command):
        if not self.isConnected():
            print "NOT CONNECTED: ", command
            return

        #print "Sending: ", command
        res = 'resend'
        while True:
            if 'resend' in res:
                self.printer.write(command.strip() + "\n")

            res = self.read()
            while not res:
                res = self.read()
            #print "Response: ", res
            if "ok" in res:
                break

    def read(self):
        if self.isConnected():
            return self.printer.readline().strip()
        return None



if __name__ == "__main__":
    printer = FakeOrionDelta(1, 2)
    printer.connect()
    printer.write("test")
    printer.read()
    printer.disconnect()
    printer.write("test")