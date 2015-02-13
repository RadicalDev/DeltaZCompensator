__author__ = 'jfindley'

import socket, sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = sys.argv[1]
s.bind(("0.0.0.0", port))


while True:
    client, addr = s.accept()
    print "{0}: CXN From: ".format(port), addr
    x = client.makefile()
    while True:
        try:
            data = x.readline()
            if not data:
                continue
            print data
        except:
            break
