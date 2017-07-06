from pyo import *


def pp(address, *args):
    print address
    print args


s = Server().boot()
s.start()
r = OscDataReceive(8001, "/data/test", pp)
# Send various types
a = OscDataSend("fissif", 8000, "/data/test")
msg = [3.14159, 1, "Hello", "world!", 2, 6.18]
a.send(msg)
# Send a blob
b = OscDataSend("b", 8000, "/data/test")
msg = [[chr(i) for i in range(10)]]
b.send(msg)
# Send a MIDI noteon on port 0
c = OscDataSend("m", 8000, "/data/test")
msg = [[0, 144, 60, 100]]
c.send(msg)
d = OscDataSend("i", 8000, "/data/test")
msg = [1]
d.send(msg)
s.gui(locals)
