"""
@file my_messages_lmsg.py

@brief  my_messages lmsg Classes

This file contains the declaration of the message classes generated by the Lions Compiler.

@details
This file was generated by the Lions Compiler (https://github.com/ItsNotSoftware/lions) on .
Modifying this file manually is not recommended as it may lead to unexpected behavior.

@note
Generated files should not be manually edited.

@authored by Lions Compiler
"""

from .lions_ import LMsg, Header
import struct
from enum import Enum

class MsgID(Enum):
    accelerometer = 1
    microphone = 2
    ping = 3


class MsgPeriod(Enum):
    accelerometer = 1000
    microphone = 0
    ping = 1000



class AccelerometerMsg:
    def __init__(self, acc_x: float, acc_y: float, acc_z: float):
        self.header = Header()
        self.acc_x = acc_x
        self.acc_y = acc_y
        self.acc_z = acc_z
        
    @staticmethod
    def from_lmsg(msg: LMsg) -> "AccelerometerMsg":
        
        acc_x = struct.unpack("<float", msg.payload[0:4])[0]
        acc_y = struct.unpack("<float", msg.payload[4:8])[0]
        acc_z = struct.unpack("<float", msg.payload[8:12])[0] 
        instance = AccelerometerMsg(acc_x, acc_y, acc_z)
        instance.header = msg.header

        return instance

    def encode(self, src: int, dst: int, next_hop: int) -> LMsg:
        msg = LMsg()
        msg.header.src = src
        msg.header.dst = dst
        msg.header.next_hop = next_hop
        msg.header.msg_id = 1 
        
        msg.payload[0:4] = struct.pack("<float", self.acc_x) 
        msg.payload[4:8] = struct.pack("<float", self.acc_y) 
        msg.payload[8:12] = struct.pack("<float", self.acc_z) 
        
        msg.calculate_checksum()

        return msg

class MicrophoneMsg:
    def __init__(self, sound_level: int, message: str):
        self.header = Header()
        self.sound_level = sound_level
        self.message = message
        
    @staticmethod
    def from_lmsg(msg: LMsg) -> "MicrophoneMsg":
        
        sound_level = struct.unpack("<int", msg.payload[0:2])[0]
        message = msg.payload[2:102].decode('utf-8')
         
        instance = MicrophoneMsg(sound_level, message)
        instance.header = msg.header

        return instance

    def encode(self, src: int, dst: int, next_hop: int) -> LMsg:
        msg = LMsg()
        msg.header.src = src
        msg.header.dst = dst
        msg.header.next_hop = next_hop
        msg.header.msg_id = 2 
        
        msg.payload[0:2] = struct.pack("<int", self.sound_level) 
        msg.payload[2:102] = self.message.encode('utf-8')
         
        
        msg.calculate_checksum()

        return msg

class PingMsg:
    def __init__(self, ):
        self.header = Header()
        
    @staticmethod
    def from_lmsg(msg: LMsg) -> "PingMsg":
         
        instance = PingMsg()
        instance.header = msg.header

        return instance

    def encode(self, src: int, dst: int, next_hop: int) -> LMsg:
        msg = LMsg()
        msg.header.src = src
        msg.header.dst = dst
        msg.header.next_hop = next_hop
        msg.header.msg_id = 3 
        
        
        msg.calculate_checksum()

        return msg


