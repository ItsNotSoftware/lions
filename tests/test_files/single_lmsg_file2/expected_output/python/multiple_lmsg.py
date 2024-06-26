"""
@file multiple_lmsg.py

@brief  multiple lmsg Classes

This file contains the declaration of the message classes generated by the Lions Compiler.

@details
This file was generated by the Lions Compiler (https://github.com/ItsNotSoftware/lions) on .
Modifying this file manually is not recommended as it may lead to unexpected behavior.

@note
Generated files should not be manually edited.

@authored by Lions Compiler
"""

from .lions import LMsg, Header
import struct

# msg ids 
MSG_ID_ACCELEROMETER = 1
MSG_ID_MICROPHONE = 2
MSG_ID_PING = 3


# msg periods
MSG_PERIOD_ACCELEROMETER = 1000
MSG_PERIOD_MICROPHONE = 0
MSG_PERIOD_PING = 1000



class AccelerometerMsg:
    def __init__(self, acc_x: float, acc_y: float, acc_z: float):
        self.header = Header()
        self.acc_x = acc_x
        self.acc_y = acc_y
        self.acc_z = acc_z
        
    @staticmethod
    def from_lmsg(msg: LMsg) -> "AccelerometerMsg":
        
        acc_x = struct.unpack("<f", msg.payload[0:4])[0]
        acc_y = struct.unpack("<f", msg.payload[4:8])[0]
        acc_z = struct.unpack("<f", msg.payload[8:12])[0] 
        instance = AccelerometerMsg(acc_x, acc_y, acc_z)
        instance.header = msg.header

        return instance

    def encode(self, src: int, dst: int, next_hop: int) -> LMsg:
        msg = LMsg(12)
        msg.header.src = src
        msg.header.dst = dst
        msg.header.next_hop = next_hop
        msg.header.msg_id = 1 
        
        msg.payload[0:4] = struct.pack("<f", self.acc_x) 
        msg.payload[4:8] = struct.pack("<f", self.acc_y) 
        msg.payload[8:12] = struct.pack("<f", self.acc_z) 
        msg.calculate_checksum()

        return msg


    def __str__(self) -> str:
        s = "\n[AccelerometerMsg]\n"
        s += f"    {self.header}\n\n"
        s += f"    acc_x: {self.acc_x}\n" 
        s += f"    acc_y: {self.acc_y}\n" 
        s += f"    acc_z: {self.acc_z}\n" 
        
        return s

class MicrophoneMsg:
    def __init__(self, sound_level: int, message: str):
        self.header = Header()
        self.sound_level = sound_level
        self.message = message
        
    @staticmethod
    def from_lmsg(msg: LMsg) -> "MicrophoneMsg":
        
        sound_level = struct.unpack("<h", msg.payload[0:2])[0]
        message = msg.payload[2:102].decode('utf-8')
         
        instance = MicrophoneMsg(sound_level, message)
        instance.header = msg.header

        return instance

    def encode(self, src: int, dst: int, next_hop: int) -> LMsg:
        msg = LMsg(102)
        msg.header.src = src
        msg.header.dst = dst
        msg.header.next_hop = next_hop
        msg.header.msg_id = 2 
        
        msg.payload[0:2] = struct.pack("<h", self.sound_level) 
        msg.payload[2:102] = self.message.encode('utf-8')
         
        msg.calculate_checksum()

        return msg


    def __str__(self) -> str:
        s = "\n[MicrophoneMsg]\n"
        s += f"    {self.header}\n\n"
        s += f"    sound_level: {self.sound_level}\n" 
        s += f"    message: {self.message}\n" 
        
        return s

class PingMsg:
    def __init__(self, ):
        self.header = Header()
        
    @staticmethod
    def from_lmsg(msg: LMsg) -> "PingMsg":
         
        instance = PingMsg()
        instance.header = msg.header

        return instance

    def encode(self, src: int, dst: int, next_hop: int) -> LMsg:
        msg = LMsg(0)
        msg.header.src = src
        msg.header.dst = dst
        msg.header.next_hop = next_hop
        msg.header.msg_id = 3 
        
        msg.calculate_checksum()

        return msg


    def __str__(self) -> str:
        s = "\n[PingMsg]\n"
        s += f"    {self.header}\n\n"
        
        return s


