# MIT License
#
# Copyright (c) [YEAR] [COPYRIGHT HOLDER]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations

from dataclasses import dataclass


@dataclass()
class RawMessageData:
    message_length: int
    message_type: int
    payload: bytes

    @classmethod
    def from_bytes(cls, msg: bytes) -> RawMessageData:
        message_length = decode_length(msg)
        if message_length < 128:
            # length encoded in the first byte
            message_type = msg[2]
            payload = msg[3:]
        else:
            # length encoded in the first and second byte
            message_type = msg[3]
            payload = msg[4:]
        return cls(message_length, message_type, payload)

    def update_message_length(self):
        self.message_length = len(self.payload) + 3

    def to_bytes(self) -> bytes:
        return encode_length(self.message_length) + bytes([0]) + bytes([self.message_type]) + self.payload


def encode_length(l: int) -> bytes:
    if l < 128:
        return bytes([l])
    else:
        return bytes([(l & 0xFF) | 0x80, (l >> 7) & 0xFF])


def decode_length(msg: bytes) -> int:
    if msg[0] & 0xF0 == 0:
        return msg[0]
    else:
        return (msg[0] & 0x7F) | (msg[1] << 7)
