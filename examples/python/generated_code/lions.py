"""
@file lions.py

@brief LMsg definition.
LMsg is a class that represents a message in the Lions protocol.

This file contains the implementation of the message classes generated by the Lions Compiler.

@details
This file was generated by the Lions Compiler (https://github.com/ItsNotSoftware/lions).
Modifying this file manually is not recommended as it may lead to unexpected behavior.

@note
Generated files should not be manually edited.

@authored by Lions Compiler
"""


import struct
from typing import List

MAX_PAYLOAD_SIZE = 248


class Header:
    def __init__(self):
        self.src = 0
        self.dst = 0
        self.next_hop = 0
        self.msg_id = 0
        self.checksum = 0


class LMsg:
    def __init__(self, payload_size: int):
        self.header = Header()
        self.payload = bytearray(payload_size)
        self.payload_size = payload_size

    def calculate_checksum(self) -> int:
        self.header.checksum = 0

        # Calculate checksum for the header
        self.header.checksum += self.header.src
        self.header.checksum += self.header.dst
        self.header.checksum += self.header.msg_id
        self.header.checksum += self.header.next_hop

        # Calculate checksum for the payload
        self.header.checksum += sum(self.payload[: self.payload_size])

        self.header.checksum = ~self.header.checksum & 0xFFFF

        return self.header.checksum

    def valid_checksum(self) -> bool:
        prev_checksum = self.header.checksum
        return self.calculate_checksum() == prev_checksum