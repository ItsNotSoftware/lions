from generated_code.my_messages_lmsg import *


acc = AccelerometerMsg(1, 2, 34)
print(acc)
msg = acc.encode(1, 2, 3)
acc = AccelerometerMsg.from_lmsg(msg)
print(acc)

print()

mic = MicrophoneMsg(-123, "Hello World!")
print(mic)
msg = mic.encode(4, 5, 6)
mic = MicrophoneMsg.from_lmsg(msg)
print(mic)

print()

ping = PingMsg()
print(ping)
msg = ping.encode(7, 8, 9)
ping = PingMsg.from_lmsg(msg)
print(ping)
